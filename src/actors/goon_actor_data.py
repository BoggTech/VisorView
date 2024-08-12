import os
import posixpath
import src.util.vfs_glob as glob
from panda3d.core import Filename, Vec4, VBase4
from direct.actor.Actor import Actor
from src.actors.actor_data import ActorData

GOON_MODEL = "phase_9/models/char/ttr_r_chr_ene_cogGoonie.bam"
GOON_ANIMATION_PATHS = glob.glob("phase_*/models/char/ttr_a_chr_ene_cogGoonie_*.bam")
GOON_ANIMATION_DICT = {}
for i in range(0, len(GOON_ANIMATION_PATHS)):
    GOON_ANIMATION_DICT[os.path.basename(GOON_ANIMATION_PATHS[i])[24:-4]] = GOON_ANIMATION_PATHS[i]
GOON_ANIMATIONS = list(GOON_ANIMATION_DICT)
GOON_ANIMATIONS.sort()

PG_COLORS = [
    Vec4(0.95, 0.0, 0.0, 1.0),
    Vec4(0.75, 0.35, 0.1, 1.0),
              ]
SG_COLORS = [
    Vec4(0.0, 0.0, 0.95, 1.0),
    Vec4(0.35, 0.0, 0.75, 1.0),
               ]

class GoonActorData(ActorData):
    _actor_type = "goon"
    _special_nodes = {"shadow": "*"}

    def __init__(self, name, hat_color=(1, 1, 1, 1), scale=1, is_security=False):
        """Initializes the GoonActorData instance.

        :param name: The name of the Goon.
        :type name: str
        :param hat_color: Color of the goons hat.
        :type hat_color: Vec4
        :param scale: Scale of the goon.
        :type scale: float
        :param is_security: Set to true to use the Security Goon model.
        :type is_security: bool
        """
        super().__init__()
        self.set_name(name)
        self.add_data("hat_color", hat_color)
        self.add_data("scale", scale)
        self.add_data("is_security", is_security)

    def get_animation_names(self):
        """Returns a dict specifying the animation names for this actor and its parts.

        :return: A dict of animation names with actor parts as keys.
        :rtype: dict
        """
        return {'modelRoot': GOON_ANIMATIONS}

    def generate_actor(self):
        """Returns an actor based on the data within this class.

        :return: An actor based on the data within this class.
        :rtype: Actor
        """
        actor = Actor(GOON_MODEL, GOON_ANIMATION_DICT)
        hat_color = self.get_data("hat_color")
        is_security = self.get_data("is_security")
        if is_security:
            actor.find("**/hard_hat").hide()
            actor.find("**/security_hat").set_color(hat_color)
        else:
            actor.find_all_matches("**/security_hat*").hide()
            actor.find("**/hard_hat").set_color(hat_color)
        scale = self.get_data("scale")
        actor.set_scale(scale)
        actor.find("**/eye").set_color(1, 1, 0, 1)
        return actor
