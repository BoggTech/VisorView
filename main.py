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
result = askquestion(title="Visorview",
                    message="Would you like to specify the location of your installed game files?")

if not result == 'yes':
    sys.exit(0)

phase_files = ("3", "3.5", "4")
vfs = VirtualFileSystem.get_global_ptr()

while True:
    phase_file_dir = Filename.from_os_specific(askdirectory(title='Select Folder'))
    for canon in phase_files:
        is_success = vfs.mount(phase_file_dir / Filename("phase_" + canon + ".mf"), ".", VirtualFileSystem.MF_read_only)
        if not is_success:
            break
    if not is_success:
        result = askquestion(title="Visorview",
                    message="Failed to locate file 'phase_" + canon + ".mf'. \n" +
                             "Would you like to select a different folder?")
        if not result == 'yes':
            sys.exit(0)
    else:
        break


print(phase_file_dir)

# Run main program
import src.visorview