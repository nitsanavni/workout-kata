import time
import curses

class TimerBPMTracker:
    def __init__(self):
        self.counter = 0
        self.timer_active = False
        self.start_time = None
        self.beat_times = []
        self.bpm = 0

    def increment_counter(self):
        self.counter += 1

    def decrement_counter(self):
        self.counter -= 1

    def toggle_timer(self):
        self.timer_active = not self.timer_active
        if self.timer_active:
            self.start_time = time.time()

    def get_elapsed_time(self):
        if self.start_time and self.timer_active:
            return time.time() - self.start_time
        return 0

    def record_beat(self):
        current_time = time.time()
        self.beat_times.append(current_time)
        if len(self.beat_times) > 4:
            self.beat_times.pop(0)

        # Calculate BPM based on intervals
        if len(self.beat_times) > 1:
            intervals = [
                self.beat_times[i] - self.beat_times[i - 1]
                for i in range(1, len(self.beat_times))
            ]
            avg_interval = sum(intervals) / len(intervals)
            self.bpm = 60 / avg_interval if avg_interval > 0 else 0
        else:
            self.bpm = 0

    def get_bpm(self):
        return int(self.bpm) if self.bpm > 0 else None

    def get_counter(self):
        return self.counter

    def format_elapsed_time(self):
        elapsed_time = self.get_elapsed_time()
        if elapsed_time < 1:
            return f"{int(elapsed_time // 60):02}:{int(elapsed_time % 60):02}:{int((elapsed_time * 100) % 100):02}"
        elif elapsed_time < 2:
            return f"{int(elapsed_time // 60):02}:{int(elapsed_time % 60):02}:{int((elapsed_time * 10) % 10)}"
        else:
            return f"{int(elapsed_time // 60):02}:{int(elapsed_time % 60):02}"


def main(stdscr):
    # Initialize curses and hide cursor
    curses.curs_set(0)
    stdscr.nodelay(True)

    tracker = TimerBPMTracker()

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Counter (controlled by UP/DOWN arrows)
        key = stdscr.getch()
        if key == curses.KEY_UP:
            tracker.increment_counter()
        elif key == curses.KEY_DOWN:
            tracker.decrement_counter()
        stdscr.addstr(1, width // 2 - 5, f"{tracker.get_counter()}")

        # Timer (controlled by SPACE)
        if key == ord(" "):  # Toggle timer with SPACE
            tracker.toggle_timer()

        stdscr.addstr(2, width // 2 - 5, tracker.format_elapsed_time())

        # BPM (Shift key to record beat)
        if key == ord(
            "\t"
        ):  # Shift not detected directly in curses, using TAB as proxy
            tracker.record_beat()

        bpm_str = f"{tracker.get_bpm()}" if tracker.get_bpm() is not None else "--"
        stdscr.addstr(3, width // 2 - 5, bpm_str)

        # Refresh display
        stdscr.refresh()
        time.sleep(0.05)


# Run the curses application
curses.wrapper(main)
