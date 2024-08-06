import sys
from os.path import expanduser
from platform import system

# Load config - must happen before any other Panda3D import
from panda3d.core import loadPrcFile

loadPrcFile("VisorConfig.prc")

from panda3d.core import VirtualFileSystem
from panda3d.core import Multifile
from panda3d.core import Filename
from tkinter.messagebox import askquestion
from tkinter.filedialog import askdirectory

# Mount phase files
user_system = system()
home_dir = Filename(expanduser("~"))
DEFAULT_INSTALL_PATHS = {
    "Linux": home_dir / Filename(".var/app/com.toontownrewritten.Launcher/data"),
    "Windows": Filename("/c/Program Files (x86)/Toontown Rewritten"),
    "Darwin": home_dir / Filename("Library/Application Support/Toontown Rewritten")
}
default_path = DEFAULT_INSTALL_PATHS[user_system]

PHASE_FILES = ("3.5", "3", "4", "5", "5.5", "6", "7", "8", "9", "10", "11", "12", "13", "14")
vfs = VirtualFileSystem.get_global_ptr()

phase_file_dir = default_path
while True:
    for canon in PHASE_FILES:
        is_success = vfs.mount(phase_file_dir / Filename("phase_" + canon + ".mf"), ".", VirtualFileSystem.MF_read_only)
        if not is_success:
            break
    if not is_success:
        result = askquestion(title="Visorview",
                             message="Failed to locate one or more required phase files in '" +
                                     phase_file_dir.to_os_specific() +
                                     "'.\nWould you like to select your Toontown Rewritten install folder manually?")
        if not result == 'yes':
            sys.exit(0)
        phase_file_dir = Filename.from_os_specific(askdirectory(title='Select Folder'))
    else:
        break

print(phase_file_dir)

# Run main program
import src.visorview
