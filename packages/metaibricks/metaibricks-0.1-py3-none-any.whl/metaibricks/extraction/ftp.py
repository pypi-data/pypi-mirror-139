import itertools
import os
import ftplib
import netrc
import shutil
import re
from typing import Any, Optional, List, Tuple, Dict, Iterator, Union
from multiprocessing import Pool
from functools import partial

from pydantic import BaseModel, SecretStr, Field, validator

from metaibricks.settings import Settings, Logger, log_error
from metaibricks.extraction.base import ExtractorBase

LOGGER = Logger(name="extraction.ftp")


class FTPSession(BaseModel):
    """Model used for handling FTP sessions

    Attrs:
        host (str):  Host's name
        username (Optional[str]): user's name used to log in. If not provided,
            the one given in .netrc will be used.
        password (Optional[str]): password associated to the username. If not
            provided, the one given in the .netrc will be used.

    Private Attrs:
        _handler (ftplib.FTP): FTP handler. It is used as a private attribute
            in order to prevent timeouts by using it through the "handler" property.

    Example:
        >>> os.listdir("my_dir")
        []
        >>> cat ~/.netrc
        machine toto.meteo.fr login my_login password my_password
        >>> session = FTPSession(host="toto.meteo.fr")
        >>> session
        FTPSession(
            host="toto.meteo.fr",
            username="my_login",
            password=SecretStr("********")
        )
        >>> session.password.get_secret_value()
        "my_password"
        >>> session.get("/my/remote/file.txt", "my_dir/file.txt")
        >>> os.listdir("my_dir")
        ["file.txt"]
    """

    host: str
    username: Optional[str]
    password: Optional[SecretStr]
    _handler: Optional[ftplib.FTP] = None

    class Config:
        underscore_attrs_are_private = True
        arbitrary_types_allowed = True

    @validator("username", always=True)
    def check_username(cls, v: str, values: dict) -> str:
        """method to validate given user's name or retreiving it if missing.
        """
        if v is None:
            return netrc.netrc(Settings().netrc_filename).authenticators(
                host=values.get("host")
            )[0]
        return v

    @validator("password", always=True)
    def check_password(cls, v: str, values: dict) -> SecretStr:
        """method to validate and protect given password, or retrieving it if
        missing.
        """
        if isinstance(v, SecretStr):
            return v
        if v is None:
            return SecretStr(
                netrc.netrc(Settings().netrc_filename).authenticators(
                    host=values.get("host")
                )[-1]
            )
        return SecretStr(v)

    @property
    def handler(self) -> ftplib.FTP:
        """property to activate then expose the FTP handler associated with the given
        credentials.

        Returns:
            ftplib.FTP: FTP Handler
        """
        try:
            self._handler.pwd()  # just verifying if activated
        except (AttributeError, ftplib.error_perm):
            self._handler = ftplib.FTP(
                host=self.host,
                user=self.username,
                passwd=self.password.get_secret_value(),
            )
            LOGGER.info("FTP handler activation", host=self.host, user=self.username)
        return self._handler

    def find_pattern(
        self, pattern: str, dirname: Optional[Union[str, List[str]]] = "."
    ) -> List[str]:
        """Method that finds all the directories or files which name matches with
        the given pattern, in the directory "dirname".

        Args:
            pattern (str): Pattern to match.
            dirname (Optional[Union[str, List[str]]]): Directory or list of
                directories where to find matching patterns. Defaults to ".".

        Returns:
            List[str]: List of all the directories or files matching the given pattern.
        """
        if isinstance(dirname, list):
            results = []
            for dname in dirname:
                results.extend(self.find_pattern(pattern, dname))
            return results

        if pattern in ("", "/"):
            # pattern root case
            return ["/"]

        if dirname == "":
            # dirname root case
            dirname = "/"

        try:
            self.handler.cwd(dirname)
        except ftplib.error_perm:
            LOGGER.warning(
                "Given pattern and directory's name matches with a file",
                host=self.host,
                dirname=dirname,
                pattern=pattern,
            )
            return []
        return [
            os.path.join(dirname, basename)
            for basename in self.handler.nlst()
            if re.match(pattern, basename)
        ]

    def get(self, src_filename: str, dst_filename: str) -> bool:
        """Main method to get a given filename from source and to copy it
        in a destination.

        Args:
            src_filename (str): Remote source file's name.
            dst_filename (str): Local destination file's name.

        Returns:
            bool: Whether the extraction is alright or not.
        """
        log_info = dict(
            host=self.host, src_filename=src_filename, dst_filename=dst_filename
        )
        LOGGER.debug("Trying to get file.", **log_info)

        # checking existing
        if os.path.isfile(dst_filename):
            LOGGER.warning("Destination file already exists: skipping.", **log_info)
            return os.path.isfile(dst_filename)

        # using a tmp file
        dst_abs_filename = os.path.abspath(dst_filename)
        dirname, basename = os.path.split(dst_abs_filename)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        tmp_filename = os.path.join(dirname, f".{basename}.tmp")

        # extracting file
        try:
            with open(tmp_filename, "wb") as fp:
                self.handler.retrbinary(f"RETR {src_filename}", fp.write)
            LOGGER.debug("File extracted.", **log_info, tmp_filename=tmp_filename)
        except Exception:
            LOGGER.error("Failed to get file.", **log_info, exc_info=True)
            os.remove(tmp_filename)
            return False

        # renaming file
        if os.path.isfile(tmp_filename):
            shutil.copyfile(tmp_filename, dst_abs_filename)
            LOGGER.debug(
                "Temporary file copied to destination file.",
                tmp_filename=tmp_filename,
                **log_info,
            )
            os.remove(tmp_filename)
            LOGGER.debug(
                "Temporary file removed.", tmp_filename=tmp_filename, **log_info
            )
        else:
            LOGGER.error(
                "Failed to create temporary file.",
                tmp_filename=tmp_filename,
                **log_info,
            )
            return False

        if not os.path.isfile(dst_filename):
            LOGGER.error("File extraction failed.", **log_info)

        LOGGER.info("File correctly extracted.", **log_info)
        return True


class FTPExtractorBase(ExtractorBase):
    """Abstract class for defining an FTPExtractor

    Attrs:
        kind (str): Extractor's kind. Constant "FTP".
    """

    kind: str = Field("FTP", const=True)


class FTPFiles(FTPExtractorBase):
    """Extractor used for extracting multiple given files using FTP.

    Attrs:
        kind (str): Constant "FTP"
        session (FTPSession): FTP session to use for extracting multiple files.
        files (List[Tuple[str, str]]): List of files to get. Each element of
            the list is a tuple containing the source file's name and the destination
            file's name.
        n_workers (Optional[int]): Numbers of workers to use to parallelize the
            extraction.

    Example:
        >>> os.listdir("my_dir")
        []
        >>> extr = FTPFiles(
                session={"host": "toto.meteo.fr"},
                files=[
                    ("/my/remote/file1.txt", "./my_dir/file1.txt"),
                    ("/my/remote/file2.txt", "./my_dir/file2.txt"),
                ]
            )
        >>> extr.run()
        >>> os.listdir("my_dir")
        ["file1.txt", "file2.txt"]
    """

    session: FTPSession
    files: List[Tuple[str, str]]

    def run(self) -> bool:
        """Main method to get all self.files.

        Returns:
            bool: Whether the extraction is alright or not.
        """
        if self.n_workers <= 1:
            return all([self.session.get(src, dst) for src, dst in self.files])
        result = []
        pool = Pool(self.n_workers)
        for src, dst in self.files:
            pool.apply_async(
                FTPSession(**self.session.dict()).get,
                args=(src, dst,),
                callback=result.append,
                error_callback=partial(log_error, log=LOGGER),
            )
        pool.close()
        pool.join()
        return all(result)


class FTPDir(FTPExtractorBase):
    """Extractor used for extracting multiple files using FTP.
    With this extractor file's name are not explicitly specified, but
    the source and destination directories are specified using constraints.

    Attrs:
        kind (str): Extractor's kind. Constant "FTP".
        session (FTPSession): FTP Session to use for extracting all files.
        src (str): Remote source files's pattern. It may contain tags "{}"
            to specify constraints (from self.constraints).
        dst (str): Local destination files's pattern. It also may contain
            tags "{}" to specify constraints (from self.constraints and src groups).
        constraints (Dict[str, List[Any]]): Dictionnary containing the possible values
            of all the tags given in src.
        n_workers (Optional[int]): Numbers of workers to use to parallelize the
            extraction.

    Private Attrs::
        _files (List[Tuple[str, str]]): List of files to retrieve when they have been
            found remotely according to the src description.

    Example:
        >>> os.listdir("my_dir")
        []
        >>> extr = FTPDir(
                session={"host": "toto.meteo.fr"},
                src="/my/remote/{year}/{month:02d}/(?P<basename>.\\w+.txt)",
                dst="my_dir/{year}_{month:02d}/{basename}",
                constraints={
                    "date": [2021],
                    "month": [1, 2, 3],
                }
            )
        >>> list(os.get_constraints_combinations())
        [
            {"year": 2021, "month": 1},
            {"year": 2021, "month": 2},
            {"year": 2021, "month": 3},
        ]
        >>> extr.files
        [
            ("/my/remote/2021/01/file1.txt", "my_dir/2021_01/file1.txt"),
            ("/my/remote/2021/01/file2.txt", "my_dir/2021_01/file2.txt"),
            ("/my/remote/2021/02/file3.txt", "my_dir/2021_02/file3.txt"),
            ("/my/remote/2021/03/file4.txt", "my_dir/2021_03/file4.txt"),
        ]
        >>> extr.run()
        >>> os.listdir("my_dir")
        ["2021_01", "2021_02", "2021_03"]
        >>> os.listdir("my_dir/2021_01")
        ["file1.txt", "file2.txt"]
    """

    kind: str = Field("FTP", const=True)
    session: FTPSession
    src: str
    dst: str
    constraints: Dict[str, List[Any]]
    _files: List[Tuple[str, str]] = None

    def get_constraints_combinations(self) -> Iterator[Dict[str, Any]]:
        """Generator made for creating the possible combinations
        with the given constraints.

        Yields:
            Iterator[Dict[str, Any]]: Iteration of dictionnaries with the name
                of the constraint as key, and its given value.
        """
        for values in itertools.product(*self.constraints.values()):
            yield {k: v for k, v in zip(self.constraints.keys(), values)}

    def get_matching_dst(self, src_filename: str, format_dico: Dict[str, Any]) -> str:
        """Returns the formated dst_filename corresponding to the given src_filename
        and the current constraints, and according to self.src and self.dst.

        Args:
            src_filename (str): Source file's name.
            format_dico (Dict[str, Any]): Dictionnary containing the keys and values
                to format the dst filename.

        Returns:
            str: Formated destination filename

        Example:
            >>> extr = FTPDir(
                session={"host": "toto.meteo.fr"},
                src="/my/remote/{year}/(?P<basename>.\\w+.txt)",
                dst="my_dir/{year}_{basename}",
                constraints={"date": [2021]},
            )
            >>> extr.get_matching_dst("/my/remote/2021/file1.txt", {"year":2021})
            "my_dir/2021_file1.txt"
        """
        reg = re.compile(self.src.format(**format_dico))
        match = reg.match(src_filename)
        dico = dict()
        if not bool(match):
            dico = {gn: None for gn in reg.groupindex}
        else:
            dico = {gn: match.group(gn) for gn in reg.groupindex}
        dico.update(format_dico)
        return self.dst.format(**dico)

    @property
    def files(self) -> List[Tuple[str, str]]:
        """Property that gives the list of the files found in the FTP session that
        corresponds to the self.src and self.constraints.

        Returns:
            List[Tuple[str, str]]: List of files to get. Each element of
            the list is a tuple containing the source file's name and the destination
            file's name.
        """
        if self._files is not None:
            return self._files
        self._files = []
        LOGGER.debug("Starting to find files.")
        for dico in self.get_constraints_combinations():
            # formatting the directory's name with the constraints
            LOGGER.debug(f"Current constraint dico : {dico}")
            format_src = self.src.format(**dico)
            LOGGER.debug(f"Formated src : {format_src}")
            sources = ["."]
            # finding all source matching the src_dirname pattern by iteration
            for pattern in format_src.split("/"):
                LOGGER.debug(f"Finding pattern {pattern} in {sources}")
                sources = self.session.find_pattern(pattern, sources)
            LOGGER.debug(f"Final sources found: {sources} with {format_src}")
            self._files += [(src, self.get_matching_dst(src, dico)) for src in sources]
        LOGGER.debug(f"Final files : {self._files}")
        return self._files

    def to_ftp_extractor(self) -> FTPFiles:
        """Short method for retruning the equivalent FTPFiles.

        Returns:
            FTPFiles: FTPFiles equivalent to the given attributes.
        """
        return FTPFiles(
            session=self.session, files=self.files, n_workers=self.n_workers,
        )

    def run(self) -> bool:
        """Main method to get all self.files.

        Returns:
            bool: Whether the extraction is alright or not.
        """
        return self.to_ftp_extractor().run()
