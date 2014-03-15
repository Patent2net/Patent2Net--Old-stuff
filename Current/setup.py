# -*- coding: utf-8 -*-

from distutils.core import setup
import sys
import glob
import py2exe

setup(
    options = {
            "py2exe":{"dll_excludes": ["MSVCP90.dll", "HID.DLL", "w9xpopen.exe", "libpng16-vc90-mt.dll", 'freetype-2.5-vc90-mt.dll'],
        }
    },
    console = ['OpsGather-PatentList.py', 'OpsGather-BiblioPatents.py', 'OpsGather-Claims.py','PatentsToNet.py']
)

if sys.platform == "win32": # For py2exe.
    sys.path.append("C:\\Program Files (x86)\\Microsoft Visual Studio 8\\VC\\redist\\x86\\Microsoft.VC90.CRT")
    base_path = ""
    data_files = [("Microsoft.VC90.CRT", glob.glob(r"C:\Program Files (x86)\Microsoft Visual Studio 8\VC\redist\x86\Microsoft.VC90.CRT\*.*"))]
