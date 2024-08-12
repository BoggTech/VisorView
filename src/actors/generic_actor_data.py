from os.path import basename
import posixpath
import src.util.vfs_glob as glob
from panda3d.core import Filename, Vec4, VBase4
from direct.actor.Actor import Actor
from src.actors.actor_data import ActorData


class GenericActorData(ActorData):
    _actor_type = "generic"

    def __init__(self, name, model_path, animation_prefix, scale=1):
        """Initializes generic actor data. This is for simple actors that consist of a model and some animations,
        specified with a glob pattern.

        :param name: The name of the generic actor.
        :type name: str
        :param model_path: The path to the actors model.
        :type model_path: str
        :param animation_prefix: The prefix of the actors animations, used in a glob pattern, i.e. "tt_a_ene_cga_"
        :type animation_prefix: str
        """
        super().__init__()
        self.set_name(name)
        self.add_data("scale", scale)
        self.model_path = model_path

        self.generic_animation_paths = glob.glob("phase_*/models/char/" + animation_prefix + "*.bam")
        self.generic_animation_dict = {}
        filename_length = len(animation_prefix)
        for i in range(0, len(self.generic_animation_paths)):
            self.generic_animation_dict[
                basename(self.generic_animation_paths[i])[filename_length:-4]
            ] = self.generic_animation_paths[i]
        self.generic_animations = list(self.generic_animation_dict)
        self.generic_animations.sort()

    def get_animation_names(self):
        """Returns a dict specifying the animation names for this actor and its parts.

        :return: A dict of animation names with actor parts as keys.
        :rtype: dict
        """
        return {'modelRoot': self.generic_animations}

    def generate_actor(self):
        """Returns an actor based on the data within this class.

        :return: An actor based on the data within this class.
        :rtype: Actor
        """
        scale = self.get_data("scale")
        actor = Actor(self.model_path, self.generic_animation_dict)
        actor.set_scale(scale)
        return actor
