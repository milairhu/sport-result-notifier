from sport import Result, Sport
from sport_api import APIConnection
import json
from datetime import datetime
import time
import winsound

class SportResultNotifier:

    def __init__(self, sport: Sport, side: str) -> None:
        self.sport = sport.value.name
        self.api_url = sport.value.url
        self.service = sport.value.service
        self.side = side
        self.win_sound = "win.wav"
        self.loss_sound = "loss.wav"
        self.log_file = "log.txt"
        self.api = APIConnection(self.api_url, self.service)


    def get_fight_result(self) -> Result:
        #TODO: Call the API to get the result of the fight
        return Result.IN_PROGRESS
    
    def get_soccer_result(self) -> Result:
        response = self.api.connect()
        data = json.loads(response)

        for event in data['summaries']:
            if event['name'] == self.match_name:
                if event['status'] == 'closed':
                    if event['result']['winner'] == self.side:
                        return Result.WIN
                    else:
                        return Result.LOSS

        # If the match is not found or not closed, return None
        return None
    
    def log_result(self, result: Result) -> None:
        with open(self.log_file, 'a') as f:
            f.write(f'{datetime.now()}: {self.side} - {result.value}\n')

    def play_win_sound(self) -> None:
        # Launch win music
        winsound.PlaySound(self.win_sound, winsound.SND_FILENAME)

    def play_loss_sound(self) -> None:
        # Launch loss music
        winsound.PlaySound(self.loss_sound, winsound.SND_FILENAME)

    def play_draw_sound(self) -> None:
        # Launch draw music
        pass

    def monitor_fight(self) -> None:
        while True:
            result = None
            if self.sport == Sport.FOOTBALL.value.name:
                result = self.get_soccer_result()
            elif self.sport == Sport.MMA.value.name:
                result = self.get_fight_result()
            else:
                print("Sport " + self.sport+ " not supported")
                return
            if result ==  Result.WIN:
                self.play_win_sound()
                self.log_result(Result.WIN)
                break
            elif result == Result.LOSS:
                self.play_loss_sound()
                self.log_result(Result.LOSS)
                break
            elif result == Result.DRAW:
                self.play_draw_sound()
                self.log_result(Result.DRAW)
                break
            else:
                # Wait 5 minute before checking the result again
                time.sleep(60*5)
