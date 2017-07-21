# -*- coding: utf-8 -*-

import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os"],
    "excludes": ["tkinter", "unittest"],
    "include_files": ["Data", "Graphics"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base, extension = None, ""
if sys.platform == "win32":
    base = "Win32GUI"
    extension = ".exe"

setup(name = "Virtuosi",
      version = "0.1",
      description = u"Seja um virtuoso tocando músicas em seu violino",
      options = {"build_exe": build_exe_options},
      executables = [Executable("main.py", base=base, targetName="Virtuosi" + extension)])
