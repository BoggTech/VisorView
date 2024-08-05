# Launcher
import sys

# Mount phase files
# TODO: support for other platforms/changing search folder - windows only for now just for testing
from panda3d.core import VirtualFileSystem
from panda3d.core import Multifile
from panda3d.core import Filename

phase_file_dir = Filename('/c/Program Files (x86)/Toontown Rewritten')
phase_files = ("3.5", "3", "4", "5", "5.5", "6", "7", "8", "9", "10", "11", "12", "13", "14")

vfs = VirtualFileSystem.get_global_ptr()
for canon in phase_files:
    vfs.mount(phase_file_dir / Filename("phase_" + canon + ".mf"), ".", VirtualFileSystem.MF_read_only)

# Load config
from panda3d.core import loadPrcFile
loadPrcFile("VisorConfig.prc")

# Run main program
import src.visorview