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

        # initialize shadow to be used by the actor
        self.__shadow = loader.loadModel(visorview_globals.SHADOW_MODEL)
        self.__shadow.setScale(visorview_globals.SHADOW_SCALE)
        self.__shadow.setColor(visorview_globals.SHADOW_COLOR)

        # states
        self.__is_posed = {}
        self.__is_animation_smoothed = True

        # misc info
        self.__pose_frame = {}
        self.__pose_animation = {}

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

        shadow_node = self.__actor_data.get_special_node("shadow")
        if shadow_node:
            self.__shadow.reparent_to(self.__actor.find(shadow_node))

        # match settings
        self.set_head_visibility(self.get_head_visibility())
        self.set_body_visibility(self.get_body_visibility())
        self.set_shadow_visibility(self.get_shadow_visibility())

        # actor animations
        self.__actor_animations = self.__actor_data.get_animation_names()
        self.__actor.reparent_to(self)
        self.set_animation_smoothing(self.is_animation_smoothed())

        # reset pose mode for new actor parts + prevent animations playing
        self.__is_posed = {}
        self.__pose_frame = {}
        self.__pose_animation = {}
        for part in self.__actor.get_part_names():
            self.set_pose_mode(False, part)

    def set_head_visibility(self, is_head):
        """Hides/shows the actor's head based on boolean is_head (if possible)."""
        self.__is_head = is_head
        head_node = self.__actor_data.get_special_node("head")
        if head_node:
            if self.__is_head:
                self.__actor.find(head_node).show_through()
            else:
                self.__actor.find(head_node).hide()

    def get_head_visibility(self):
        """Returns True if the actor's head is visible, False otherwise."""
        return self.__is_head

    def toggle_head_visibility(self):
        """Toggles head visibility."""
        self.set_head_visibility(not self.get_head_visibility())

    def set_body_visibility(self, is_body):
        """Hides/shows the actor's body based on boolean is_body (if possible)."""
        self.__is_body = is_body
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
            self.__shadow.show_through()
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
        self.set_animation_smoothing(not self.is_animation_smoothed())

    def set_pose_mode(self, is_posed, part=None):
        """Enables or disables pose mode based on boolean is_posed (if possible). If no part is specified, it will use
        the first part in the dictionary."""
        part = self.get_first_part() if part is None else part

        self.__is_posed[part] = is_posed
        current_animation = self.__actor.get_current_anim(part)
        current_animation_frame = self.__actor.get_current_frame(current_animation, part)

        if self.is_posed(part):
            self.__pose_animation[part] = current_animation
            self.__pose_frame[part] = current_animation_frame
            if current_animation is not None:
                self.__actor.pose(self.__pose_animation[part], self.__pose_frame[part], part)
        else:
            if self.get_current_animation(part) is not None:
                self.__actor.loop(self.get_current_animation(part), partName=part)

    def is_posed(self, part=None):
        """Returns True if the actor is posed, False otherwise. If no part is specified, it will use the first
        part in the dictionary."""
        part = self.get_first_part() if part is None else part
        return self.__is_posed[part] if part in self.__is_posed else False

    def get_current_animation(self, part=None):
        """Gets the current animation on the part, posed or looping. If no part is specified, it will use the first
        part in the dictionary."""
        part = self.get_first_part() if part is None else part
        if self.is_posed(part):
            return self.__pose_animation[part] if part in self.__pose_animation else None
        else:
            return self.__actor.get_current_anim(part)

    def toggle_posed(self, part=None):
        """Toggles pose mode. If no part is specified, it will use the first
        part in the dictionary."""
        part = self.get_first_part() if part is None else part
        self.set_pose_mode(not self.is_posed(part), part)

    def increment_pose(self, count, part=None):
        """Increments the currently posed frame by count. Must be posed. If no part is specified, it will use the first
        part in the dictionary.
        """
        part = self.get_first_part() if part is None else part

        if not self.is_posed(part):
            return

        # modulo to ensure frame count loops around
        part_frame = self.get_current_frame(part)
        part_animation = self.get_current_animation(part)
        current_anim_frame_count = self.__actor.get_num_frames(part_animation)
        # framecount will be none if no animation is currently playing, this prevents a crash
        if current_anim_frame_count is not None:
            self.__pose_frame[part] = (part_frame + count) % current_anim_frame_count
            self.__actor.pose(part_animation, part_frame, part)

    def get_current_frame(self, part=None):
        """Get the current animation frame, either from a looping animation or pose. If no part is specified, it will
        return the current frame of the first part in the dictionary."""
        part = self.get_first_part() if part is None else part
        if self.is_posed(part):
            return self.__pose_frame[part]
        else:
            current_animation = self.__actor.get_current_anim(part)
            return self.__actor.get_current_frame(current_animation, part)

    def get_first_part(self):
        """Gets the first part of the actor, usually modelRoot for single-part actors."""
        first_part = self.__actor.get_part_names()[0]
        return first_part

    def get_actor_animations(self, part=None):
        """Returns a list of the actor's animations for a specified part. If no part is specified, it will use the
        first part in the dictionary."""
        part = self.get_first_part() if part is None else part
        return self.__actor_animations[part] if self.__actor_animations is not None else None

    def animate(self, animation_name, part=None):
        """Loops an animation on the actor. If no part is specified, it will use the first part in the dictionary."""
        part = self.get_first_part() if part is None else part
        self.set_pose_mode(False, part)
        self.__actor.loop(animation_name, partName=part)

    def set_actor_data(self, actor_data):
        """Replaces the current actor with a new one, specified by actor_data."""
        self.__actor_data = actor_data
        self.build_actor()

    def get_actor_parts(self):
        """Returns a list of the actors part names"""
        return self.__actor.get_part_names()

    def __get_actor_type(self):
        """Returns the actor's type as a string.'"""
        return self.__actor_data.get_type()
