from src.actors.cog_actor import CogActor
from src.globals import RESOURCES_DIR

ACTORS = [
    CogActor("Factory Foreman (Neutral)", "sell", "b", 1.148, (0.886, 0.737, 0.784, 1.0),
             RESOURCES_DIR + "/phase_4/models/char/ttr_m_ene_sellbotForeman.bam", is_supervisor=True),
    CogActor("Factory Foreman (Angry)", "sell", "b", 1.148, (0.886, 0.737, 0.784, 1.0),
             RESOURCES_DIR + "/phase_4/models/char/ttr_m_ene_sellbotForemanAngry.bam", is_supervisor=True),
    CogActor("Mint Auditor", "cash", "c", 1.378, (0.686, 0.882, 0.831, 1.0),
             RESOURCES_DIR + "/phase_4/models/char/ttr_m_ene_cashbotAuditor.bam", is_supervisor=True),
    CogActor("Office Clerk", "law", "b", 1.323, (0.722, 0.769, 0.816, 1.0),
             RESOURCES_DIR + "/phase_4/models/char/ttr_m_ene_lawbotClerk.bam", is_supervisor=True),
    CogActor("Club President", "boss", "a", 0.706, (0.950, 0.750, 0.750, 1.0),
             RESOURCES_DIR + "/phase_4/models/char/ttr_m_ene_bossbotClubPresident.bam", is_supervisor=True)
]