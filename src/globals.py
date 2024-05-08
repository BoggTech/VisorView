import os
import glob

DEFAULT_POS = (0,0,0)
DEFAULT_HPR = (180,0,0)

DEFAULT_CAMERA_POS = (0,-20,4.2)

SCREENSHOT_DIR = "../screenshots"
RESOURCES_DIR = "../resources"
CONFIG_DIR = "../VisorConfig.prc"

SUIT_A_MODEL = os.path.join(RESOURCES_DIR,"phase_3.5","models","char","tt_a_ene_cga_zero.bam")
SUIT_B_MODEL = os.path.join(RESOURCES_DIR,"phase_3.5","models","char","tt_a_ene_cgb_zero.bam")
SUIT_C_MODEL = os.path.join(RESOURCES_DIR,"phase_3.5","models","char","tt_a_ene_cgc_zero.bam")

SHADOW_MODEL = os.path.join(RESOURCES_DIR,"phase_3","models","props","drop_shadow.bam")
SHADOW_SCALE = 0.45
SHADOW_COLOR = (0.0, 0.0, 0.0, 0.5)

COG_ICONS = os.path.join(RESOURCES_DIR,"phase_3","models","gui","ttr_m_gui_gen_cogIcons.bam")
COG_ICON_POS_HPR_SCALE = (0.02, 0.05, 0.04,
                            180.00, 0.00, 0.00,
                            0.51, 0.51, 0.51)

SHOE_TEXTURE = os.path.join(RESOURCES_DIR,"phase_3.5","maps","shoe.jpg")
HAND_TEXTURE = os.path.join(RESOURCES_DIR,"phase_3.5","maps","hand.jpg")
ARM_TEXTURE = os.path.join(RESOURCES_DIR,"phase_3.5","maps","s_arm.jpg")

SUIT_A_ANIMATION_PATHS = glob.glob(os.path.join(RESOURCES_DIR,"**","tt_a_ene_cga_*.bam"), recursive=True)
SUIT_B_ANIMATION_PATHS = glob.glob(os.path.join(RESOURCES_DIR,"**","tt_a_ene_cgb_*.bam"), recursive=True)
SUIT_C_ANIMATION_PATHS = glob.glob(os.path.join(RESOURCES_DIR,"**","tt_a_ene_cgc_*.bam"), recursive=True)

SUIT_A_ANIMATION_DICT = {}
SUIT_B_ANIMATION_DICT = {}
SUIT_C_ANIMATION_DICT = {}

# split em up into dictionaries for the actor
for i in range(0, len(SUIT_A_ANIMATION_PATHS)):
    SUIT_A_ANIMATION_DICT[os.path.basename(SUIT_A_ANIMATION_PATHS[i])[13:-4]] = SUIT_A_ANIMATION_PATHS[i]

for i in range(0, len(SUIT_B_ANIMATION_PATHS)):
    SUIT_B_ANIMATION_DICT[os.path.basename(SUIT_B_ANIMATION_PATHS[i])[13:-4]] = SUIT_B_ANIMATION_PATHS[i]

for i in range(0, len(SUIT_C_ANIMATION_PATHS)):
    SUIT_C_ANIMATION_DICT[os.path.basename(SUIT_C_ANIMATION_PATHS[i])[13:-4]] = SUIT_C_ANIMATION_PATHS[i]

SUIT_A_ANIMATIONS = list(SUIT_A_ANIMATION_DICT)
SUIT_B_ANIMATIONS = list(SUIT_B_ANIMATION_DICT)
SUIT_C_ANIMATIONS = list(SUIT_C_ANIMATION_DICT)
SUIT_A_ANIMATIONS.sort()
SUIT_B_ANIMATIONS.sort()
SUIT_C_ANIMATIONS.sort()

COG_DATA = {
"foreman": {"blazer": os.path.join(RESOURCES_DIR,"phase_3.5","maps","ttr_t_ene_sellbotForeman_blazer.jpg"),
           "leg": os.path.join(RESOURCES_DIR,"phase_3.5","maps","ttr_t_ene_sellbotForeman_leg.jpg"),
           "sleeve": os.path.join(RESOURCES_DIR,"phase_3.5","maps","ttr_t_ene_sellbotForeman_sleeve.jpg"),
           "head": os.path.join(RESOURCES_DIR,"phase_4","models","char","ttr_m_ene_sellbotForeman.bam"),
           "hands": (0.886,0.737,0.784,1.0),
           "scale": 1.148,
           "suit": "b",
           "emblem": "SalesIcon" },

"foreman_angry": {"blazer": os.path.join(RESOURCES_DIR,"phase_3.5","maps","ttr_t_ene_sellbotForeman_blazer.jpg"),
           "leg": os.path.join(RESOURCES_DIR,"phase_3.5","maps","ttr_t_ene_sellbotForeman_leg.jpg"),
           "sleeve": os.path.join(RESOURCES_DIR,"phase_3.5","maps","ttr_t_ene_sellbotForeman_sleeve.jpg"),
           "head": os.path.join(RESOURCES_DIR,"phase_4","models","char","ttr_m_ene_sellbotForemanAngry.bam"),
           "hands": (0.886,0.737,0.784,1.0),
           "scale": 1.148,
           "suit": "b",
           "emblem": "SalesIcon" },

"auditor": {"blazer": os.path.join(RESOURCES_DIR,"phase_3.5","maps","ttr_t_ene_cashbotAuditor_blazer.jpg"),
           "leg": os.path.join(RESOURCES_DIR,"phase_3.5","maps","ttr_t_ene_cashbotAuditor_leg.jpg"),
           "sleeve": os.path.join(RESOURCES_DIR,"phase_3.5","maps","ttr_t_ene_cashbotAuditor_sleeve.jpg"),
           "head": os.path.join(RESOURCES_DIR,"phase_4","models","char","ttr_m_ene_cashbotAuditor.bam"),
           "hands": (0.686,0.882,0.831,1.0),
           "scale": 1.378,
           "suit": "c",
           "emblem": "MoneyIcon" },

"clerk": {"blazer": os.path.join(RESOURCES_DIR,"phase_3.5","maps","ttr_t_ene_lawbotClerk_blazer.jpg"),
           "leg": os.path.join(RESOURCES_DIR,"phase_3.5","maps","ttr_t_ene_lawbotClerk_leg.jpg"),
           "sleeve": os.path.join(RESOURCES_DIR,"phase_3.5","maps","ttr_t_ene_lawbotClerk_sleeve.jpg"),
           "head": os.path.join(RESOURCES_DIR,"phase_4","models","char","ttr_m_ene_lawbotClerk.bam"),
           "hands": (0.722,0.769,0.816,1.0),
           "scale": 1.323,
           "suit": "b",
           "emblem": "LegalIcon" },

"club_president": {"blazer": os.path.join(RESOURCES_DIR,"phase_3.5","maps","ttr_t_ene_bossbotClubPresident_blazer.jpg"),
           "leg": os.path.join(RESOURCES_DIR,"phase_3.5","maps","ttr_t_ene_bossbotClubPresident_leg.jpg"),
           "sleeve": os.path.join(RESOURCES_DIR,"phase_3.5","maps","ttr_t_ene_bossbotClubPresident_sleeve.jpg"),
           "head": os.path.join(RESOURCES_DIR,"phase_4","models","char","ttr_m_ene_bossbotClubPresident.bam"),
           "hands": (0.950,0.750,0.750,1.0),
           "scale": 0.706,
           "suit": "a",
           "emblem": "CorpIcon" }
}

