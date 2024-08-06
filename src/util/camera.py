from panda3d.core import WindowProperties, NodePath
from direct.task import Task
import src.globals.visorview_globals as globals

RELATIVE_CAMERA_TASK_PRIORITY = 2                  # Camera reset must be higher so it runs last
DEFAULT_CAMERA_TASK_PRIORITY = 1                   # Therefore, use this for anything else.
RELATIVE_CAMERA_TASK_NAME = 'relative_camera_task' 
ROTATE_TASK_NAME = 'camera_rotate_task'
PAN_TASK_NAME = 'camera_pan_task'
ZOOM_TASK_NAME = 'camera_zoom_task'
CAMERA_START_POS = (0,-20,0)

class Camera(NodePath):
    """A NodePath that is parented to the Panda3D camera and implements mouse control."""
    
    def __init__(self) -> None:
        """Disables the default camera controls, moves the camera to its default position, reparents the camera, and enables mouse input."""
        super().__init__("camera_node")

        self.window_properties = WindowProperties()
        self.enabled = True
        # Disable default p3d camera because we're handling it ourselves.
        base.disable_mouse()     
        self.enable()

        camera.reparent_to(self)
        camera.set_pos(CAMERA_START_POS)
        self.reparent_to(render)

    def enable(self):
        """Accept mouse input events for controlling the camera."""
        base.accept("mouse2", self.enable_rotate_control)
        base.accept("mouse2-up", self.disable_rotate_control)
        base.accept("mouse3", self.enable_zoom_control)
        base.accept("mouse3-up", self.disable_zoom_control)
        base.accept("mouse1", self.enable_pan_control)
        base.accept("mouse1-up", self.disable_pan_control)

    def disable(self):
        """Stop accepting mouse input events for controlling the camera and disable any ongoing camera tasks."""
        base.ignore("mouse2")
        base.ignore("mouse2-up")
        base.ignore("mouse3")
        base.ignore("mouse3-up")
        base.ignore("mouse1")
        base.ignore("mouse1-up")
        self.end_controls()

    def reset_position(self):
        """Reset the camera and parent node to their default positions as defined in visorview_globals.py."""
        self.set_pos_hpr(*globals.DEFAULT_CAMERA_NODE_POS, 0, 0, 0)
        camera.set_pos(globals.DEFAULT_CAMERA_POS)

    def get_mouse_distance_from_center(self) -> set:
        """Function that gets the mouse's distance from the center, represented as as a float in the range (-1, 1). For odd window sizes, the center pixel is rounded down.

        :rtype: set
        :return: A set S where S[0] is x and S[1] is y
        """
        props = base.win.get_properties()
        window_size_x = props.get_x_size()
        window_size_y = props.get_y_size()
        # get distance mouse has moved. odd numbers round down
        pointer = base.win.get_pointer(0)
        mouse_x = pointer.get_x()
        mouse_y = pointer.get_y()
        center_x = window_size_x // 2
        center_y = window_size_y // 2
        change_in_x = (mouse_x - center_x) / center_x
        change_in_y = -(mouse_y - center_y) / center_y

        return (change_in_x, change_in_y)
    
    def move_mouse_to_center(self):
        """Function that moves the mouse pointer to the center of the ShowBase window."""
        props = base.win.get_properties()
        window_size_x = props.get_x_size()
        window_size_y = props.get_y_size()
        base.win.move_pointer(0,
                            window_size_x // 2,
                            window_size_y // 2)


    def enable_relative_mouse(self):
        """Starts the task that enables relative mouse mode and hides the cursor. Does nothing if already running."""
        if taskMgr.hasTaskNamed(RELATIVE_CAMERA_TASK_NAME):
            # already running
            return
        self.window_properties.set_cursor_hidden(True)
        base.win.request_properties(self.window_properties)
        self.move_mouse_to_center()
        taskMgr.add(self.relative_camera_task, 
                    RELATIVE_CAMERA_TASK_NAME, 
                    priority=RELATIVE_CAMERA_TASK_PRIORITY)
        
    def disable_relative_mouse(self):
        """Disables the task that enable relative mouse mode and unhides the cursor."""
        self.window_properties.set_cursor_hidden(False)
        base.win.request_properties(self.window_properties)
        while taskMgr.hasTaskNamed(RELATIVE_CAMERA_TASK_NAME):
            taskMgr.remove(RELATIVE_CAMERA_TASK_NAME)

    def relative_camera_task(self, task):
        """Task that resets the camera to the center. It should be run with a higher (asin, the actual number) priority so that it runs last in the chain."""
        self.move_mouse_to_center()
        return Task.cont

    def enable_rotate_control(self):
        """Starts the task that enables rotational control of the camera. Does nothing if already running."""
        if taskMgr.hasTaskNamed(RELATIVE_CAMERA_TASK_NAME):
            # some other camera task is already running
            return
        self.enable_relative_mouse()
        taskMgr.add(self.camera_rotate_task, 
                    ROTATE_TASK_NAME, 
                    priority=DEFAULT_CAMERA_TASK_PRIORITY)

    def disable_rotate_control(self):
        """Disables the task that enables rotational control of the camera."""
        if not taskMgr.hasTaskNamed(ROTATE_TASK_NAME):
            # we're not running
            return
        # Revert to normal mode:
        while taskMgr.hasTaskNamed(ROTATE_TASK_NAME):
            taskMgr.remove(ROTATE_TASK_NAME)
        self.disable_relative_mouse()

    def camera_rotate_task(self, task):
        """Task that rotates the camera based on the mouse pointer's distance from the center of the ShowBase window."""
        distances = self.get_mouse_distance_from_center()
        change_in_x = distances[0]
        change_in_y = distances[1]
        props = base.win.get_properties()
        window_size_x = props.get_x_size()
        window_size_y = props.get_y_size()
        
        # TODO: mess with these values, add sensitivity?
        camera_h = self.get_h()
        camera_p = self.get_p()
        camera_r = self.get_r()
        new_h = camera_h - (change_in_x * window_size_x/10)
        new_p = camera_p + (change_in_y * window_size_y/10)
        new_r = camera_r

        self.set_hpr(new_h, new_p, new_r)
        return Task.cont
    
    # Function called to activate zoom controls.
    def enable_zoom_control(self):
        """Starts the task that enables zoom control of the camera. Does nothing if already running."""
        if taskMgr.hasTaskNamed(RELATIVE_CAMERA_TASK_NAME):
            # some other camera task is already running
            return
        self.enable_relative_mouse()
        taskMgr.add(self.camera_zoom_task, 
                              ZOOM_TASK_NAME, 
                              priority=DEFAULT_CAMERA_TASK_PRIORITY)

    # Function called to disable zoom controls.
    def disable_zoom_control(self):
        """Disables the task that enables zoom control of the camera."""
        if not taskMgr.hasTaskNamed(ZOOM_TASK_NAME):
            # we're not running
            return
        # Revert to normal mode:
        while taskMgr.hasTaskNamed(ZOOM_TASK_NAME):
            taskMgr.remove(ZOOM_TASK_NAME)
        self.disable_relative_mouse()

    def camera_zoom_task(self, task):
        """Task that zooms the camera based on the mouse pointer's distance from the center of the ShowBase window."""
        distances = self.get_mouse_distance_from_center()
        change_in_y = distances[1]

        # we're gonna do some math to move in the direction the camera is facing
        camera_h = camera.get_h()
        camera_p = camera.get_p()
        camera_r = camera.get_r()

        # TODO: mess with these values, add sensitivity?
        forwardVec = camera.get_quat().get_forward()
        camera.setPos(camera.get_pos() + forwardVec*change_in_y*5.0)
        return Task.cont
    
    # Function called to activate pan controls.
    def enable_pan_control(self):
        """Starts the task that enables panning control of the camera. Does nothing if already running."""
        if taskMgr.hasTaskNamed(RELATIVE_CAMERA_TASK_NAME):
            # some other camera task is already running
            return
        self.enable_relative_mouse()
        taskMgr.add(self.camera_pan_task,
                    PAN_TASK_NAME, 
                    priority=DEFAULT_CAMERA_TASK_PRIORITY)

    # Function called to activate pan controls.
    def disable_pan_control(self):
        """Disables the task that enables panning control of the camera."""
        if not taskMgr.hasTaskNamed(PAN_TASK_NAME):
            # we're not running
            return
        # Revert to normal mode:
        while taskMgr.hasTaskNamed(PAN_TASK_NAME):
            taskMgr.remove(PAN_TASK_NAME)
        self.disable_relative_mouse()

    def camera_pan_task(self, task):
        """Task that pans the camera based on the mouse pointer's distance from the center of the ShowBase window."""
        distances = self.get_mouse_distance_from_center()
        change_in_x = distances[0]
        change_in_y = distances[1]
        right_vec = camera.get_quat().get_right()
        up_vec = camera.get_quat().get_up()
        camera.setPos(camera.get_pos() + right_vec*change_in_x*5.0)
        camera.setPos(camera.get_pos() + up_vec*change_in_y*5.0)
        return Task.cont

    def end_controls(self):
        """Function that stops all running camera control tasks."""
        self.disable_pan_control()
        self.disable_rotate_control()
        self.disable_zoom_control()
        self.disable_relative_mouse()