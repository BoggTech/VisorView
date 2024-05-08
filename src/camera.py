from panda3d.core import WindowProperties
from direct.task import Task

RELATIVE_CAMERA_TASK_PRIORITY = 2                  # Camera reset must be higher so it runs last
DEFAULT_CAMERA_TASK_PRIORITY = 1                   # Therefore, use this for anything else.
RELATIVE_CAMERA_TASK_NAME = 'relative_camera_task' 
ROTATE_TASK_NAME = 'camera_rotate_task'
PAN_TASK_NAME = 'camera_pan_task'
ZOOM_TASK_NAME = 'camera_zoom_task'

# Class that controls the camera.
class Camera:
    def __init__(self) -> None:
        self.window_properties = WindowProperties()
        self.enabled = True
        # Disable default p3d camera because we're handling it ourselves.
        base.disableMouse()     
        self.enable()

    # Enable camera controls
    def enable(self): 
        base.accept("mouse2", self.enable_rotate_control)
        base.accept("mouse2-up", self.disable_rotate_control)
        base.accept("mouse3", self.enable_zoom_control)
        base.accept("mouse3-up", self.disable_zoom_control)
        base.accept("mouse1", self.enable_pan_control)
        base.accept("mouse1-up", self.disable_pan_control)

    # Disable camera controls + end any ongoing actions
    def disable(self):
        base.ignore("mouse2")
        base.ignore("mouse2-up")
        base.ignore("mouse3")
        base.ignore("mouse3-up")
        base.ignore("mouse1")
        base.ignore("mouse1-up")
        self.end_controls()

    # Function that gets the mouse's distance from the center, represented as an
    # integer in the range (-1, 1). Returns a set where s[0] = x and s[1] = y
    def get_mouse_distance_from_center(self) -> set:
        change_in_x = 0
        change_in_y = 0
        props = base.win.getProperties()
        window_size_x = props.getXSize()
        window_size_y = props.getYSize()
        if base.mouseWatcherNode.hasMouse():
            # get distance mouse has moved. odd numbers round down
            pointer = base.win.getPointer(0)
            mouse_x = pointer.getX()
            mouse_y = pointer.getY()
            center_x = window_size_x // 2
            center_y = window_size_y // 2
            change_in_x = (mouse_x - center_x) / center_x
            change_in_y = -(mouse_y - center_y) / center_y

        return (change_in_x, change_in_y)
    
    def move_mouse_to_center(self):
        props = base.win.getProperties()
        window_size_x = props.getXSize()
        window_size_y = props.getYSize()
        if base.mouseWatcherNode.hasMouse():
            base.win.movePointer(0,
                                window_size_x // 2,
                                window_size_y // 2)


    # Panda3D default relative positioning is broken. Use this to enable relative positioning.
    def enable_relative_mouse(self):
        if taskMgr.hasTaskNamed(RELATIVE_CAMERA_TASK_NAME):
            # already running
            return
        base.win.requestProperties(self.window_properties)
        self.move_mouse_to_center()
        taskMgr.add(self.relative_camera_task, 
                    RELATIVE_CAMERA_TASK_NAME, 
                    priority=RELATIVE_CAMERA_TASK_PRIORITY)
        
    def disable_relative_mouse(self):
        self.window_properties.setCursorHidden(False)
        base.win.requestProperties(self.window_properties)
        while taskMgr.hasTaskNamed(RELATIVE_CAMERA_TASK_NAME):
            taskMgr.remove(RELATIVE_CAMERA_TASK_NAME)

    # Task that resets the camera to the center. It should be run with a
    # higher (asin, the actual number) priority so that it runs last in the chain. 
    def relative_camera_task(self, task):
        self.move_mouse_to_center()
        return Task.cont

    # Function called to activate rotate controls.
    def enable_rotate_control(self):
        if taskMgr.hasTaskNamed(RELATIVE_CAMERA_TASK_NAME):
            # some other camera task is already running
            return
        self.enable_relative_mouse()
        taskMgr.add(self.camera_rotate_task, 
                    ROTATE_TASK_NAME, 
                    priority=DEFAULT_CAMERA_TASK_PRIORITY)

    # Function called to disable rotate controls.
    def disable_rotate_control(self):
        # Revert to normal mode:
        while taskMgr.hasTaskNamed(ROTATE_TASK_NAME):
            taskMgr.remove(ROTATE_TASK_NAME)
        self.disable_relative_mouse()

    def camera_rotate_task(self, task):
        distances = self.get_mouse_distance_from_center()
        change_in_x = distances[0]
        change_in_y = distances[1]
        props = base.win.getProperties()
        window_size_x = props.getXSize()
        window_size_y = props.getYSize()
        
        # TODO: mess with these values, add sensitivity?
        camera_h = camera.getH()
        camera_p = camera.getP()
        camera_r = camera.getR()
        new_h = camera_h - (change_in_x * window_size_x/10)
        new_p = camera_p + (change_in_y * window_size_y/10)
        new_r = camera_r

        camera.setHpr(new_h, new_p, new_r)
        return Task.cont
    
    # Function called to activate zoom controls.
    def enable_zoom_control(self):
        if taskMgr.hasTaskNamed(RELATIVE_CAMERA_TASK_NAME):
            # some other camera task is already running
            return
        self.enable_relative_mouse()
        taskMgr.add(self.camera_zoom_task, 
                              ZOOM_TASK_NAME, 
                              priority=DEFAULT_CAMERA_TASK_PRIORITY)

    # Function called to disable zoom controls.
    def disable_zoom_control(self):
        # Revert to normal mode:
        while taskMgr.hasTaskNamed(ZOOM_TASK_NAME):
            taskMgr.remove(ZOOM_TASK_NAME)
        self.disable_relative_mouse()

    def camera_zoom_task(self, task):
        distances = self.get_mouse_distance_from_center()
        change_in_y = distances[1]

        # we're gonna do some math to move in the direction the camera is facing
        camera_h = camera.getH()
        camera_p = camera.getP()
        camera_r = camera.getR()

        # TODO: mess with these values, add sensitivity?
        forwardVec = camera.getQuat().getForward()
        camera.setPos(camera.getPos() + forwardVec*change_in_y*5.0)
        return Task.cont
    
    # Function called to activate pan controls.
    def enable_pan_control(self):
        if taskMgr.hasTaskNamed(RELATIVE_CAMERA_TASK_NAME):
            # some other camera task is already running
            return
        self.enable_relative_mouse()
        taskMgr.add(self.camera_pan_task,
                    PAN_TASK_NAME, 
                    priority=DEFAULT_CAMERA_TASK_PRIORITY)

    # Function called to activate pan controls.
    def disable_pan_control(self):
        # Revert to normal mode:
        while taskMgr.hasTaskNamed(PAN_TASK_NAME):
            taskMgr.remove(PAN_TASK_NAME)
        self.disable_relative_mouse()

    def camera_pan_task(self, task):
        distances = self.get_mouse_distance_from_center()
        change_in_x = distances[0]
        change_in_y = distances[1]
        rightVec = camera.getQuat().getRight()
        upVec = camera.getQuat().getUp()
        camera.setPos(camera.getPos() + rightVec*change_in_x*5.0)
        camera.setPos(camera.getPos() + upVec*change_in_y*5.0)
        return Task.cont

    # Function that stops all control modes actively running
    def end_controls(self):
        self.disable_pan_control()
        self.disable_rotate_control()
        self.disable_zoom_control()
        self.disable_relative_mouse()
