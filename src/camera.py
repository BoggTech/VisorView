from pandac.PandaModules import WindowProperties
from direct.task import Task

# Class that controls the camera. Takes in base as an argument
class Camera:
    def __init__(self, base, camera) -> None:
        self.camera = camera
        self.base = base
        self.window_properties = WindowProperties()

        self.enabled = True

        # disable default camera
        self.base.disableMouse()

        self.last_mouse_x = 0
        self.last_mouse_y = 0

        self.base.accept("mouse1", self.enable_pan_control)
        self.base.accept("mouse1-up", self.disable_pan_control)

    # Function called when mouse is held down and panning is active.
    def enable_pan_control(self):
        # I'm inclined to use relative mode here but it doesn't work.
        self.window_properties.setCursorHidden(True)
        self.base.win.requestProperties(self.window_properties)

        props = self.base.win.getProperties()
        window_size_x = props.getXSize()
        window_size_y = props.getYSize()
        # move mouse to center; relative positioning
        if self.base.mouseWatcherNode.hasMouse():
            self.base.win.movePointer(0,
                                window_size_x // 2,
                                window_size_y // 2)
        
        # we want this to run on the next frame, otherwise the mouse position wont
        # update in time and the camera snaps weirdly. domethodlater with a delay 
        # of 0 seems to work best, however, TODO look at this again just in case 
        # there's a more elegant solution.
        taskMgr.doMethodLater(0, self.camera_pan_task, 'camera_pan_task')

    def disable_pan_control(self):
        # Revert to normal mode:
        self.window_properties.setCursorHidden(False)
        self.base.win.requestProperties(self.window_properties)
        taskMgr.remove('camera_pan_task')

    def camera_pan_task(self, task):
        change_in_x = 0
        change_in_y = 0
        props = self.base.win.getProperties()
        window_size_x = props.getXSize()
        window_size_y = props.getYSize()

        if self.base.mouseWatcherNode.hasMouse():
            # get distance mouse has moved
            change_in_x = self.base.mouseWatcherNode.getMouseX()
            change_in_y = self.base.mouseWatcherNode.getMouseY()

            # the center of the window in terms of mouse x/y can use decimal values. the actual position can't. we need to account
            # for this when the window has an odd length, because we can never attain the true center position.
            if window_size_x % 2 == 1:
                odd_difference = .5 / (window_size_x / 2)
                change_in_x -= odd_difference
            if window_size_y % 2 == 1:
                odd_difference = .5 / (window_size_y / 2)
                change_in_y -= odd_difference
                print(change_in_y)

            # move mouse back to center
            props = self.base.win.getProperties()
            self.base.win.movePointer(0,
                                window_size_x // 2,
                                window_size_y // 2)

        camera_h = self.camera.getH()
        camera_p = self.camera.getP()
        camera_r = self.camera.getR()

        new_h = camera_h - (change_in_x * window_size_x/10)
        new_p = camera_p + (change_in_y * window_size_y/10)
        new_r = camera_r

        self.camera.setHpr(new_h, new_p, new_r)
        return Task.cont