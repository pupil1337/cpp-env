import os
import subprocess
import re
import sys
from enum import Enum

class ANSI(Enum):
    """
    Enum class for adding ansi colorcodes directly into strings.
    Automatically converts values to strings representing their
    internal value, or an empty string in a non-colorized scope.
    """

    RESET = "\x1b[0m"

    BOLD = "\x1b[1m"
    ITALIC = "\x1b[3m"
    UNDERLINE = "\x1b[4m"
    STRIKETHROUGH = "\x1b[9m"
    REGULAR = "\x1b[22;23;24;29m"

    BLACK = "\x1b[30m"
    RED = "\x1b[31m"
    GREEN = "\x1b[32m"
    YELLOW = "\x1b[33m"
    BLUE = "\x1b[34m"
    MAGENTA = "\x1b[35m"
    CYAN = "\x1b[36m"
    WHITE = "\x1b[37m"

    PURPLE = "\x1b[38;5;93m"
    PINK = "\x1b[38;5;206m"
    ORANGE = "\x1b[38;5;214m"
    GRAY = "\x1b[38;5;244m"

    def __str__(self) -> str:
        global _colorize
        return str(self.value) if _colorize else ""

def print_warning(*values: object) -> None:
    """Prints a warning message with formatting."""
    print(f"{ANSI.YELLOW}{ANSI.BOLD}WARNING:{ANSI.REGULAR}", *values, ANSI.RESET, file=sys.stderr)


def using_gcc(env):
    return "gcc" in os.path.basename(env["CC"])


def using_clang(env):
    return "clang" in os.path.basename(env["CC"])


def using_emcc(env):
    return "emcc" in os.path.basename(env["CC"])


def get_compiler_version(env):
    """
    Returns a dictionary with various version information:

    - major, minor, patch: Version following semantic versioning system
    - metadata1, metadata2: Extra information
    - date: Date of the build
    """
    ret = {
        "major": -1,
        "minor": -1,
        "patch": -1,
        "metadata1": None,
        "metadata2": None,
        "date": None,
        "apple_major": -1,
        "apple_minor": -1,
        "apple_patch1": -1,
        "apple_patch2": -1,
        "apple_patch3": -1,
    }

    if not env.msvc:
        # Not using -dumpversion as some GCC distros only return major, and
        # Clang used to return hardcoded 4.2.1: # https://reviews.llvm.org/D56803
        try:
            version = (
                subprocess.check_output([env.subst(env["CXX"]), "--version"], shell=(os.name == "nt"))
                .strip()
                .decode("utf-8")
            )
        except (subprocess.CalledProcessError, OSError):
            print_warning("Couldn't parse CXX environment variable to infer compiler version.")
            return ret
    else:
        # TODO: Implement for MSVC
        return ret
    match = re.search(
        r"(?:(?<=version )|(?<=\) )|(?<=^))"
        r"(?P<major>\d+)"
        r"(?:\.(?P<minor>\d*))?"
        r"(?:\.(?P<patch>\d*))?"
        r"(?:-(?P<metadata1>[0-9a-zA-Z-]*))?"
        r"(?:\+(?P<metadata2>[0-9a-zA-Z-]*))?"
        r"(?: (?P<date>[0-9]{8}|[0-9]{6})(?![0-9a-zA-Z]))?",
        version,
    )
    if match is not None:
        for key, value in match.groupdict().items():
            if value is not None:
                ret[key] = value

    match_apple = re.search(
        r"(?:(?<=clang-)|(?<=\) )|(?<=^))"
        r"(?P<apple_major>\d+)"
        r"(?:\.(?P<apple_minor>\d*))?"
        r"(?:\.(?P<apple_patch1>\d*))?"
        r"(?:\.(?P<apple_patch2>\d*))?"
        r"(?:\.(?P<apple_patch3>\d*))?",
        version,
    )
    if match_apple is not None:
        for key, value in match_apple.groupdict().items():
            if value is not None:
                ret[key] = value

    # Transform semantic versioning to integers
    for key in [
        "major",
        "minor",
        "patch",
        "apple_major",
        "apple_minor",
        "apple_patch1",
        "apple_patch2",
        "apple_patch3",
    ]:
        ret[key] = int(ret[key] or -1)
    return ret
