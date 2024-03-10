from enum import Enum
import os
from sport_api import SportAPI


class Result(Enum):
    WIN = "win"
    LOSS = "loss"
    DRAW = "draw"
    IN_PROGRESS = "in_progress"

class Sport(Enum):
    MMA = SportAPI("MMA", "api.sportradar.us", "/mma/trial/v2/en/schedules/live/summaries.json?api_key={}".format(os.getenv('MMA_API_KEY')))
    FOOTBALL = SportAPI("Football", "api.sportradar.us", "/soccer/trial/v4/en/schedules/live/summaries.json?api_key={}".format(os.getenv('FOOTBALL_API_KEY')))

