import sys

# Load config - must happen before any other Panda3D import
from panda3d.core import loadPrcFile
loadPrcFile("VisorConfig.prc")

from panda3d.core import VirtualFileSystem
from panda3d.core import Multifile
from panda3d.core import Filename
from tkinter.messagebox import askquestion
from tkinter.filedialog import askdirectory

# Mount phase files
# TODO: support for other platforms/changing search folder - windows only for now just for testing

result = askquestion(title="Visorview",
                    message="Would you like to specify the location of your installed game files?")

if result == 'yes':
    phase_file_dir = Filename.fromOsSpecific(askdirectory(title='Select Folder'))
else:
    sys.exit(0)
phase_files = ("3.5", "3", "4", "5", "5.5", "6", "7", "8", "9", "10", "11", "12", "13", "14")

vfs = VirtualFileSystem.get_global_ptr()
for canon in phase_files:
    vfs.mount(phase_file_dir / Filename("phase_" + canon + ".mf"), ".", VirtualFileSystem.MF_read_only)

print(phase_file_dir)

# Run main program
import src.visorview