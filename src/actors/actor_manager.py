from direct.showbase.ShowBaseGlobal import hidden
from panda3d.core import NodePath
from direct.interval.IntervalGlobal import *
from direct.interval.ActorInterval import ActorInterval
from direct.showbase.ShowBase import Loader
import src.globals.visorview_globals as visorview_globals
from src.actors.skelecog_actor_data import make_skelecog_data_from_cog_data


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
        self.__is_skelecog = False

        # misc info
        self.__pose_frame = {}      # used to keep track of the current frame the actor is posed on
        self.__pose_animation = {}  # used to keep track of the actor's posed animation (get_current_anim dont work)
        self.__looped_animation = {}  # actor intervals = .get_current_anim() isnt always accurate, store ourselves
        self.__from_frame_sequence = None  # stores the sequence used to loop an animation from a certain frame
        self.__skelecog_parent = None  # stores the original actor data when we swap to a skelecog
        self.__head_rotation = 0  # stores the rotation of the head node, if the actor has one

        # actor
        self.__actor = None
        self.__actor_animations = None
        if self.__actor_data is not None:
            self.build_actor()

    def build_actor(self, preserve_anim=False):
        """Function that gets the name of the current cog and assembles/configures its based on parameters defined in
        visorview_globals.py.
        """
        # hide the shadow away while we work
        self.__shadow.reparent_to(hidden)

        # backup animations before we switch our actor; we'll need them to preserve animations
        parts = self.get_actor_parts()
        looping_part_anim = self.__looped_animation
        looping_part_frame = {}
        if preserve_anim and parts is not None:
            for part in parts:
                if part in looping_part_anim:
                    looping_part_frame[part] = self.__actor.get_current_frame(looping_part_anim[part], part)
        else:
            # clear animations
            self.__looped_animation = {}

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
        self.set_head_rotation(self.__head_rotation)

        # actor animations
        self.__actor_animations = self.__actor_data.get_animation_names()
        self.__actor.reparent_to(self)
        self.set_animation_smoothing(self.is_animation_smoothed())

        # deal with resetting pose mode; backup everything in case we want to preserve the current pose/anim
        is_posed = self.__is_posed
        pose_frame = self.__pose_frame
        pose_animation = self.__pose_animation
        self.__is_posed = {}
        self.__pose_frame = {}
        self.__pose_animation = {}

        if preserve_anim:
            parts = self.get_actor_parts()
            for part in parts:
                # bring all the relevant old data over with our new actor
                self.__is_posed[part] = is_posed[part] if part in is_posed else False
                self.__pose_frame[part] = pose_frame[part] if part in pose_frame else 0
                self.__pose_animation[part] = pose_animation[part] if part in pose_animation else None
                # make sure the actor is updated based on this info
                if self.is_posed(part):
                    self.set_pose_mode(True, part)
                else:
                    if part in looping_part_anim:
                        self.animate(looping_part_anim[part], part, looping_part_frame[part])

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

    def set_is_skelecog(self, is_skelecog):
        """Sets whether the actor should display as a skelecog or not."""
        self.__is_skelecog = is_skelecog

        if self.__is_skelecog and self.__actor_data.get_type() == "cog":
            self.__skelecog_parent = self.__actor_data
            self.__actor_data = make_skelecog_data_from_cog_data(self.__skelecog_parent)
            self.build_actor(True)
        elif not self.__is_skelecog and self.__actor_data.get_type() == "skelecog":
            self.__actor_data = self.__skelecog_parent
            self.__skelecog_parent = None
            self.build_actor(True)

    def toggle_skelecog(self):
        self.set_is_skelecog(not self.is_skelecog())

    def is_skelecog(self):
        return self.__is_skelecog

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

        # do this before we set is_posed for this part, because these functions should return based on the current
        # state of is_posed and not the new one
        current_animation = self.get_current_animation(part)
        current_animation_frame = self.get_current_frame(part)
        self.__is_posed[part] = is_posed

        if self.is_posed(part):
            self.__pose_animation[part] = current_animation
            self.__pose_frame[part] = current_animation_frame
            if current_animation is not None:
                self._pose(self.__pose_animation[part], self.__pose_frame[part], part)
        else:
            if self.get_current_animation(part) is not None:
                self._loop(self.get_current_animation(part), part_name=part)

    def _loop(self, animation, part_name=None, from_frame=None):
        """Method that loops an animation on a given part. If no part is specified, it will use the first part in the
        dictionary. fromFrame can be specified, and a sequence will be used to loop the animation from that frame and
        continue on from frame zero at the next loop. This differs from the default behaviour of actor.loop, which will
        loop endlessly from that frame."""
        # make sure the sequence won't jarringly restart the loop
        if self.__from_frame_sequence is not None:
            self.__from_frame_sequence.finish()
        if from_frame is not None:
            self.__from_frame_sequence = Sequence(
                self.__actor.actorInterval(animation, startFrame=from_frame, partName=part_name),
                Func(self.__actor.loop, animation, 1, part_name),
            )
            self.__from_frame_sequence.start()
        else:
            self.__actor.loop(animation, partName=part_name)
        # we're storing this manually as .get_current_anim isnt accurate when actorIntervals are at play.
        self.__looped_animation[part_name] = animation

    def _pose(self, animation, frame, part=None):
        """Method that poses the actor at a given frame. If no part is specified, it will use the first part in the
        dictionary."""
        # make sure the sequence won't jarringly restart the loop
        if self.__from_frame_sequence is not None:
            self.__from_frame_sequence.finish()
        self.__actor.pose(animation, frame, part)
        # we're storing this manually as .get_current_anim isnt accurate when actorIntervals are at play.
        self.__looped_animation[part] = None

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
            current_animation = self.__actor.get_current_anim(part)
            if current_animation is None:
                # this might happen if we're in an actorinterval, so lets check our saved animations:
                current_animation = self.__looped_animation[part] if part in self.__looped_animation else None
            return current_animation

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
            self._pose(part_animation, self.__pose_frame[part], part)

    def get_current_frame(self, part=None):
        """Get the current animation frame, either from a looping animation or pose. If no part is specified, it will
        return the current frame of the first part in the dictionary."""
        part = self.get_first_part() if part is None else part
        if self.is_posed(part):
            return self.__pose_frame[part]
        else:
            current_animation = self.__actor.get_current_anim(part)
            if current_animation is None:
                # this might happen if we're in an actorinterval, so lets check our saved animations:
                current_animation = self.__looped_animation[part] if part in self.__looped_animation else None
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

    def animate(self, animation_name, part=None, from_frame=None):
        """Loops an animation on the actor. If no part is specified, it will use the first part in the dictionary."""
        part = self.get_first_part() if part is None else part
        self.set_pose_mode(False, part)
        self._loop(animation_name, from_frame=from_frame, part_name=part)

    def set_actor_data(self, actor_data):
        """Replaces the current actor with a new one, specified by actor_data."""
        self.__actor_data = actor_data
        # match skelecog data here to avoid it being called more than necessary in build_actor & cause issues
        self.set_is_skelecog(self.is_skelecog())
        self.build_actor()

    def get_actor_parts(self):
        """Returns a list of the actors part names"""
        return self.__actor.get_part_names() if self.__actor is not None else None

    def set_head_rotation(self, h):
        """Method that sets the rotation of the actors head, if it exists.

        :param h: The rotation of the actors head."""
        if self.__actor_data is None:
            return
        self.__head_rotation = h
        head_node = self.__actor_data.get_special_node("head")
        if head_node:
            if self.__get_actor_type() == "boss":
                # everything about these guys is WEIRD!!
                self.__actor.find(head_node).set_p(h)
            else:
                self.__actor.find(head_node).set_h(h)

    def flip_head(self):
        """Method that flips the actors head, if it exists."""
        if self.__head_rotation > 0:
            # assume it's 180
            self.set_head_rotation(0)
        else:
            self.set_head_rotation(180)

    def __get_actor_type(self):
        """Returns the actor's type as a string.'"""
        return self.__actor_data.get_type() if self.__actor_data is not None else None
