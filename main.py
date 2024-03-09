import time
import winsound

class SportResultNotifier:
    def __init__(self):
        self.result = None

    def get_fight_result(self):
        # TODO : Call an API to get the result of the fight
        self.result = "win"

    def play_win_sound(self):
        # Launch win music
        winsound.PlaySound('win.wav', winsound.SND_FILENAME)

    def play_loss_sound(self):
        # Launch loss music
        winsound.PlaySound('loss.wav', winsound.SND_FILENAME)

    def monitor_fight(self):
        while True:
            self.get_fight_result()
            if self.result == "win":
                self.play_win_sound()
                break
            elif self.result == "loss":
                self.play_loss_sound()
                break
            else:
                # Wait 1 minute before checking the result again
                time.sleep(60)

if __name__ == "__main__":
    notifier = SportResultNotifier()
    notifier.monitor_fight()