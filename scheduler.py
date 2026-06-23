from datetime import datetime, timedelta
import time

class Scheduler:
    def __init__(self, callback):
        self.callback = callback
        self.running = False

    def start_hourly(self):
        self.running = True

        while self.running:
            now = datetime.now()
            next_hour = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
            sleep_time = (next_hour - now).total_seconds()

            time.sleep(min(sleep_time, 60))

            if self.running:
                self.callback()

    def stop(self):
        self.running = False