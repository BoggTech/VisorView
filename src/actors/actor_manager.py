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
        Takes in any ActorData object, generates an actor from it and manages its properties. If no actor data is
        passed, the actor will not be initialized.

        :param actor_data: An ActorData object.
        :type actor_data: ActorData
        """
        NodePath.__init__(self, 'ActorManager')
        self._actor_data = actor_data

        # visibility settings
        self._is_head = True
        self._is_body = True
        self._is_shadow = True

        # initialize shadow to be used by the actor
        self._shadow = loader.loadModel(visorview_globals.SHADOW_MODEL)
        self._shadow.setScale(visorview_globals.SHADOW_SCALE)
        self._shadow.setColor(visorview_globals.SHADOW_COLOR)

        # states
        self._is_posed = {}
        self._is_animation_smoothed = True
        self._is_skelecog = False

        # misc info
        self._pose_frame = {}      # used to keep track of the current frame the actor is posed on
        self._pose_animation = {}  # used to keep track of the actor's posed animation (get_current_anim dont work)
        self._looped_animation = {}  # actor intervals = .get_current_anim() isnt always accurate, store ourselves
        self._from_frame_sequence = None  # stores the sequence used to loop an animation from a certain frame
        self._skelecog_parent = None  # stores the original actor data when we swap to a skelecog
        self._head_rotation = 0  # stores the rotation of the head node, if the actor has one

        # actor
        self._actor = None
        self._actor_animations = None
        if self._actor_data is not None:
            self._build_actor()

    def _build_actor(self, preserve_anim=False):
        """Method that reads the actor_data stored in this ActorManager and creates an Actor.

        :param preserve_anim: If True, animation/pose will be carried over from the previous actor (where possible)
        :type preserve_anim: bool
        """
        # hide the shadow away while we work
        self._shadow.reparent_to(hidden)

        # backup animations before we switch our actor; we'll need them to preserve animations
        parts = self.get_actor_parts()
        looping_part_anim = self._looped_animation
        looping_part_frame = {}
        if preserve_anim and parts is not None:
            for part in parts:
                if part in looping_part_anim:
                    looping_part_frame[part] = self._actor.get_current_frame(looping_part_anim[part], part)
        else:
            # clear animations
            self._looped_animation = {}

        if self._actor is not None:
            self._actor.cleanup()
            self._actor.remove_node()

        self._actor = self._actor_data.generate_actor()

        shadow_node = self._actor_data.get_special_node("shadow")
        if shadow_node:
            self._shadow.reparent_to(self._actor.find(shadow_node))

        # match settings
        self.set_head_visibility(self.get_head_visibility())
        self.set_body_visibility(self.get_body_visibility())
        self.set_shadow_visibility(self.get_shadow_visibility())
        self.set_head_rotation(self._head_rotation)

        # actor animations
        self._actor_animations = self._actor_data.get_animation_names()
        self._actor.reparent_to(self)
        self.set_animation_smoothing(self.is_animation_smoothed())

        # deal with resetting pose mode; backup everything in case we want to preserve the current pose/anim
        is_posed = self._is_posed
        pose_frame = self._pose_frame
        pose_animation = self._pose_animation
        self._is_posed = {}
        self._pose_frame = {}
        self._pose_animation = {}

        if preserve_anim:
            parts = self.get_actor_parts()
            for part in parts:
                # bring all the relevant old data over with our new actor
                self._is_posed[part] = is_posed[part] if part in is_posed else False
                self._pose_frame[part] = pose_frame[part] if part in pose_frame else 0
                self._pose_animation[part] = pose_animation[part] if part in pose_animation else None
                # make sure the actor is updated based on this info
                if self.is_posed(part):
                    self.set_pose_mode(True, part)
                else:
                    if part in looping_part_anim:
                        self.animate(looping_part_anim[part], part, looping_part_frame[part])

    def set_head_visibility(self, is_head):
        """Updates the visibility of the actor's head within the ActorManager instance and applies it, if possible.

        :param is_head: If True, head will be shown.
        :type is_head: bool
        """
        self._is_head = is_head
        head_node = self._actor_data.get_special_node("head")
        if head_node:
            if self._is_head:
                self._actor.find(head_node).show_through()
            else:
                self._actor.find(head_node).hide()

    def get_head_visibility(self):
        """Returns the visibility of the actor's head as set in the ActorManager instance.

        :return: True if the actor's head is visible, False otherwise.
        :rtype: bool
        """
        return self._is_head

    def toggle_head_visibility(self):
        """Toggles head visibility."""
        self.set_head_visibility(not self.get_head_visibility())

    def set_body_visibility(self, is_body):
        """Updates the visibility of the actor's body within the ActorManager instance and applies it, if possible.

        :param is_body: If True, body will be shown.
        :type is_body: bool
        """
        self._is_body = is_body
        if self._is_body:
            self._actor.show()
        else:
            self._actor.hide()

    def get_body_visibility(self):
        """Returns the visibility of the actor's body as set in the ActorManager instance.

        :return: True if the actor's body is visible, False otherwise.
        :rtype: bool
        """
        return self._is_body

    def toggle_body_visibility(self):
        """Toggles body visibility."""
        self.set_body_visibility(not self.get_body_visibility())

    def set_shadow_visibility(self, is_shadow):
        """Updates the visibility of the actor's shadow within the ActorManager instance and applies it, if possible.

        :param is_shadow: If True, shadow will be shown.
        :type is_shadow: bool
        """
        self._is_shadow = is_shadow
        if is_shadow:
            self._shadow.show_through()
        else:
            self._shadow.hide()

    def get_shadow_visibility(self):
        """Returns the visibility of the actor's shadow as set in the ActorManager instance.

        :return: True if the actor's shadow is visible, False otherwise.
        :rtype: bool
        """
        return self._is_shadow

    def toggle_shadow_visibility(self):
        """Toggles shadow visibility."""
        self.set_shadow_visibility(not self.get_shadow_visibility())

    def set_is_skelecog(self, is_skelecog):
        """Sets whether the actor should display as a skelecog or not and updates the actor accordingly, if possible.

        :param is_skelecog: If True, actor will display as a skelecog when possible.
        :type is_skelecog: bool
        """
        self._is_skelecog = is_skelecog

        if self._is_skelecog and self._actor_data.get_type() == "cog":
            self._skelecog_parent = self._actor_data
            self._actor_data = make_skelecog_data_from_cog_data(self._skelecog_parent)
            self._build_actor(True)
        elif not self._is_skelecog and self._actor_data.get_type() == "skelecog":
            self._actor_data = self._skelecog_parent
            self._skelecog_parent = None
            self._build_actor(True)

    def toggle_skelecog(self):
        """Toggles the actor displaying as a skelecog or not."""
        self.set_is_skelecog(not self.is_skelecog())

    def is_skelecog(self):
        """Returns whether the actor should appear as a skelecog or not.

        :return: True if the actor is set to be a skelecog.
        :rtype: bool
        """
        return self._is_skelecog

    def set_animation_smoothing(self, is_smooth):
        """Set animation smoothing on the actor

        :param is_smooth: If True, the animations on the actor will be smoothed.
        :type is_smooth: bool
        """
        self._is_animation_smoothed = is_smooth
        self._actor.setBlend(frameBlend=self._is_animation_smoothed)

    def is_animation_smoothed(self):
        """Returns the actors animation smoothing state.

        :return: True if the actor's animations are being smoothed.
        :rtype: bool"""
        return self._is_animation_smoothed

    def toggle_animation_smoothing(self):
        """Toggles animation smoothing."""
        self.set_animation_smoothing(not self.is_animation_smoothed())

    def set_pose_mode(self, is_posed, part=None):
        """Set the state of pose mode.

        :param is_posed: If True, pose mode will be enabled.
        :type is_posed: bool
        :param part: Actor part to target. If no part is specified, it will use the first part in the dictionary.
        :type part: str
        """
        part = self._get_first_part() if part is None else part

        # do this before we set is_posed for this part, because these functions should return based on the current
        # state of is_posed and not the new one
        current_animation = self.get_current_animation(part)
        current_animation_frame = self.get_current_frame(part)
        self._is_posed[part] = is_posed

        if self.is_posed(part):
            self._pose_animation[part] = current_animation
            self._pose_frame[part] = current_animation_frame
            if current_animation is not None:
                self._pose(self._pose_animation[part], self._pose_frame[part], part)
        else:
            if self.get_current_animation(part) is not None:
                self._loop(self.get_current_animation(part), part_name=part)

    def _loop(self, animation, part_name=None, from_frame=None):
        """Method that loops an animation on a given part. This method differs from the behaviour of actor.loop, which
        will loop endlessly from it's from_frame, and will instead play once from that frame and continue to loop from
        frame zero.

        :param animation: Animation name to loop.
        :type animation: str
        :param part_name: Actor part to target. If no part is specified, it will use the first part in the dictionary.
        :type part_name: str
        :param from_frame: Frame to start the animation on.
        :type from_frame: int
        """
        # make sure the sequence won't jarringly restart the loop
        if self._from_frame_sequence is not None:
            self._from_frame_sequence.finish()
        if from_frame is not None:
            self._from_frame_sequence = Sequence(
                self._actor.actorInterval(animation, startFrame=from_frame, partName=part_name),
                Func(self._actor.loop, animation, 1, part_name),
            )
            self._from_frame_sequence.start()
        else:
            self._actor.loop(animation, partName=part_name)
        # we're storing this manually as .get_current_anim isnt accurate when actorIntervals are at play.
        self._looped_animation[part_name] = animation

    def _pose(self, animation, frame, part=None):
        """Method that poses a given part of the actor at a given frame.
        
        :param animation: Animation name to pose.
        :type animation: str
        :param frame: Frame to pose the animation on.
        :type frame: int
        :param part: Actor part to target. If no part is specified, it will use the first part in the dictionary.
        :type part: str
        """
        # make sure the sequence won't jarringly restart the loop
        if self._from_frame_sequence is not None:
            self._from_frame_sequence.finish()
        self._actor.pose(animation, frame, part)
        # we're storing this manually as .get_current_anim isn't accurate when actorIntervals are at play.
        self._looped_animation[part] = None

    def is_posed(self, part=None):
        """Returns state of pose mode for a given part.

        :param part: Actor part to target. If no part is specified, it will use the first part in the dictionary.
        :type part: str
        """
        part = self._get_first_part() if part is None else part
        return self._is_posed[part] if part in self._is_posed else False

    def get_current_animation(self, part=None):
        """Gets the current animation on the part, posed or looping.

        :param part: Actor part to target. If no part is specified, it will use the first part in the dictionary.
        :type part: str
        """
        part = self._get_first_part() if part is None else part
        if self.is_posed(part):
            return self._pose_animation[part] if part in self._pose_animation else None
        else:
            current_animation = self._actor.get_current_anim(part)
            if current_animation is None:
                # this might happen if we're in an actorinterval, so lets check our saved animations:
                current_animation = self._looped_animation[part] if part in self._looped_animation else None
            return current_animation

    def toggle_posed(self, part=None):
        """Toggles pose mode for a given part.

        :param part: Actor part to target. If no part is specified, it will use the first part in the dictionary.
        :type part: str
        """
        part = self._get_first_part() if part is None else part
        self.set_pose_mode(not self.is_posed(part), part)

    def increment_pose(self, count, part=None):
        """Increments the currently posed frame by count. Must be posed.

        :param count: The number of frames to increment the pose by.
        :type count: int
        :param part: Actor part to target. If no part is specified, it will use the first part in the dictionary.
        :type part: str
        """
        part = self._get_first_part() if part is None else part

        if not self.is_posed(part):
            return

        # modulo to ensure frame count loops around
        part_frame = self.get_current_frame(part)
        part_animation = self.get_current_animation(part)
        current_anim_frame_count = self._actor.get_num_frames(part_animation)
        # frame count will be none if no animation is currently playing, this prevents a crash
        if current_anim_frame_count is not None:
            self._pose_frame[part] = (part_frame + count) % current_anim_frame_count
            self._pose(part_animation, self._pose_frame[part], part)

    def get_current_frame(self, part=None):
        """Get the current animation frame, either from a looping animation or pose.

        :param part: Actor part to target. If no part is specified, it will use the first part in the dictionary.
        :type part: str
        """
        part = self._get_first_part() if part is None else part
        if self.is_posed(part):
            return self._pose_frame[part]
        else:
            current_animation = self._actor.get_current_anim(part)
            if current_animation is None:
                # this might happen if we're in an actorinterval, so lets check our saved animations:
                current_animation = self._looped_animation[part] if part in self._looped_animation else None
            return self._actor.get_current_frame(current_animation, part)

    def _get_first_part(self):
        """Gets the first part of the actor.

        :return: First part of the actor's dictionary, usually modelRoot for single-part actors.
        :rtype: str"""
        first_part = self._actor.get_part_names()[0]
        return first_part

    def get_actor_animations(self, part=None):
        """Returns a list of the actor's animations for a specified part.

        :param part: Actor part to target. If no part is specified, it will use the first part in the dictionary.
        :type part: str
        """
        part = self._get_first_part() if part is None else part
        return self._actor_animations[part] if self._actor_animations is not None else None

    def animate(self, animation_name, part=None, from_frame=None):
        """Loops an animation on the actor.

        :param animation_name: Animation name to loop.
        :type animation_name: str
        :param part: Actor part to target. If no part is specified, it will use the first part in the dictionary.
        :type part: str
        :param from_frame: Frame to start the animation from.
        :type from_frame: int
        """
        part = self._get_first_part() if part is None else part
        self.set_pose_mode(False, part)
        self._loop(animation_name, from_frame=from_frame, part_name=part)

    def set_actor_data(self, actor_data):
        """Replaces the current set of actor data with a new one and builds an actor from it.

        :param actor_data: Actor data to use.
        :type actor_data: ActorData
        """
        self._actor_data = actor_data
        # match skelecog data here to avoid it being called more than necessary in build_actor & cause issues
        self.set_is_skelecog(self.is_skelecog())
        self._build_actor()

    def get_actor_parts(self):
        """Returns a list of the actors part names

        :return: List of actor part names.
        :rtype: list[str]"""
        return self._actor.get_part_names() if self._actor is not None else None

    def set_head_rotation(self, h):
        """Method that sets the rotation of the actors head and applies it (if possible).

        :param h: The rotation of the actors head.
        :type h: float"""
        if self._actor_data is None:
            return
        self._head_rotation = h
        head_node = self._actor_data.get_special_node("head")
        if head_node:
            if self._get_actor_type() == "boss":
                # everything about these guys is WEIRD!!
                self._actor.find(head_node).set_p(h)
            else:
                self._actor.find(head_node).set_h(h)

    def flip_head(self):
        """Method that flips the actors head, if it exists."""
        if self._head_rotation > 0:
            # assume it's 180
            self.set_head_rotation(0)
        else:
            self.set_head_rotation(180)

    def _get_actor_type(self):
        """Returns the actor's type as a string.

        :return: The actor's type.
        :rtype: str
        """
        return self._actor_data.get_type() if self._actor_data is not None else None
