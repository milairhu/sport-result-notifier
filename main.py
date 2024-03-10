from dotenv import load_dotenv
from src.notifier import SportResultNotifier
from src.sport import Sport



'''
Use for UFC results:
    API: api.sportradar.us
    Service for live results: /mma/trial/v2/en/schedules/live/summaries.json?api_key={your_api_key}
Use for Soccer results:
    API: api.sportradar.us
    Service for live results: /soccer/trial/v4/en/schedules/live/summaries.json?api_key={your_api_key}

TODO: complete with other sports and associated services
'''


if __name__ == "__main__":
    load_dotenv()
    notifier = SportResultNotifier(Sport.FOOTBALL, "FC Metz")
    notifier.monitor_event()