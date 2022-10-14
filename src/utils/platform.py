import os
import sys

IS_POSIX = os.name == "posix"
SCRIPT_EXT = ".sh" if IS_POSIX else ".bat"
PLATFORM = sys.platform
