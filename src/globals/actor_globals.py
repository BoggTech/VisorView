from panda3d.core import VBase4
from src.actors.cog_actor_data import CogActorData
from src.actors.goon_actor_data import GoonActorData
from src.actors.generic_actor_data import GenericActorData
from src.actors.boss_actor_data import BossActorData

A_SIZE = 6.06
B_SIZE = 5.29
C_SIZE = 4.14
BOSS_HANDS = VBase4(0.95, 0.75, 0.75, 1.0)
LAW_HANDS = VBase4(0.75, 0.75, 0.95, 1.0)
CASH_HANDS = VBase4(0.65, 0.95, 0.85, 1.0)
SELL_HANDS = VBase4(0.95, 0.75, 0.95, 1.0)
HEAD_PREFIX_4 = "phase_4/maps/"
HEAD_PREFIX_3_5 = "phase_3.5/maps/"

SUPERVISORS = [
    CogActorData("Factory Foreman (Neutral)", "sell", "b", 6.05 / B_SIZE, (0.886, 0.737, 0.784, 1.0), "phase_4/models/char/ttr_m_ene_sellbotForeman.bam", is_supervisor=True),
    CogActorData("Factory Foreman (Angry)", "sell", "b", 6.05 / B_SIZE, (0.886, 0.737, 0.784, 1.0), "phase_4/models/char/ttr_m_ene_sellbotForemanAngry.bam", is_supervisor=True),
    CogActorData("Mint Auditor", "cash", "c", 5.7 / C_SIZE, (0.686, 0.882, 0.831, 1.0), "phase_4/models/char/ttr_m_ene_cashbotAuditor.bam", is_supervisor=True),
    CogActorData("Office Clerk", "law", "b", 7 / B_SIZE, (0.722, 0.769, 0.816, 1.0), "phase_4/models/char/ttr_m_ene_lawbotClerk.bam", is_supervisor=True),
    CogActorData("Club President", "boss", "a", 4.65 / A_SIZE, (0.950, 0.750, 0.750, 1.0), "phase_4/models/char/ttr_m_ene_bossbotClubPresident.bam", is_supervisor=True)
]

BOSSES = [
    BossActorData("Senior Vice President (VP)", "sell", 1),
    BossActorData("Chief Financial Officer (CFO)", "cash", 1),
    BossActorData("Chief Justice (CJ)", "law", 1),
    BossActorData("Chief Executive Officer (CEO)", "boss", 1),
]

SELLBOTS = [
    CogActorData("Cold Caller", "sell", "c", 3.5 / C_SIZE, VBase4(0.55, 0.65, 1.0, 1.0), head_nodes="**/coldcaller", head_color=VBase4(0.25, 0.35, 1.0, 1.0)),
    CogActorData("Telemarketer", "sell", "b", 3.75 / B_SIZE, head_nodes="**/telemarketer", ),
    CogActorData("Name Dropper", "sell", "a", 4.35 / A_SIZE, head_nodes="**/numbercruncher", head_texture=HEAD_PREFIX_4 + "name-dropper.jpg"),
    CogActorData("Glad Hander", "sell", "c", 4.75 / C_SIZE, head_nodes="**/gladhander", ),
    CogActorData("Mover & Shaker", "sell", "b", 4.75 / B_SIZE, head_nodes="**/movershaker", ),
    CogActorData("Two-Face", "sell", "a", 5.25 / A_SIZE, head_nodes="**/twoface", ),
    CogActorData("The Mingler", "sell", "a", 5.75 / A_SIZE, head_nodes="**/twoface", head_texture=HEAD_PREFIX_4 + "mingler.jpg"),
    CogActorData("Mr. Hollywood", "sell", "a", 7.0 / A_SIZE, head_nodes="**/yesman"),
    SUPERVISORS[0],  # foreman (neutral)
    SUPERVISORS[1],   # foreman (angry)
    BOSSES[0]  # vp
]

CASHBOTS = [
    CogActorData('Short Change', 'cash', 'c', 3.6 / C_SIZE, head_nodes='**/coldcaller'),
    CogActorData('Penny Pincher', 'cash', 'a', 3.55 / A_SIZE, VBase4(1.0, 0.5, 0.6, 1.0), head_nodes='**/pennypincher'),
    CogActorData('Tightwad', 'cash', 'c', 4.5 / C_SIZE, head_nodes='**/tightwad'),
    CogActorData('Bean Counter', 'cash', 'b', 4.4 / B_SIZE, head_nodes='**/beancounter'),
    CogActorData('Number Cruncher', 'cash', 'a', 5.25 / A_SIZE, head_nodes='**/numbercruncher'),
    CogActorData('Money Bags', 'cash', 'c', 5.3 / C_SIZE, head_nodes='**/moneybags'),
    CogActorData('Loan Shark', 'cash', 'b', 6.5 / B_SIZE, VBase4(0.5, 0.85, 0.75, 1.0), head_nodes='**/loanshark'),
    CogActorData('Robber Baron', 'cash', 'a', 7.0 / A_SIZE, head_nodes='**/yesman', head_texture=HEAD_PREFIX_4 + 'robber-baron.jpg'),
    SUPERVISORS[2],  # auditor
    BOSSES[1]  # cfo
]

LAWBOTS = [
    CogActorData('Bottom Feeder', 'law', 'c', 4.0 / C_SIZE, head_nodes='**/tightwad', head_texture=HEAD_PREFIX_3_5 + 'bottom-feeder.jpg'),
    CogActorData('Bloodsucker', 'law', 'b', 4.375 / B_SIZE, VBase4(0.95, 0.95, 1.0, 1.0), head_nodes='**/movershaker', head_texture=HEAD_PREFIX_4 + 'blood-sucker.jpg'),
    CogActorData('Double Talker', 'law', 'a', 4.25 / A_SIZE, head_nodes='**/twoface', head_texture=HEAD_PREFIX_4 + 'double-talker.jpg'),
    CogActorData('Ambulance Chaser', 'law', 'b', 4.35 / B_SIZE, head_nodes='**/ambulancechaser'),
    CogActorData('Back Stabber', 'law', 'a', 4.5 / A_SIZE, head_nodes='**/backstabber'),
    CogActorData('Spin Doctor', 'law', 'b', 5.65 / B_SIZE, VBase4(0.5, 0.8, 0.75, 1.0), head_nodes='**/telemarketer', head_texture=HEAD_PREFIX_4 + 'spin-doctor.jpg'),
    CogActorData('Legal Eagle', 'law', 'a', 7.125 / A_SIZE, VBase4(0.25, 0.25, 0.5, 1.0), head_nodes='**/legaleagle'),
    CogActorData('Big Wig', 'law', 'a', 7.0 / A_SIZE, head_nodes='**/bigwig'),
    SUPERVISORS[3],  # clerk
    BOSSES[2]  # cj
]

BOSSBOTS = [
    CogActorData('Flunky', 'boss', 'c', 4.0 / C_SIZE, head_nodes=["**/flunky", "**/glasses"]),
    CogActorData('Pencil Pusher', 'boss', 'b', 3.35 / B_SIZE, head_nodes='**/pencilpusher'),
    CogActorData('Yesman', 'boss', 'a', 4.125 / A_SIZE, head_nodes='**/yesman'),
    CogActorData('Micromanager', 'boss', 'c', 2.5 / C_SIZE, head_nodes='**/micromanager'),
    CogActorData('Downsizer', 'boss', 'b', 4.5 / B_SIZE, head_nodes='**/beancounter'),
    CogActorData('Head Hunter', 'boss', 'a', 6.5 / A_SIZE, head_nodes='**/headhunter'),
    CogActorData('Corporate Raider', 'boss', 'c', 6.75 / C_SIZE, VBase4(0.85, 0.55, 0.55, 1.0), head_nodes='**/flunky', head_texture=HEAD_PREFIX_3_5 + 'corporate-raider.jpg'),
    CogActorData('The Big Cheese', 'boss', 'a', 7.0 / A_SIZE, VBase4(0.75, 0.95, 0.75, 1.0), head_nodes='**/bigcheese'),
    SUPERVISORS[4],  # club president,
    BOSSES[3]  # ceo
]

MISC = [
    GoonActorData("Construction Goon (Yellow)"),
    GoonActorData("Construction Goon (Orange)", (0.75, 0.35, 0.1, 1.0), 1.3),
    GoonActorData("Construction Goon (Red)", (0.95, 0.0, 0.0, 1.0), 1.6),
    GoonActorData("Security Goon (Blue)", (0.47, 0.55, 1.0, 1.0), 3.5, is_security=True),
    GoonActorData("Security Goon (Purple)", (0.51, 0.23, 0.75, 1.0), 3.5, is_security=True),
    GenericActorData("The Boiler", "phase_5/models/char/ttr_r_chr_cbg_boss.bam", "ttr_a_chr_cbg_boss_", .5),
    GenericActorData("Sellbot Field Office", "phase_5/models/char/ttr_r_ara_cbe_cogdoSell.bam", "ttr_a_ara_cbe_cogdoSell_", .5)
]

ACTORS = {"supervisors": SUPERVISORS,
          "sellbots": SELLBOTS,
          "cashbots": CASHBOTS,
          "lawbots": LAWBOTS,
          "bossbots": BOSSBOTS,
          "bosses": BOSSES,
          "misc": MISC
          }

COG_SET_NAMES = ["supervisors", "sellbots", "cashbots", "lawbots", "bossbots", "bosses", "misc"]