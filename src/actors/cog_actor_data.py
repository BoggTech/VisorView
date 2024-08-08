import os
import posixpath
import src.util.vfs_glob as glob
from panda3d.core import Filename, Vec4, VBase4
from direct.actor.Actor import Actor
from src.actors.actor_data import ActorData

SUIT_MODELS = {"a": Filename("phase_3.5/models/char/tt_a_ene_cga_zero.bam"),
               "b": Filename("phase_3.5/models/char/tt_a_ene_cgb_zero.bam"),
               "c": Filename("phase_3.5/models/char/tt_a_ene_cgc_zero.bam")}

SUIT_HEAD_DICT = {"a": Filename("phase_4/models/char/suitA-"),
                  "b": Filename("phase_4/models/char/suitB-"),
                  "c": Filename("phase_3.5/models/char/suitC-"),
                  }

DEPARTMENTS = ("sell", "cash", "law", "boss")
DEPARTMENT_NAME_DICT = {"sell": "s", "cash": "m", "law": "l", "boss": "c"}
MEDALLION_NAME_DICT = {"sell": "SalesIcon", "cash": "MoneyIcon", "law": "LegalIcon", "boss": "CorpIcon"}
SUPERVISOR_NAME_DICT = {"sell": "sellbotForeman", "cash": "cashbotAuditor", "law": "lawbotClerk",
                        "boss": "bossbotClubPresident"}
DEPARTMENT_HAND_DICT = {"sell": VBase4(0.95, 0.75, 0.95, 1.0), "cash": VBase4(0.65, 0.95, 0.85, 1.0),
                        "law": VBase4(0.75, 0.75, 0.95, 1.0), "boss": VBase4(0.95, 0.75, 0.75, 1.0)}

COG_ICONS = Filename("phase_3/models/gui/ttr_m_gui_gen_cogIcons.bam")
COG_ICON_POS_HPR_SCALE = (0.02, 0.05, 0.04,
                          180.00, 0.00, 0.00,
                          0.51, 0.51, 0.51)

MEDALLION_COLORS = {
    'boss': Vec4(0.863, 0.776, 0.769, 1.000),
    'sell': Vec4(0.843, 0.745, 0.745, 1.000),
    'law': Vec4(0.749, 0.776, 0.824, 1.000),
    'cash': Vec4(0.749, 0.769, 0.749, 1.000),
}

SUIT_ANIMATION_PATHS = {"a": glob.glob(posixpath.join("phase_*", "models", "char", "tt_a_ene_cga_*.bam")),
                        "b": glob.glob(posixpath.join("phase_*", "models", "char", "tt_a_ene_cgb_*.bam")),
                        "c": glob.glob(posixpath.join("phase_*", "models", "char", "tt_a_ene_cgc_*.bam"))}

SUIT_ANIMATION_DICTS = {"a": {}, "b": {}, "c": {}}

# split em up into dictionaries for the actor
for i in range(0, len(SUIT_ANIMATION_PATHS["a"])):
    SUIT_ANIMATION_DICTS["a"][os.path.basename(SUIT_ANIMATION_PATHS["a"][i])[13:-4]] = SUIT_ANIMATION_PATHS["a"][i]

for i in range(0, len(SUIT_ANIMATION_PATHS["b"])):
    SUIT_ANIMATION_DICTS["b"][os.path.basename(SUIT_ANIMATION_PATHS["b"][i])[13:-4]] = SUIT_ANIMATION_PATHS["b"][i]

for i in range(0, len(SUIT_ANIMATION_PATHS["c"])):
    SUIT_ANIMATION_DICTS["c"][os.path.basename(SUIT_ANIMATION_PATHS["c"][i])[13:-4]] = SUIT_ANIMATION_PATHS["c"][i]

SUIT_ANIMATIONS = {"a": list(SUIT_ANIMATION_DICTS["a"]),
                   "b": list(SUIT_ANIMATION_DICTS["b"]),
                   "c": list(SUIT_ANIMATION_DICTS["c"])}
[SUIT_ANIMATIONS[x].sort() for x in SUIT_ANIMATIONS.keys()]


class CogActorData(ActorData):
    """Class that stores data for and generates Toontown Rewritten cog actors."""
    actor_type = "cog"
    has_shadow = True
    shadow_node = "**/def_shadow"

    def __init__(self, name, department, suit_type, scale, hand_color=None, head_path=None, head_nodes=None,
                 head_color=None, head_texture=None, is_supervisor=False):
        """Initializes the CogActor instance.

        :param name: The name of the cog.
        :param department: The department of the cog (sell, cash, law or boss)
        :param suit_type: The suit type of the cog (a, b or c).
        :param scale: The scale of the cog.
        :param hand_color: The hand color of the cog. Has defaults based on department.
        :param head_path: The path to the head of the cog. Defaults to default model for the suit type.
        :param head_nodes: The node(s) to show for the head. Can be a string or list of strings. "*" by default.
        :param head_color: The color of the head. Not applied by default.
        :param is_supervisor: If the cog should use supervisor suit textures or not. Defaults to False.
        """
        super().__init__()
        head_nodes = ["*"] if head_nodes is None else head_nodes
        head_nodes = [head_nodes] if not isinstance(head_nodes, list) else head_nodes
        head_path = SUIT_HEAD_DICT[suit_type] + "heads.bam" if head_path is None else head_path
        hand_color = DEPARTMENT_HAND_DICT[department] if hand_color is None else hand_color
        self.set_name(name)
        self.add_data("department", department)
        self.add_data("suit_type", suit_type)
        self.add_data("scale", scale)
        self.add_data("hand_color", hand_color)
        self.add_data("head_path", head_path)
        self.add_data("head_nodes", head_nodes)
        self.add_data("head_color", head_color)
        self.add_data("head_texture", head_texture)
        self.add_data("is_supervisor", is_supervisor)

    def get_suit_textures(self, department, is_supervisor):
        """Returns a dict of textures for a based on provided parameters. Returns None for invalid parameters.

        :param department: Department name: sell, cash, law or boss.
        :param is_supervisor: True if the cog is a Supervisor.
        """
        department = department.lower()
        if department not in DEPARTMENTS:
            return None

        if is_supervisor:
            prefix = "phase_3.5/maps/ttr_t_ene_"
            abbr = SUPERVISOR_NAME_DICT[department]
        else:
            prefix = "phase_3.5/maps/"
            abbr = DEPARTMENT_NAME_DICT[department]

        texture_dict = {"arm": Filename(prefix + abbr + "_arm.jpg"),
                        "blazer": Filename(prefix + abbr + "_blazer.jpg"),
                        "leg": Filename(prefix + abbr + "_leg.jpg"),
                        "sleeve": Filename(prefix + abbr + "_sleeve.jpg")}

        return texture_dict

    def get_animation_names(self):
        """Returns a list of animation names for this actor."""
        suit_type = self.get_data("suit_type")
        return None if suit_type is None else {'modelRoot': SUIT_ANIMATIONS[suit_type]}

    def generate_actor(self):
        """Method that generates and returns the full cog as an actor, animations included."""
        # Begin by creating the suit + applying the appropriate textures
        suit_type = self.get_data("suit_type")
        suit_model_path = SUIT_MODELS[suit_type]
        suit_animation_dict = SUIT_ANIMATION_DICTS[suit_type]
        cog = Actor(suit_model_path, suit_animation_dict)
        is_supervisor = self.get_data("is_supervisor")
        department = self.get_data("department")
        texture_dict = self.get_suit_textures(department, is_supervisor)
        if texture_dict is not None:
            tx_blazer = loader.load_texture(texture_dict["blazer"])
            tx_leg = loader.load_texture(texture_dict["leg"])
            tx_sleeve = loader.load_texture(texture_dict["sleeve"])
            cog.find('**/torso').set_texture(tx_blazer, 1)
            cog.find('**/legs').set_texture(tx_leg, 1)
            cog.find('**/arms').set_texture(tx_sleeve, 1)

        # Load and attach head
        head_path = self.get_data("head_path")
        head_nodes = self.get_data("head_nodes")
        head_color = self.get_data("head_color")
        head_texture = self.get_data("head_texture")
        head_model = loader.load_model(head_path)
        head_null = cog.find('**/def_head')
        [head_model.find(head_node).copy_to(head_null) for head_node in head_nodes]
        head_model.remove_node()
        if head_color is not None:
            head_null.set_color(head_color)
        if head_texture is not None:
            head_tx = loader.load_texture(head_texture)
            head_null.set_texture(head_tx, 1)


        # Load and attach insignia
        chest_null = cog.find("**/def_joint_attachMeter")
        icons = loader.load_model(COG_ICONS)
        medallion = icons.find('**/' + MEDALLION_NAME_DICT[department]).copy_to(chest_null)
        medallion.set_pos_hpr_scale(*COG_ICON_POS_HPR_SCALE)
        medallion.set_color(MEDALLION_COLORS[department])

        # Apply hand color
        hand_color = self.get_data("hand_color")
        cog.find('**/hands').set_color(hand_color)

        # Apply scale
        scale = self.get_data("scale")
        cog.set_scale(scale)

        # adjust rotation
        cog.set_h(180)

        # Return final actor
        return cog
