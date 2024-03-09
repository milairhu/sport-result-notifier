from enum import Enum
import winsound
import time
from typing import Optional
from datetime import datetime

class Result(Enum):
    WIN = "win"
    LOSS = "loss"
    IN_PROGRESS = "in_progress"

class SportResultNotifier:

    def __init__(self) -> None:
        self.url = "https://api.sport.com/fight/1"
        self.side = "red"
        self.win_sound = "win.wav"
        self.loss_sound = "loss.wav"
        self.log_file = "log.txt"


    def get_fight_result(self) -> Result:
        # TODO : Call an API to get the result of the fight
        return Result.WIN
    
    def log_result(self, result: Result) -> None:
        with open(self.log_file, 'a') as f:
            f.write(f'{datetime.now()}: {result.value}\n')

    def play_win_sound(self) -> None:
        # Launch win music
        winsound.PlaySound(self.win_sound, winsound.SND_FILENAME)

    def play_loss_sound(self) -> None:
        # Launch loss music
        winsound.PlaySound(self.loss_sound, winsound.SND_FILENAME)

    def monitor_fight(self) -> None:
        while True:
            result = self.get_fight_result()
            if result ==  Result.WIN:
                self.play_win_sound()
                self.log_result(Result.WIN)
                break
            elif result == Result.LOSS:
                self.play_loss_sound()
                self.log_result(Result.LOSS)
                break
            else:
                # Wait 1 minute before checking the result again
                time.sleep(60)

if __name__ == "__main__":
    notifier = SportResultNotifier()
    notifier.monitor_fight()