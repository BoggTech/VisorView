import os, glob
import src.globals as globals
from panda3d.core import Filename, Loader
from direct.actor.Actor import Actor
from src.actors.actor_base import ActorBase

SUIT_MODELS = {"a": Filename(globals.RESOURCES_DIR + "/phase_3.5/models/char/tt_a_ene_cga_zero.bam"),
               "b": Filename(globals.RESOURCES_DIR + "/phase_3.5/models/char/tt_a_ene_cgb_zero.bam"),
               "c": Filename(globals.RESOURCES_DIR + "/phase_3.5/models/char/tt_a_ene_cgc_zero.bam")}

DEPARTMENTS = ("sell", "cash", "law", "boss")
DEPARTMENT_NAME_DICT = {"sell": "s", "cash": "m", "law": "l", "boss": "c"}
MEDALLION_NAME_DICT = {"sell": "SalesIcon", "cash": "MoneyIcon", "law": "LegalIcon", "boss": "CorpIcon"}
SUPERVISOR_NAME_DICT = {"sell": "sellbotForeman", "cash": "cashbotAuditor", "law": "lawbotClerk",
                        "boss": "bossbotClubPresident"}

COG_ICONS = Filename(globals.RESOURCES_DIR + "/phase_3/models/gui/ttr_m_gui_gen_cogIcons.bam")
COG_ICON_POS_HPR_SCALE = (0.02, 0.05, 0.04,
                          180.00, 0.00, 0.00,
                          0.51, 0.51, 0.51)

SUIT_ANIMATION_PATHS = {"a": glob.glob(os.path.join(globals.RESOURCES_DIR, "**", "tt_a_ene_cga_*.bam"), recursive=True),
                        "b": glob.glob(os.path.join(globals.RESOURCES_DIR, "**", "tt_a_ene_cgb_*.bam"), recursive=True),
                        "c": glob.glob(os.path.join(globals.RESOURCES_DIR, "**", "tt_a_ene_cgc_*.bam"), recursive=True)}

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


class CogActor(ActorBase):
    """Class that stores data for and generates Toontown Rewritten cog actors."""
    has_shadow = True
    shadow_node = "**/def_shadow"

    def __init__(self, name, department, suit_type, scale, hand_color, head_path, head_node="*", is_supervisor=False):
        super().__init__()
        self.set_name(name)
        self.add_data("department", department)
        self.add_data("suit_type", suit_type)
        self.add_data("scale", scale)
        self.add_data("hand_color", hand_color)
        self.add_data("head_path", head_path)
        self.add_data("head_node", head_node)
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
            prefix = "/phase_3.5/maps/ttr_t_ene_"
            abbr = SUPERVISOR_NAME_DICT[department]
        else:
            prefix = "/phase_3.5/maps/"
            abbr = DEPARTMENT_NAME_DICT[department]

        texture_dict = {"arm": Filename(globals.RESOURCES_DIR + prefix + abbr + "_arm.jpg"),
                        "blazer": Filename(globals.RESOURCES_DIR + prefix + abbr + "_blazer.jpg"),
                        "leg": Filename(globals.RESOURCES_DIR + prefix + abbr + "_leg.jpg"),
                        "sleeve": Filename(globals.RESOURCES_DIR + prefix + abbr + "_sleeve.jpg")}

        return texture_dict

    def get_animations(self):
        suit_type = self.get_data("suit_type")
        return None if suit_type is None else SUIT_ANIMATIONS[suit_type]

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
        head_node = self.get_data("head_node")
        head_model = loader.load_model(head_path)
        head_null = cog.find('**/def_head')
        head_model.find(head_node).copy_to(head_null)
        head_model.remove_node()

        # Load and attach insignia
        chest_null = cog.find("**/def_joint_attachMeter")
        icons = loader.load_model(COG_ICONS)
        medallion = icons.find('**/' + MEDALLION_NAME_DICT[department]).copy_to(chest_null)
        medallion.set_pos_hpr_scale(*COG_ICON_POS_HPR_SCALE)

        # Apply hand color
        hand_color = self.get_data("hand_color")
        cog.find('**/hands').set_color(hand_color)

        # Apply scale
        scale = self.get_data("scale")
        cog.set_scale(scale)

        cog.set_h(180)

        # Return final actor
        return cog
