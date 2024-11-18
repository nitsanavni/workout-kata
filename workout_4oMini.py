import time

class Metronome:
    def __init__(self):
        self.counter = 0
        self.timer_active = False
        self.start_time = None
        self.beat_times = []
        self.bpm = 0

    def update_counter(self, direction):
        if direction == "up":
            self.counter += 1
        elif direction == "down":
            self.counter -= 1

    def toggle_timer(self):
        self.timer_active = not self.timer_active
        if self.timer_active:
            self.start_time = time.time()

    def get_elapsed_time(self):
        if self.start_time and self.timer_active:
            return time.time() - self.start_time
        return 0

    def update_bpm(self, current_time):
        self.beat_times.append(current_time)
        if len(self.beat_times) > 4:
            self.beat_times.pop(0)

        if len(self.beat_times) > 1:
            intervals = [self.beat_times[i] - self.beat_times[i - 1] for i in range(1, len(self.beat_times))]
            avg_interval = sum(intervals) / len(intervals)
            self.bpm = 60 / avg_interval
        else:
            self.bpm = 0

    def format_elapsed_time(self):
        elapsed_time = self.get_elapsed_time()
        if elapsed_time < 1:
            return f"{int(elapsed_time // 60):02}:{int(elapsed_time % 60):02}:{int((elapsed_time * 100) % 100):02}"
        elif elapsed_time < 2:
            return f"{int(elapsed_time // 60):02}:{int(elapsed_time % 60):02}:{int((elapsed_time * 10) % 10)}"
        else:
            return f"{int(elapsed_time // 60):02}:{int(elapsed_time % 60):02}"

    def format_bpm(self):
        return f"{int(self.bpm):d}" if self.bpm > 0 else "--"
