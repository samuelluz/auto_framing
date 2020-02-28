import sys
from cx_Freeze import setup, Executable


base = None
if sys.platform == "win32":
    base = "Win32GUI"
executables = [
        Executable("app.py", base=base)
]

buildOptions = dict(
        packages = [],
        includes = [],
        include_files = [],
        excludes = []
)

setup(
    name = "MolduraAutomatica",
    version = "1.0.0",
    description = "moldura automática",
    options = dict(build_exe = buildOptions),
    executables = executables
 )