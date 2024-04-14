from src.sport import Result, Sport
from src.sport_api import APIConnection
import json
from datetime import datetime
import time
import winsound

from src.utils import speak_text

class SportResultNotifier:

    def __init__(self, sport: Sport, side: str) -> None:
        self.sport = sport.value.name
        self.api_url = sport.value.url
        self.service = sport.value.service
        self.side = side
        self.win_sound = "sound/win.wav"
        self.loss_sound = "sound/loss.wav"
        self.draw_sound = "sound/draw.wav"
        self.log_file = "log.txt"
        self.api = APIConnection(self.api_url, self.service)
        self.side_score = -1
        self.opponent_score = -1
        self.side_is_home = False


    def get_fight_result(self) -> Result:
        #TODO: Call the API to get the result of the fight
        return Result.IN_PROGRESS
    
    def get_soccer_result(self) -> Result:
        response = self.api.connect() # Call the API to get the result of soccer games
        data = json.loads(response) # Convert the response to a json object
        for event in data['summaries']:
            for competitor in event['sport_event']['competitors']:
                if competitor['name'] == self.side :
                    # If there is data about the game 
                    if  self.side_score == -1 and self.opponent_score == -1:
                        # If this is the first time we are checking the game
                        if competitor['qualifier'] == 'home':
                            # If The team is playing at home
                            self.side_is_home = True
                            self.side_score = event['sport_event_status']['home_score']
                            self.opponent_score = event['sport_event_status']['away_score']
                        else:
                            # If The team is playing away
                            self.side_is_home = False
                            self.side_score = event['sport_event_status']['away_score']
                            self.opponent_score = event['sport_event_status']['home_score']
                    if event['sport_event_status']['match_status'] == 'ended':
                        # If Game is over
                        try:
                            if event['sport_event_status']['match_tie'] == True:
                                # If Game is a draw
                                return Result.DRAW
                        except KeyError:
                            pass
                        #If not a draw, check if the team won or lost
                        winnerid = event['sport_event_status']['winner_id']
                        for competitor in event['sport_event']['competitors']:
                            if competitor['name'] == self.side:
                                # If the team is found
                                if competitor['id'] == winnerid:
                                    # if the team is the winner
                                    return Result.WIN
                                else:
                                    return Result.LOSS
                    elif event['sport_event_status']['match_status'] == 'halftime':
                        # Game is at half time
                        print("Game is at half time")
                        return Result.HALF_TIME
                    else:
                        # Game is still in progress
                        print("Game is still in progress")
                        print(f"Score: Self {self.side_score} - Opponent:  {self.opponent_score}")
                        # Look for score changes
                        if self.side_is_home:
                            if self.side_score < event['sport_event_status']['home_score']:
                                self.side_score = event['sport_event_status']['home_score']
                                return Result.TEAM_GOAL
                            elif self.opponent_score < event['sport_event_status']['away_score']:
                                self.opponent_score = event['sport_event_status']['away_score']
                                return Result.OPPONENT_GOAL
                            elif self.opponent_score > event['sport_event_status']['away_score']:
                                self.opponent_score = event['sport_event_status']['away_score']
                                return Result.OPPONENT_GOAL_CANCELED
                            elif self.side_score > event['sport_event_status']['home_score']:
                                self.side_score = event['sport_event_status']['home_score']
                                return Result.TEAM_GOAL_CANCELED
                        else:
                            if self.side_score < event['sport_event_status']['away_score']:
                                self.side_score = event['sport_event_status']['away_score']
                                return Result.TEAM_GOAL
                            elif self.opponent_score < event['sport_event_status']['home_score']:
                                self.opponent_score = event['sport_event_status']['home_score']
                                return Result.OPPONENT_GOAL
                            elif self.opponent_score > event['sport_event_status']['home_score']:
                                self.opponent_score = event['sport_event_status']['home_score']
                                return Result.OPPONENT_GOAL_CANCELED
                            elif self.side_score > event['sport_event_status']['away_score']:
                                self.side_score = event['sport_event_status']['away_score']
                                return Result.TEAM_GOAL_CANCELED
                        return Result.IN_PROGRESS
        # Team not found
        return None
    
    def log_result(self, result: Result) -> None:
        with open(self.log_file, 'a') as f:
            f.write(f'{self.sport},  {datetime.now()}: {self.side} - {result.value}\n')

    def play_win_sound(self) -> None:
        # Launch win music
        winsound.PlaySound(self.win_sound, winsound.SND_FILENAME)
        speak_text(f"Game is over. Congratulations! {self.side} won the game!")

    def play_loss_sound(self) -> None:
        # Launch loss music
        winsound.PlaySound(self.loss_sound, winsound.SND_FILENAME)
        speak_text(f"Game is over. Too bad... {self.side} lost the game...")

    def play_draw_sound(self) -> None:
        # Launch draw music
        winsound.PlaySound(self.draw_sound, winsound.SND_FILENAME)
        speak_text("Game is over. The game is a draw...")

    def play_half_time_sound(self) -> None:
        # Launch half time music
        speak_text("Game is at half time. See you in a few minutes!")

    def monitor_event(self) -> None:
        while True:
            result = None
            if self.sport == Sport.FOOTBALL.value.name:
                result = self.get_soccer_result()
            elif self.sport == Sport.MMA.value.name:
                result = self.get_fight_result()
            else:
                print("ERROR: Sport " + self.sport+ " not supported")
                return
            if result ==  Result.WIN:
                self.play_win_sound()
                self.log_result(Result.WIN)
                print("Team won! Exiting...")
                return
            elif result == Result.LOSS:
                self.play_loss_sound()
                self.log_result(Result.LOSS)
                print("Team lost. Exiting...")
                return
            elif result == Result.DRAW:
                self.play_draw_sound()
                self.log_result(Result.DRAW)
                print("Game is a draw. Exiting...")
                return
            elif result == Result.TEAM_GOAL:
                speak_text(f"Goal for {self.side}!")
                self.log_result(Result.TEAM_GOAL)
            elif result == Result.OPPONENT_GOAL:
                speak_text(f"Goal for opponent...")
                self.log_result(Result.OPPONENT_GOAL)
            elif result == Result.OPPONENT_GOAL_CANCELED:
                speak_text(f"Goal for opponent canceled!")
                self.log_result(Result.OPPONENT_GOAL_CANCELED)
            elif result == Result.TEAM_GOAL_CANCELED:
                speak_text(f"Goal for {self.side} canceled...")
                self.log_result(Result.TEAM_GOAL_CANCELED)
            elif result == Result.HALF_TIME:
                # Halftime: Wait 5 minutes before checking the result again
                self.log_result(Result.HALF_TIME)
                self.play_half_time_sound()
                time.sleep(60*5)
            elif result == Result.IN_PROGRESS:
                # Wait 1 minute before checking the result again
                time.sleep(60)
            else: 
                print("ERROR: Result for the request is not supported")
                return
