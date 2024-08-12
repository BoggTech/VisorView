import src.globals.visorview_globals as visorview_globals

import os
from datetime import datetime
from panda3d.core import AntialiasAttrib
from panda3d.core import TextNode
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import *
from src.util.camera import Camera
from src.actors.actor_manager import ActorManager
from src.globals.actor_globals import ACTORS, COG_SET_NAMES


class VisorView(ShowBase):
    """ShowBase instance for VisorView."""

    def __init__(self):
        """Initializes the ShowBase as well as a number of local variables required by VisorView and accepts input events."""
        ShowBase.__init__(self)
        self.camera_controller = Camera()

        # initialize the gui
        self.animation_scroll_list = DirectScrolledList(
            incButton_pos=(-1, 0, -.1), incButton_text="DN", incButton_text_scale=0.1,
            incButton_borderWidth=(0.05, 0.05),
            decButton_pos=(-1, 0, .1), decButton_text="UP", decButton_text_scale=0.1,
            decButton_borderWidth=(0.05, 0.05),
            itemFrame_pos=(-.8, 0, 0.8), forceHeight=.11, numItemsVisible=15)
        self.animation_scroll_list.hide()
        self.available_animations = []
        self.is_animation_scroll = False
        self.is_pose_scroll = False
        self.is_scroll_visible = False

        # initialize our actor
        self.actors = ACTORS["supervisors"]
        self.cog_set_index = 0
        self.actor = ActorManager()
        self.actor.reparent_to(render)
        self.index = 0
        self.current_pose_part = None
        self.build_cog()

        self.reset_camera_pos()

        # we're initialized, time to accept input
        self.accept("space", self.cycle)
        self.accept("arrow_left", lambda: self.cycle(True))
        self.accept("arrow_right", lambda: self.cycle(False))
        self.accept("arrow_up", lambda: self.cycle(False, True))
        self.accept("arrow_down", lambda: self.cycle(True, True))
        self.accept("s", self.actor.toggle_shadow_visibility)
        self.accept("control-s", self.actor.toggle_skelecog)
        self.accept("control-b", self.actor.toggle_body_visibility)
        self.accept("control-h", self.actor.toggle_head_visibility)
        self.accept("1", lambda: self.switch_actor_set("supervisors"))
        self.accept("2", lambda: self.switch_actor_set("sellbots"))
        self.accept("3", lambda: self.switch_actor_set("cashbots"))
        self.accept("4", lambda: self.switch_actor_set("lawbots"))
        self.accept("5", lambda: self.switch_actor_set("bossbots"))
        self.accept("6", lambda: self.switch_actor_set("bosses"))
        self.accept("7", lambda: self.switch_actor_set("misc"))
        self.accept("a", self.toggle_animation_scroll)
        self.accept("p", self.toggle_posing)
        self.accept("b", self.actor.toggle_animation_smoothing)
        self.accept("f9", self.take_screenshot)
        self.accept("control-z", self.reset_camera_pos)
        self.accept("wheel_up", self.scroll_up)
        self.accept("wheel_down", self.scroll_down)

    def take_screenshot(self):
        """Function that takes a screenshot of the ShowBase window and saves it to the screenshot directory as
        defined in visorview_globals.py."""
        path = visorview_globals.SCREENSHOT_DIR
        if not os.path.exists(path):
            os.makedirs(path)

        current_cog = self.actors[self.index].get_name()

        now = datetime.now()
        date_string = now.strftime("%d-%m-%Y-%H-%M-%S")
        screenshot_name = os.path.join(path, "ss-{}-{}.png".format(current_cog, date_string))
        base.screenshot(screenshot_name, False)

    def enable_mouse_cam(self):
        """Enables movement of the camera via the mouse."""
        self.camera_controller.enable()

    def disable_mouse_cam(self):
        """Disables movement of the camera via the mouse."""
        self.camera_controller.disable()

    def reset_camera_pos(self):
        """Resets the position of the camera to default as defined in visorview_globals.py."""
        self.camera_controller.reset_position()

    # TODO: GUI should be rewritten entirely and brought to their own classes, and input should be handled in there.
    def scroll_up(self):
        """Function that should be called when the mousewheel is scrolled up, used for functionality in pose mode and
        the animation list."""
        if self.is_scroll_visible:
            self.animation_scroll_list.scrollBy(-1)
        elif self.actor.is_posed(self.current_pose_part) and self.current_pose_part is not None:
            self.actor.increment_pose(1, self.current_pose_part)

    def scroll_down(self):
        """Function that should be called when the mousewheel is scrolled down, used for functionality in pose mode
        and the animation list."""
        if self.is_scroll_visible:
            self.animation_scroll_list.scrollBy(1)
        elif self.actor.is_posed(self.current_pose_part) and self.current_pose_part is not None:
            self.actor.increment_pose(-1, self.current_pose_part)

    def build_cog(self):
        """Function that gets the name of the current cog and assembles/configures its based on parameters defined in
        visorview_globals.py.
        """
        if self.is_scroll_visible:
            self.set_animation_scroll_visibility(False, True)
            self.set_animation_scroll_visibility(False, False)

        if self.current_pose_part is not None:
            self.toggle_posing()

        self.actor.set_actor_data(self.actors[self.index])

    def cycle(self, is_left=False, department=False):
        """Function that rotates to the next cog in the list of cogs defined in visorview_globals.py.

         :param is_left: When false, the index will decrement rather than increment.
         :param department: When true, you will cycle through cog departments/sets rather than individual cogs.
         """
        if department:
            if is_left:
                self.cog_set_index -= 1
                self.cog_set_index = len(COG_SET_NAMES) - 1 if self.cog_set_index < 0 else self.cog_set_index
            else:
                self.cog_set_index += 1
                self.cog_set_index = 0 if self.cog_set_index == len(COG_SET_NAMES) else self.cog_set_index
            self.switch_actor_set(COG_SET_NAMES[self.cog_set_index])
            return

        if is_left:
            self.index -= 1
            self.index = len(self.actors) - 1 if self.index < 0 else self.index
        else:
            self.index += 1
            self.index = 0 if self.index == len(self.actors) else self.index
        self.build_cog()

    def switch_actor_set(self, name):
        """Method that swaps out the set of actors we're cycling through."""
        if name not in ACTORS.keys():
            return
        self.actors = ACTORS[name]
        self.cog_set_index = COG_SET_NAMES.index(name)
        if self.index >= len(self.actors):
            self.index = len(self.actors) - 1
        self.build_cog()

    def add_actor_parts_to_list(self, for_posing=False):
        """Function that clears the animation list and adds the actor parts to it. if for_posing is true, the buttons
        will enable pose mode for that part."""
        self.animation_scroll_list.removeAndDestroyAllItems()
        parts = self.actor.get_actor_parts()

        if not for_posing and len(parts) < 2:
            # no need to select part when we only have one
            self.add_animations_to_list(want_back_button=False)
            return

        method = self.start_posing_part if for_posing else self.add_animations_to_list
        label = "POSE PART" if for_posing else "ANIMATE PART"
        text = DirectLabel(text=label, text_scale=0.1, text_align=TextNode.ALeft, relief=None)
        self.animation_scroll_list.addItem(text)

        for part in parts:
            new_button = DirectButton(text=part, text_scale=0.1, text_align=TextNode.ALeft, relief=None,
                                      suppressMouse=False, command=method, extraArgs=[part])
            self.animation_scroll_list.addItem(new_button)

    def add_animations_to_list(self, part='modelRoot', want_back_button=True):
        """Function that clears the animation list and adds animations to it, based on a specified part. Will add a
        back button by default, returning to the list of actor parts, unless want_back_button is set to false."""
        self.available_animations = self.actor.get_actor_animations(part)
        self.available_animations.sort()
        self.animation_scroll_list.removeAndDestroyAllItems()

        if want_back_button:
            back_button = DirectButton(text="<- BACK", text_scale=0.1, text_align=TextNode.ALeft, relief=None,
                                       suppressMouse=False, command=self.add_actor_parts_to_list)
            self.animation_scroll_list.addItem(back_button)

        for i in self.available_animations:
            if not i == "lose" and not i == "lose_zero":
                # lose animations have their own body type and viewing them on the wrong model = unpleasant
                new_button = DirectButton(text=i, text_scale=0.1, text_align=TextNode.ALeft, relief=None,
                                          suppressMouse=False, command=self.animate_actor, extraArgs=[i, part])
                self.animation_scroll_list.addItem(new_button)

    def animate_actor(self, animation, part=None):
        """Method that calls an animation on our actor and updates pose mode accordingly"""
        if self.current_pose_part is not None:
            self.toggle_posing()
        self.actor.animate(animation, part)

    def toggle_animation_scroll(self):
        """Function that toggles the animation scroll list."""
        self.set_animation_scroll_visibility(not self.is_animation_scroll, False)

    def toggle_pose_scroll(self):
        self.set_animation_scroll_visibility(not self.is_animation_scroll, True)

    def set_animation_scroll_visibility(self, state, for_posing):
        """Enables or disables the animation scroll list based on boolean 'state'. Mouse controls are disabled when its
        open. If for_posing is true, the animation scroll list will be used to select a body part for posing
        """
        if state:
            # we'll be making it visible so prepare the items and disable cam
            self.add_actor_parts_to_list(for_posing)
            self.animation_scroll_list.show()
            self.disable_mouse_cam()
            self.is_scroll_visible = True
        else:
            self.animation_scroll_list.hide()
            self.enable_mouse_cam()
            self.is_scroll_visible = False
        if for_posing:
            # we're doing this for posing
            self.is_animation_scroll = False
            self.is_pose_scroll = state
        else:
            # we're doing this for animations
            self.is_pose_scroll = False
            self.is_animation_scroll = state

    def toggle_posing(self):
        """Function that prompts the user to select a part for posing (if there's more than one) otherwise
        it enables posing mode for the sole part. Will also toggle pose mode off when called a second time
        """
        if self.current_pose_part is not None:
            self.current_pose_part = None
            return
        parts = self.actor.get_actor_parts()
        if len(parts) > 1:
            self.set_animation_scroll_visibility(not self.is_pose_scroll, True)
        else:
            self.start_posing_part(parts[0])

    def start_posing_part(self, part='modelRoot'):
        """Function that begins posing the specified part and closes the animation scroll window."""
        self.actor.set_pose_mode(True, part)
        self.current_pose_part = part
        self.set_animation_scroll_visibility(False, True)


app = VisorView()
app.render.set_antialias(AntialiasAttrib.MMultisample)
app.run()
