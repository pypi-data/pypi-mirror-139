"""Contains high-level object representing the whole of an IOS Shell file."""
from dataclasses import dataclass
import datetime
from typing import Any, Dict, List, Optional, Union

from . import parsing, sections


@dataclass
class ShellFile:
    """Represents the contents of an IOS Shell file."""

    filename: str
    """The file name the data originally came from.
    Useful for debugging."""
    modified_date: datetime.datetime
    header_version: sections.Version
    file: sections.FileInfo
    administration: sections.Administration
    location: sections.Location
    instrument: Optional[sections.Instrument]
    history: Optional[sections.History]
    calibration: Optional[sections.Calibration]
    deployment: Optional[sections.Deployment]
    recovery: Optional[sections.Recovery]
    raw: Optional[sections.Raw]
    """The contents of the section starting with \\*RAW, not the raw file contents."""
    comments: str
    data: Union[List[List[Any]], str]
    """Data is assumed to be processed if it is a List[List[Any]],
    and unprocessed if it is a str.

    Some data has been known to contain dates or arbitrary strings, so raw numpy arrays
    are difficult to make work."""

    @classmethod
    def fromfile(cls, filename, process_data=True):  # pragma: no mutate
        """Construct a ShellFile object from the contents of a file."""
        with open(filename, "r", encoding="ASCII", errors="ignore") as f:
            contents = f.read()
        try:
            return ShellFile.fromcontents(contents, process_data, filename=filename)
        except ValueError as e:
            if filename in str(e):
                raise
            exc = ValueError(f"Error in {filename}: {e}")
            exc.__traceback__ = e.__traceback__
            raise exc from None

    @classmethod
    def fromcontents(cls, contents, process_data=True, filename="bare string"):
        """Construct a ShellFile object from the contents of a string."""
        header, raw_data = contents.split("*END OF HEADER", 1)  # pragma: no mutate
        header_lines = header.splitlines()
        header_lines.append("*END OF HEADER")
        while "" in header_lines:
            header_lines.remove("")
        modified_date, rest = parsing.get_modified_date(header_lines)
        header_version, rest = parsing.get_header_version(rest)
        # begin named sections
        # sections may appear out of order
        (
            file,
            administration,
            location,
            instrument,
            history,
            calibration,
            deployment,
            recovery,
            comments,
            raw,
        ) = (
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        )
        line = rest[0]
        while not line.startswith("*END OF HEADER"):
            if line.startswith("*FILE"):
                if file is not None:
                    raise ValueError("There should only be one file section")
                file, rest = parsing.get_file(rest)
            elif line.startswith("*ADMINISTRATION"):
                if administration is not None:
                    raise ValueError("There should only be one administration section")
                administration, rest = parsing.get_administration(rest)
            elif line.startswith("*LOCATION"):
                if location is not None:
                    raise ValueError("There should only be one location section")
                location, rest = parsing.get_location(rest)
            elif line.startswith("*INSTRUMENT"):
                if instrument is not None:
                    raise ValueError("There should only be one instrument section")
                instrument, rest = parsing.get_instrument(rest)
            elif line.startswith("*HISTORY"):
                if history is not None:
                    raise ValueError("There should only be one history section")
                history, rest = parsing.get_history(rest)
            elif line.startswith("*COMMENTS"):
                if comments is not None:
                    raise ValueError("There should only be one comments section")
                comments, rest = parsing.get_comments(rest)
            elif line.startswith("*CALIBRATION"):
                if calibration is not None:
                    raise ValueError("There should only be one calibration section")
                calibration, rest = parsing.get_calibration(rest)
            elif line.startswith("*RAW"):
                if raw is not None:
                    raise ValueError("There should only be one raw section")
                raw, rest = parsing.get_raw(rest)
            elif line.startswith("*DEPLOYMENT"):
                if deployment is not None:
                    raise ValueError("There should only be one deployment section")
                deployment, rest = parsing.get_deployment(rest)
            elif line.startswith("*RECOVERY"):
                if recovery is not None:
                    raise ValueError("There should only be one recovery section")
                recovery, rest = parsing.get_recovery(rest)
            else:
                raise ValueError(f"Unknown section: {line}")
            line = rest[0]
        # end named sections
        # check for required sections
        if file is None:
            raise ValueError("*FILE section must be present")
        if administration is None:
            raise ValueError("*ADMINISTRATION section must be present")
        if location is None:
            raise ValueError("*LOCATION section must be present")
        info = ShellFile(
            filename=filename,
            modified_date=modified_date,
            header_version=header_version,
            file=file,
            administration=administration,
            location=location,
            instrument=instrument,
            history=history,
            calibration=calibration,
            deployment=deployment,
            recovery=recovery,
            raw=raw,
            comments=comments if comments is not None else "",
            data=raw_data,
        )
        if process_data:
            info.process_data()
        return info

    def get_location(self) -> Dict[str, float]:
        """Produce a conventent dict of the longitude and latitude in the file."""
        return {
            "longitude": self.location.longitude,
            "latitude": self.location.latitude,
        }

    def get_time(self) -> datetime.datetime:
        """A time to associate the contents with.

        Typically the START TIME field of \\*FILE
        """
        if self.file.start_time != datetime.datetime.min:
            return self.file.start_time
        elif self.file.end_time != datetime.datetime.min:
            return self.file.end_time
        else:
            raise ValueError("No valid time found")

    def data_is_processed(self) -> bool:
        """Determine whether or not the data in the file has already been processed."""
        return not isinstance(self.data, str)

    def process_data(self):
        """Perform the processing of the data."""
        if self.data_is_processed():
            return
        # assertion to satisfy (optional) type checking
        assert isinstance(self.data, str)
        try:
            data, _ = parsing.get_data(
                self.data, self.file.format, self.file.number_of_records
            )
            self.data = data
        except Exception as e:
            exc = ValueError(f"Error processing data in {self.filename}: {e}")
            exc.__traceback__ = e.__traceback__
            raise exc from None
