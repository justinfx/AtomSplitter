@echo off
rem = """

python -x "%~f0"
goto endofPython """

"""
Copyright (c) 2010 cmiVFX.com <info@cmivfx.com>

This file is part of AtomSplitter.

AtomSplitter is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

AtomSplitter is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with AtomSplitter.  If not, see <http://www.gnu.org/licenses/>.

Written by: Justin Israel
      justinisrael@gmail.com
      justinfx.com

"""

from distutils.core import setup
import py2exe
import shutil
import sys, os, glob

def find_data_files(source,target,patterns):
    """Locates the specified data-files and returns the matches
    in a data_files compatible format.

    source is the root of the source data tree.
        Use '' or '.' for current directory.
    target is the root of the target data tree.
        Use '' or '.' for the distribution directory.
    patterns is a sequence of glob-patterns for the
        files you want to copy.
    """
    if glob.has_magic(source) or glob.has_magic(target):
        raise ValueError("Magic not allowed in src, target")
    ret = {}
    for pattern in patterns:
        pattern = os.path.join(source,pattern)
        for filename in glob.glob(pattern):
            if os.path.isfile(filename):
                targetpath = os.path.join(target,os.path.relpath(filename,source))
                path = os.path.dirname(targetpath)
                ret.setdefault(path,[]).append(filename)
    return sorted(ret.items())

sys.argv += ['py2exe', '-b1', '-d./dist']

myData = []
myData.extend( find_data_files('', '', ['qt.conf']) )

setup(
    # use "console = " for console-based apps
    windows=[{'script':"../AtomSplitter.py", 'icon_resources':[(1,'icon.ico')]}],
    data_files = myData,
    zipfile=None,
    version="1.6.2",
    name='AtomSplitter',
    author='cmivfx.com / Justin Israel (justinfx.com)',
    options={ "py2exe": { "includes" : ['sip','PyQt4.QtCore','PyQt4.QtGui','PyQt4.QtNetwork','PyQt4.QtWebKit'] } }
 
    )

shutil.rmtree('build')
os.remove('dist/w9xpopen.exe')
rem = """
:endofPython """