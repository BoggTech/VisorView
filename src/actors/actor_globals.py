from panda3d.core import VBase4
from src.actors.cog_actor import CogActor
from src.globals import RESOURCES_DIR

A_SIZE = 6.06
B_SIZE = 5.29
C_SIZE = 4.14
BOSS_HANDS = VBase4(0.95, 0.75, 0.75, 1.0)
LAW_HANDS = VBase4(0.75, 0.75, 0.95, 1.0)
CASH_HANDS = VBase4(0.65, 0.95, 0.85, 1.0)
SELL_HANDS = VBase4(0.95, 0.75, 0.95, 1.0)
HEAD_PREFIX_4 = RESOURCES_DIR + "/phase_4/maps/"
HEAD_PREFIX_3_5 = RESOURCES_DIR + "/phase_3.5/maps/"

SUPERVISORS = [
    CogActor("Factory Foreman (Neutral)", "sell", "b", 1.148, (0.886, 0.737, 0.784, 1.0), RESOURCES_DIR + "/phase_4/models/char/ttr_m_ene_sellbotForeman.bam", is_supervisor=True),
    CogActor("Factory Foreman (Angry)", "sell", "b", 1.148, (0.886, 0.737, 0.784, 1.0), RESOURCES_DIR + "/phase_4/models/char/ttr_m_ene_sellbotForemanAngry.bam", is_supervisor=True),
    CogActor("Mint Auditor", "cash", "c", 1.378, (0.686, 0.882, 0.831, 1.0), RESOURCES_DIR + "/phase_4/models/char/ttr_m_ene_cashbotAuditor.bam", is_supervisor=True),
    CogActor("Office Clerk", "law", "b", 1.323, (0.722, 0.769, 0.816, 1.0), RESOURCES_DIR + "/phase_4/models/char/ttr_m_ene_lawbotClerk.bam", is_supervisor=True),
    CogActor("Club President", "boss", "a", 0.706, (0.950, 0.750, 0.750, 1.0), RESOURCES_DIR + "/phase_4/models/char/ttr_m_ene_bossbotClubPresident.bam", is_supervisor=True)
]

SELLBOTS = [
    CogActor("Cold Caller", "sell", "c", 3.5 / C_SIZE, VBase4(0.55, 0.65, 1.0, 1.0), head_nodes="**/coldcaller", head_color=VBase4(0.25, 0.35, 1.0, 1.0)),
    CogActor("Telemarketer", "sell", "b", 3.75 / B_SIZE, head_nodes="**/telemarketer", ),
    CogActor("Name Dropper", "sell", "a", 4.35 / A_SIZE, head_nodes="**/numbercruncher", head_texture=HEAD_PREFIX_4 + "name-dropper.jpg"),
    CogActor("Glad Hander", "sell", "c", 4.75 / C_SIZE, head_nodes="**/gladhander", ),
    CogActor("Mover & Shaker", "sell", "b", 4.75 / B_SIZE, head_nodes="**/movershaker", ),
    CogActor("Two-Face", "sell", "a", 5.25 / A_SIZE, head_nodes="**/twoface", ),
    CogActor("The Mingler", "sell", "a", 5.75 / A_SIZE, head_nodes="**/twoface", head_texture=HEAD_PREFIX_4 + "mingler.jpg"),
    CogActor("Mr. Hollywood", "sell", "a", 7.0 / A_SIZE, head_nodes="**/yesman"),
    SUPERVISORS[0],  # foreman (neutral)
    SUPERVISORS[1]   # foreman (angry)
]

CASHBOTS = [
    CogActor('Short Change', 'cash', 'c', 3.6 / C_SIZE, head_nodes='**/coldcaller'),
    CogActor('Penny Pincher', 'cash', 'a', 3.55 / A_SIZE, VBase4(1.0, 0.5, 0.6, 1.0), head_nodes='**/pennypincher'),
    CogActor('Tightwad', 'cash', 'c', 4.5 / C_SIZE, head_nodes='**/tightwad'),
    CogActor('Bean Counter', 'cash', 'b', 4.4 / B_SIZE, head_nodes='**/beancounter'),
    CogActor('Number Cruncher', 'cash', 'a', 5.25 / A_SIZE, head_nodes='**/numbercruncher'),
    CogActor('Money Bags', 'cash', 'c', 5.3 / C_SIZE, head_nodes='**/moneybags'),
    CogActor('Loan Shark', 'cash', 'b', 6.5 / B_SIZE, VBase4(0.5, 0.85, 0.75, 1.0), head_nodes='**/loanshark'),
    CogActor('Robber Baron', 'cash', 'a', 7.0 / A_SIZE, head_nodes='**/yesman', head_texture=HEAD_PREFIX_4 + 'robber-baron.jpg'),
    SUPERVISORS[2]  # auditor
]

LAWBOTS = [
    CogActor('Bottom Feeder', 'law', 'c', 4.0 / C_SIZE, head_nodes='**/tightwad', head_texture=HEAD_PREFIX_3_5 + 'bottom-feeder.jpg'),
    CogActor('Bloodsucker', 'law', 'b', 4.375 / B_SIZE, VBase4(0.95, 0.95, 1.0, 1.0), head_nodes='**/movershaker', head_texture=HEAD_PREFIX_4 + 'blood-sucker.jpg'),
    CogActor('Double Talker', 'law', 'a', 4.25 / A_SIZE, head_nodes='**/twoface', head_texture=HEAD_PREFIX_4 + 'double-talker.jpg'),
    CogActor('Ambulance Chaser', 'law', 'b', 4.35 / B_SIZE, head_nodes='**/ambulancechaser'),
    CogActor('Back Stabber', 'law', 'a', 4.5 / A_SIZE, head_nodes='**/backstabber'),
    CogActor('Spin Doctor', 'law', 'b', 5.65 / B_SIZE, VBase4(0.5, 0.8, 0.75, 1.0), head_nodes='**/telemarketer', head_texture=HEAD_PREFIX_4 + 'spin-doctor.jpg'),
    CogActor('Legal Eagle', 'law', 'a', 7.125 / A_SIZE, VBase4(0.25, 0.25, 0.5, 1.0), head_nodes='**/legaleagle'),
    CogActor('Big Wig', 'law', 'a', 7.0 / A_SIZE, head_nodes='**/bigwig'),
    SUPERVISORS[3]  # clerk
]

BOSSBOTS = [
    CogActor('Flunky', 'boss', 'c', 4.0 / C_SIZE, head_nodes=["**/flunky", "**/glasses"]),
    CogActor('Pencil Pusher', 'boss', 'b', 3.35 / B_SIZE, head_nodes='**/pencilpusher'),
    CogActor('Yesman', 'boss', 'a', 4.125 / A_SIZE, head_nodes='**/yesman'),
    CogActor('Micromanager', 'boss', 'c', 2.5 / C_SIZE, head_nodes='**/micromanager'),
    CogActor('Downsizer', 'boss', 'b', 4.5 / B_SIZE, head_nodes='**/beancounter'),
    CogActor('Head Hunter', 'boss', 'a', 6.5 / A_SIZE, head_nodes='**/headhunter'),
    CogActor('Corporate Raider', 'boss', 'c', 6.75 / C_SIZE, VBase4(0.85, 0.55, 0.55, 1.0), head_nodes='**/flunky', head_texture=HEAD_PREFIX_3_5 + 'corporate-raider.jpg'),
    CogActor('The Big Cheese', 'boss', 'a', 7.0 / A_SIZE, VBase4(0.75, 0.95, 0.75, 1.0), head_nodes='**/bigcheese'),
    SUPERVISORS[4]  # club president
]

ACTORS = {"supervisors": SUPERVISORS,
          "sellbots": SELLBOTS,
          "cashbots": CASHBOTS,
          "lawbots": LAWBOTS,
          "bossbots": BOSSBOTS
          }

COG_SET_NAMES = ["supervisors", "sellbots", "cashbots", "lawbots", "bossbots"]