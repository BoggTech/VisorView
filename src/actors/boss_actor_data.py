from os.path import basename
import posixpath
import src.util.vfs_glob as glob
from panda3d.core import Filename, Vec4, VBase4
from direct.actor.Actor import Actor
from src.actors.actor_data import ActorData
from direct.showbase.ShowBase import Loader

TORSO_DICT = {
    "sell": "phase_9/models/char/sellbotBoss-torso-zero.bam",
    "cash": "phase_10/models/char/cashbotBoss-torso-zero.bam",
    "law": "phase_11/models/char/lawbotBoss-torso-zero.bam",
    "boss": "phase_12/models/char/bossbotBoss-torso-zero.bam",
}

HEAD_DICT = {
    "sell": "phase_9/models/char/sellbotBoss-head-zero.bam",
    "cash": "phase_10/models/char/cashbotBoss-head-zero.bam",
    "law": "phase_11/models/char/lawbotBoss-head-zero.bam",
    "boss": "phase_12/models/char/bossbotBoss-head-zero.bam",
}

TREADS_MODEL = "phase_9/models/char/bossCog-treads.bam"
LEGS_MODEL = "phase_9/models/char/bossCog-legs-zero.bam"

HEAD_ANIMATION_PATHS = glob.glob("phase_*/models/char/bossCog-head-*.bam")
TORSO_ANIMATION_PATHS = glob.glob("phase_*/models/char/bossCog-torso-*.bam")
LEG_ANIMATION_PATHS = glob.glob("phase_*/models/char/bossCog-legs-*.bam")

HEAD_ANIMATION_DICT = {}
TORSO_ANIMATION_DICT = {}
LEG_ANIMATION_DICT = {}

for i in range(0, len(HEAD_ANIMATION_PATHS)):
    HEAD_ANIMATION_DICT[basename(HEAD_ANIMATION_PATHS[i])[13:-4]] = HEAD_ANIMATION_PATHS[i]
for i in range(0, len(TORSO_ANIMATION_PATHS)):
    TORSO_ANIMATION_DICT[basename(TORSO_ANIMATION_PATHS[i])[14:-4]] = TORSO_ANIMATION_PATHS[i]
for i in range(0, len(LEG_ANIMATION_PATHS)):
    LEG_ANIMATION_DICT[basename(LEG_ANIMATION_PATHS[i])[13:-4]] = LEG_ANIMATION_PATHS[i]

HEAD_ANIMATIONS = list(HEAD_ANIMATION_DICT)
TORSO_ANIMATIONS = list(TORSO_ANIMATION_DICT)
LEG_ANIMATIONS = list(LEG_ANIMATION_DICT)

HEAD_ANIMATIONS.sort()
TORSO_ANIMATIONS.sort()
LEG_ANIMATIONS.sort()

ANIMATION_NAME_DICT = {
    "head": HEAD_ANIMATIONS,
    "torso": TORSO_ANIMATIONS,
    "leg": LEG_ANIMATIONS
}

class BossActorData(ActorData):
    """Class that stores data on and generates actors for the four Boss Cogs."""
    _actor_type = "boss"

    def __init__(self, name, department, scale):
        """Initializes the actor data.
        :param department: Department name. (sell, cash, law or boss)
        :type department: str
        :param scale: Scale of the Boss Cog.
        :type scale: int"""

        super().__init__()
        self.add_data("scale", scale)
        self.add_data("department", department)
        self.set_name(name)

    def generate_actor(self):
        """Returns an actor based on the data within this class."""
        department = self.get_data("department")
        actor = Actor({
            'head': HEAD_DICT[department],
            'torso': TORSO_DICT[department],
            'leg': LEGS_MODEL
        }, {
            'head': HEAD_ANIMATION_DICT,
            'torso': TORSO_ANIMATION_DICT,
            'leg': LEG_ANIMATION_DICT
        })
        actor.attach("head", "torso", "joint34")
        actor.attach("torso", "leg", "joint_pelvis")

        treads = loader.load_model(TREADS_MODEL)
        axle = actor.find('**/joint_axle')
        treads.reparent_to(axle)

        return actor

    def get_animation_names(self):
        """Returns a list of valid animations for the actor."""
        return ANIMATION_NAME_DICT
