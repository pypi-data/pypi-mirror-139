import enum
import typing

class reduce_command:
    iaxis: int
    def __repr__(self) -> str: ...

class slice_mode(enum.Enum):
    shrink = enum.auto()
    crop = enum.auto()

@typing.overload
def shrink_and_rebin(
    iaxis: int, lower: float, upper: float, merge: int
) -> reduce_command: ...
@typing.overload
def shrink_and_rebin(lower: float, upper: float, merge: int) -> reduce_command: ...
@typing.overload
def crop_and_rebin(
    iaxis: int, lower: float, upper: float, merge: int
) -> reduce_command: ...
@typing.overload
def crop_and_rebin(lower: float, upper: float, merge: int) -> reduce_command: ...
@typing.overload
def slice_and_rebin(
    iaxis: int, begin: int, end: int, merge: int, mode: slice_mode = ...
) -> reduce_command: ...
@typing.overload
def slice_and_rebin(
    begin: int, end: int, merge: int, mode: slice_mode = ...
) -> reduce_command: ...
@typing.overload
def rebin(iaxis: int, merge: int) -> reduce_command: ...
@typing.overload
def rebin(merge: int) -> reduce_command: ...
@typing.overload
def shrink(iaxis: int, lower: int, upper: int) -> reduce_command: ...
@typing.overload
def shrink(lower: int, upper: int) -> reduce_command: ...
@typing.overload
def crop(iaxis: int, lower: float, upper: float) -> reduce_command: ...
@typing.overload
def crop(lower: float, upper: float) -> reduce_command: ...
@typing.overload
def slice(iaxis: int, begin: int, end: int, mode: slice_mode) -> reduce_command: ...
@typing.overload
def slice(begin: int, end: int, mode: slice_mode) -> reduce_command: ...
