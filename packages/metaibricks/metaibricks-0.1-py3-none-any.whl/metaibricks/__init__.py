"""
Meteopy package : fake package to illustrate the organisation of a
python project.
"""
from metaibricks.settings import CLI, Logger, Settings
from metaibricks.extraction import FTPSession, FTPFiles, FTPDir
from metaibricks.pipeline import Pipeline

__version__ = "0.1"

__all__ = [
    "__version__",
    "CLI",
    "Logger",
    "Settings",
    "FTPSession",
    "FTPFiles",
    "FTPDir",
    "Pipeline",
]
