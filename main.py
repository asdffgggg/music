import numpy as np
import simpleaudio as sa
from enum import Enum
from math import pi
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Static, Button



class Note:
    def __init__(self, pitches, dur) -> None:
        self.pitches = pitches
        self.dur = dur
class Sound(Enum):
    Sine = 0

class Instrument:
    def __init__(self) -> None:
        self.name = "default"
        self.code = ""
        self.sound = Sound.Sine
class MusicApp(App):
    instruments = [Instrument()]
    curr_instr = 0
    CSS_PATH = "style.tcss"
    def compose(self) -> ComposeResult:
        with Horizontal(classes = "row"):
            with Vertical(classes="column"):
                yield Static("Instruments:")
            for i, insta in enumerate(self.instruments):
                with Vertical(classes="column"):
                    yield Button(insta.name, id = insta.name)
        with Horizontal():
            with Vertical(classes="column"):
                yield Static("Palette")
                for c in "CDEFGAB":
                    yield Button(c)

            with Vertical(classes="column"):
                yield Static("Notes")
            with Vertical(classes="column"):
                yield Static("Control")

if __name__ == "__main__":
    app = MusicApp()
    app.run()

# samplerate = 44100
# lengh = 400
# samples =  np.linspace(0, lengh, num =lengh* samplerate)
# samples *= 110 * 2*pi
# samples = np.sin(samples)
# samples *= 2**15 -1
# samples = samples.astype(np.int16)

# sa.play_buffer(samples, 1, 2, samplerate).wait_done()