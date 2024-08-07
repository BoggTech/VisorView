from direct.showbase.ShowBaseGlobal import hidden
from panda3d.core import NodePath
from direct.showbase.ShowBase import Loader
import src.globals.visorview_globals as visorview_globals


class ActorManager(NodePath):
    def __init__(self, actor_data=None):
        """Initializes the ActorManager.
        Takes in any ActorData object, generates an actor from it and manages its properties.
        """
        NodePath.__init__(self, 'ActorManager')
        self.__actor_data = actor_data

        # visibility settings
        self.__is_head = True
        self.__is_body = True
        self.__is_shadow = True

        # states
        self.__is_posed = False
        self.__is_animation_smoothed = True

        # initialize shadow to be used by the actor
        self.__shadow = loader.loadModel(visorview_globals.SHADOW_MODEL)
        self.__shadow.setScale(visorview_globals.SHADOW_SCALE)
        self.__shadow.setColor(visorview_globals.SHADOW_COLOR)

        # misc info
        self.__pose_frame = 0
        self.__pose_animation = None

        # actor
        self.__actor = None
        self.__actor_animations = None
        if self.__actor_data is not None:
            self.build_actor()

    def build_actor(self):
        """Function that gets the name of the current cog and assembles/configures its based on parameters defined in
        visorview_globals.py.
        """
        # hide the shadow away while we work
        self.__shadow.reparent_to(hidden)
        if self.__actor is not None:
            self.__actor.cleanup()
            self.__actor.remove_node()

        self.__actor = self.__actor_data.generate_actor()
        if self.__actor_data.has_shadow:
            self.__shadow.reparent_to(self.__actor.find(self.__actor_data.shadow_node))

        # match settings
        self.set_head_visibility(self.get_head_visibility())
        self.set_body_visibility(self.get_body_visibility())
        self.set_shadow_visibility(self.get_shadow_visibility())

        # actor animations
        self.__actor_animations = self.__actor_data.get_animation_names()
        self.__actor.reparent_to(self)
        self.set_animation_smoothing(self.is_animation_smoothed())

        # disable posing + clear anim
        self.__pose_animation = None  # prevent animation from playing
        self.set_pose_mode(False)

    def set_head_visibility(self, is_head):
        """Hides/shows the actor's head based on boolean is_head (if possible)."""
        self.__is_head = is_head
        if self.__get_actor_type() == 'cog':
            if self.__is_head:
                self.__actor.find('**/def_head').show_through()
            else:
                self.__actor.find('**/def_head').hide()

    def get_head_visibility(self):
        """Returns True if the actor's head is visible, False otherwise."""
        return self.__is_head

    def toggle_head_visibility(self):
        """Toggles head visibility."""
        self.set_head_visibility(not self.get_head_visibility())

    def set_body_visibility(self, is_body):
        """Hides/shows the actor's body based on boolean is_body (if possible)."""
        self.__is_body = is_body
        if self.__get_actor_type() == 'cog':
            if self.__is_body:
                self.__actor.show()
            else:
                self.__actor.hide()

    def get_body_visibility(self):
        """Returns True if the actor's body is visible, False otherwise.'"""
        return self.__is_body

    def toggle_body_visibility(self):
        """Toggles body visibility."""
        self.set_body_visibility(not self.get_body_visibility())

    def set_shadow_visibility(self, is_shadow):
        """Hides/shows the actor's shadow."""
        self.__is_shadow = is_shadow
        if is_shadow:
            self.__shadow.show()
        else:
            self.__shadow.hide()

    def get_shadow_visibility(self):
        """Returns True if the actor's shadow is visible, False otherwise."""
        return self.__is_shadow

    def toggle_shadow_visibility(self):
        """Toggles shadow visibility."""
        self.set_shadow_visibility(not self.get_shadow_visibility())

    def set_animation_smoothing(self, is_smooth):
        """Sets animation smoothing based on boolean value is_smooth"""
        self.__is_animation_smoothed = is_smooth
        self.__actor.setBlend(frameBlend=self.__is_animation_smoothed)

    def is_animation_smoothed(self):
        """Returns True if animation smoothing is enabled, False otherwise."""
        return self.__is_animation_smoothed

    def toggle_animation_smoothing(self):
        """Toggles animation smoothing."""
        self.set_animation_smoothing(not self.get_animation_smoothing())

    def set_pose_mode(self, is_posed):
        """Enables or disables pose mode based on boolean is_posed (if possible)."""
        self.__is_posed = is_posed
        current_animation = self.__actor.get_current_anim()
        current_animation_frame = self.__actor.get_current_frame(current_animation)

        if self.is_posed():
            if current_animation is not None:
                self.__pose_animation = current_animation
                self.__pose_frame = current_animation_frame
                self.__actor.pose(self.__pose_animation, self.__pose_frame)
        else:
            if self.__pose_animation is not None:
                self.__actor.loop(self.__pose_animation)

    def is_posed(self):
        """Returns True if the actor is posed, False otherwise."""
        return self.__is_posed

    def toggle_posed(self):
        """Toggles pose mode."""
        self.set_pose_mode(not self.is_posed())

    def increment_pose(self, count):
        """Increments the currently posed frame by count. Must be posed."""
        if not self.is_posed():
            return

        # modulo to ensure frame count loops around
        current_anim_frame_count = self.__actor.get_num_frames(self.__pose_animation)
        self.__pose_frame = (self.__pose_frame + count) % current_anim_frame_count
        self.__actor.pose(self.__pose_animation, self.__pose_frame)

    def get_current_frame(self):
        """Get the current animation frame, either from a looping animation or pose."""
        if self.is_posed():
            return self.__pose_frame
        else:
            current_animation = self.__actor.get_current_anim()
            return self.__actor.get_current_frame(current_animation)

    def get_actor_animations(self):
        """Returns a list of the actor's animations."""
        return self.__actor_animations

    def animate(self, animation_name):
        """Loops an animation on the actor."""
        self.set_pose_mode(False)
        if animation_name == "zero":
            # this is really hacky and a little dumb but i quite literally can't find another way to make the actor
            # return to the default t-pose... using .stop() just makes it go to a pose with its arms down. if anybody
            # sees this and knows how and can save me from this please let me know
            self.build_actor()
        else:
            self.__actor.loop(animation_name)

    def set_actor_data(self, actor_data):
        """Replaces the current actor with a new one, specified by actor_data."""
        self.__actor_data = actor_data
        self.build_actor()

    def __get_actor_type(self):
        """Returns the actor's type as a string.'"""
        return self.__actor_data.get_type()