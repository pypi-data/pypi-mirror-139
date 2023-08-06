from pydantic import Field

from metaibricks.base import ParallelTaskBase


class ExtractorBase(ParallelTaskBase):
    """Abstract class for defining an Extractor

    Inherits:
        ParallelTaskBase
    """

    kind: str = Field("Extractor", const=True)
