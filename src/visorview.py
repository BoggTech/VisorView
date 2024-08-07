import src.globals as globals

import os
from datetime import datetime
from panda3d.core import AntialiasAttrib, Loader
from panda3d.core import TextNode
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from direct.gui.DirectGui import *
from src.camera import Camera
from src.actors.actor_globals import ACTORS, COG_SET_NAMES

resources = globals.RESOURCES_DIR
if not os.path.exists(resources):
    os.makedirs(resources)
    print("Please input Toontown Rewritten extracted phase files!")


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

        # initialize various states
        self.is_head = True
        self.is_body = True
        self.is_blend = True

        # initialize pose mode
        self.is_posed = False
        self.current_animation = None
        self.last_pose_frame = 0

        # initialize shadow to be used by the actor
        self.shadow = loader.loadModel(globals.SHADOW_MODEL)
        self.shadow.setScale(globals.SHADOW_SCALE)
        self.shadow.setColor(globals.SHADOW_COLOR)
        self.is_shadow = True

        # initialize our actor
        self.actors = ACTORS["supervisors"]
        self.cog_set_index = 0
        self.actor = None
        self.index = 0
        self.build_cog()

        self.reset_actor_pos()
        self.reset_camera_pos()

        # we're initialized, time to accept input
        self.accept("space", self.cycle)
        self.accept("arrow_left", lambda: self.cycle(True))
        self.accept("arrow_right", lambda: self.cycle(False))
        self.accept("arrow_up", lambda: self.cycle(False, True))
        self.accept("arrow_down", lambda: self.cycle(True, True))
        self.accept("s", self.toggle_shadow)
        self.accept("control-b", self.toggle_body)
        self.accept("control-h", self.toggle_head)
        self.accept("1", lambda: self.switch_actor_set("supervisors"))
        self.accept("2", lambda: self.switch_actor_set("sellbots"))
        self.accept("3", lambda: self.switch_actor_set("cashbots"))
        self.accept("4", lambda: self.switch_actor_set("lawbots"))
        self.accept("5", lambda: self.switch_actor_set("bossbots"))
        self.accept("a", self.toggle_animation_scroll)
        self.accept("p", self.toggle_pose)
        self.accept("b", self.toggle_blend)
        self.accept("f9", self.take_screenshot)
        self.accept("control-z", self.reset_camera_pos)
        self.accept("wheel_up", self.scroll_up)
        self.accept("wheel_down", self.scroll_down)

    def take_screenshot(self):
        """Function that takes a screenshot of the ShowBase window and saves it to the screenshot directory as
        defined in globals.py."""
        path = globals.SCREENSHOT_DIR
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

    def reset_actor_pos(self):
        """Resets the position of the actor to default as defined in globals.py."""
        self.actor.set_pos_hpr(*globals.DEFAULT_POS, *globals.DEFAULT_HPR)

    def reset_camera_pos(self):
        """Resets the position of the camera to default as defined in globals.py."""
        self.camera_controller.reset_position()

    # TODO: GUI should be rewritten entirely and brought to their own classes, and input should be handled in there.
    def scroll_up(self):
        """Function that should be called when the mousewheel is scrolled up, used for functionality in pose mode and
        the animation list."""
        if self.is_animation_scroll:
            self.animation_scroll_list.scrollBy(-1)
        elif self.is_posed and self.last_pose_frame is not None:
            self.last_pose_frame += 1
            if self.last_pose_frame > self.actor.getNumFrames(self.current_animation):
                self.last_pose_frame = 0
            self.actor.pose(self.current_animation, self.last_pose_frame)

    def scroll_down(self):
        """Function that should be called when the mousewheel is scrolled down, used for functionality in pose mode
        and the animation list."""
        if self.is_animation_scroll:
            self.animation_scroll_list.scrollBy(1)
        elif self.is_posed and self.last_pose_frame is not None:
            self.last_pose_frame -= 1
            if self.last_pose_frame < 0:
                self.last_pose_frame = self.actor.getNumFrames(self.current_animation)
            self.actor.pose(self.current_animation, self.last_pose_frame)

    def build_cog(self):
        """Function that gets the name of the current cog and assembles/configures its based on parameters defined in
        globals.py.
        """
        # hide the shadow away while we work
        self.shadow.reparent_to(hidden)
        if self.actor is not None:
            self.actor.cleanup()
            self.actor.remove_node()
        actor_data = self.actors[self.index]
        self.actor = actor_data.generate_actor()
        if actor_data.has_shadow:
            self.shadow.reparent_to(self.actor.find(actor_data.shadow_node))

        # disable posing + clear anim
        self.is_posed = False
        self.set_animation(None)

        # match settings
        self.toggle_head(False)
        self.toggle_shadow(False)
        self.toggle_body(False)
        self.actor.reparent_to(render)
        self.actor.set_blend(frameBlend=self.is_blend)

        # this is a little messy in the meantime but it'll be changed later
        self.available_animations = list(self.actor.getAnimControlDict()['common']['modelRoot'].keys())
        self.available_animations.sort()
        self.animation_scroll_list.removeAndDestroyAllItems()
        for i in self.available_animations:
            if not i == "lose" and not i == "lose_zero":
                # lose animations have their own body type and viewing them on the wrong model = unpleasant
                new_button = DirectButton(text=i, text_scale=0.1, text_align=TextNode.ALeft, relief=None,
                                          suppressMouse=False, command=self.set_animation, extraArgs=[i])
                self.animation_scroll_list.addItem(new_button)

    def cycle(self, is_left=False, department=False):
        """Function that rotates to the next cog in the list of cogs defined in globals.py.

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

    def set_animation(self, animation):
        """Function that switches the actors currently playing animation."""
        self.current_animation = animation
        self.actor.loop(animation)

        # no more posing
        self.is_posed = False

    # TODO: clean these up a little bit
    def toggle_pose(self):
        """Function that toggles pose mode on or off. Closes any open UI."""
        self.is_posed = not self.is_posed
        if self.is_posed:
            # if the scroll is open, toggle it
            self.toggle_animation_scroll(False)
            self.last_pose_frame = self.actor.getCurrentFrame()
            self.actor.pose(self.current_animation, self.last_pose_frame)
        else:
            self.actor.loop(self.current_animation)

    def toggle_blend(self):
        """Function that toggles animation blending on the actor."""
        self.is_blend = not self.is_blend
        self.actor.setBlend(frameBlend=self.is_blend)

    def toggle_animation_scroll(self, state=None):
        """Function that toggles the animation scroll list. Mouse controls are disabled when its open.

        :param boolean state: The desired state. Set to None by default, which will simply toggle the current state.
        """

        if not state is None:
            self.is_animation_scroll = state
        else:
            self.is_animation_scroll = not self.is_animation_scroll

        if self.is_animation_scroll:
            self.animation_scroll_list.show()
            self.disable_mouse_cam()
        else:
            self.animation_scroll_list.hide()
            self.enable_mouse_cam()

    def toggle_shadow(self, update_state=True):
        """Function that toggles the actor's shadow visibility.

        :param boolean update_state: True by default, if False it will not toggle the current state.
        """
        if update_state:
            self.is_shadow = not self.is_shadow

        if self.is_shadow:
            self.shadow.show_through()
        else:
            self.shadow.hide()

    def toggle_head(self, update_state=True):
        """Function that toggles the actor's head visibility.
        
        :param boolean update_state: True by default, if False it will not toggle the current state.
        """
        if update_state:
            self.is_head = not self.is_head

        if self.is_head:
            self.actor.find('**/def_head').show_through()
        else:
            self.actor.find('**/def_head').hide()

    def toggle_body(self, update_state=True):
        """Function that toggles the actor's body visibility.

        :param boolean update_state: True by default, if False it will not toggle the current state.
        """
        if update_state:
            self.is_body = not self.is_body

        if self.is_body:
            self.actor.show_through()
        else:
            self.actor.hide()

        # make sure the children are shown/hidden if they need to be
        self.toggle_head(False)
        self.toggle_shadow(False)


app = VisorView()
app.render.set_antialias(AntialiasAttrib.MMultisample)
app.run()
