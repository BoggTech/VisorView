from src.actors.cog_actor_data import *
from panda3d.core import Texture

SKELECOG_MODELS = {"a": Filename("phase_5/models/char/tt_a_ene_sca_zero.bam"),
                   "b": Filename("phase_5/models/char/tt_a_ene_scb_zero.bam"),
                   "c": Filename("phase_5/models/char/tt_a_ene_scc_zero.bam")}

TIE_DICT = {"sell": "phase_5/maps/cog_robot_tie_sales.jpg",
            "cash": "phase_5/maps/cog_robot_tie_money.jpg",
            "law":  "phase_5/maps/cog_robot_tie_legal.jpg",
            "boss": "phase_5/maps/cog_robot_tie_boss.jpg",}

def make_skelecog_data_from_cog_data(cog_data):
    """Method that creates a SkelecogActorData instance from CogActorData"""
    name = cog_data.get_name()
    department = cog_data.get_data("department")
    suit_type = cog_data.get_data("suit_type")
    scale = cog_data.get_data("scale")
    return SkelecogActorData(name, department, suit_type, scale)


class SkelecogActorData(CogActorData):
    """Class that stores data for and generates Toontown Rewritten cog actors."""
    _actor_type = "skelecog"

    def __init__(self, name, department=None, suit_type=None, scale=None):
        """Initializes the SkelecogActorData instance.

        :param name: The name of the cog.
        :param department: The department of the cog (sell, cash, law or boss)
        :param suit_type: The suit type of the cog (a, b or c).
        :param scale: The scale of the cog."""

        super().__init__(name, department, suit_type, scale)

    def generate_actor(self):
        """Returns an actor based on the data within this class."""
        department = self.get_data("department")
        suit_type = self.get_data("suit_type")
        scale = self.get_data("scale")

        cog = Actor(SKELECOG_MODELS[suit_type], SUIT_ANIMATION_DICTS[suit_type])

        # Load and attach insignia
        chest_null = cog.find("**/def_joint_attachMeter")
        icons = loader.load_model(COG_ICONS)
        medallion = icons.find('**/' + MEDALLION_NAME_DICT[department]).copy_to(chest_null)
        medallion.set_pos_hpr_scale(*COG_ICON_POS_HPR_SCALE)
        medallion.set_color(MEDALLION_COLORS[department])

        # generate tie
        tie = cog.find('**/tie')
        tie_texture = loader.load_texture(TIE_DICT[department])
        tie_texture.set_minfilter(Texture.FTLinearMipmapLinear)
        tie_texture.set_magfilter(Texture.FTLinear)
        tie.set_texture(tie_texture, 1)

        # Apply scale
        cog.set_scale(scale)

        # adjust rotation
        cog.set_h(180)

        # Return final actor
        return cog
