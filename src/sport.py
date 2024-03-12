from enum import Enum
import os
from src.sport_api import SportAPI
from datetime import datetime

class Result(Enum):
    WIN = "win"
    LOSS = "loss"
    DRAW = "draw"
    IN_PROGRESS = "in_progress"
    TEAM_GOAL = "team_goal"
    OPPONENT_GOAL = "opponent_goal"
    HALF_TIME = "half_time"
    OPPONENT_GOAL_CANCELED = "opponent_goal_canceled"
    TEAM_GOAL_CANCELED = "team_goal_canceled"

class Sport(Enum):
    MMA = SportAPI("MMA", "api.sportradar.us", f"/mma/trial/v2/en/schedules/live/summaries.json?api_key={os.getenv('MMA_API_KEY')}") #TODO : update with right service
    FOOTBALL = SportAPI("Football", "api.sportradar.us", f"/soccer/trial/v4/en/schedules/live/summaries.json?api_key={os.getenv('FOOTBALL_API_KEY')}")

