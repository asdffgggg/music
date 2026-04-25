import numpy as np
import simpleaudio as sa
from math import pi
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Static


class MusicApp(App):
    CSS_PATH = "style.tcss"
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static("instruments")
            with Horizontal():
                with Vertical(classes="column"):
                    yield Static("Palette")
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