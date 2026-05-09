import numpy as np
import simpleaudio as sa
from enum import Enum
from math import pi
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Static, Button, TextArea


class Sound(Enum):
    Sine = 0
letters = "CDEFGAB"
samplerate = 44100
class Instrument:
    def __init__(self) -> None:
        self.name = "default"
        self.code = ""
        self.sound = Sound.Sine
class MusicApp(App):
    instruments = [Instrument()]
    curr_instr = 0
    CSS_PATH = "style.tcss"
    tempo = 120
    samples = None
    def compose(self) -> ComposeResult:
        with Horizontal(classes = "instruments"):
            yield Static("Instruments:")
            for i, insta in enumerate(self.instruments):
                yield Button(insta.name, id = insta.name)
        with Horizontal():
            with Vertical(classes="column"):
                yield Static("Palette")
                for c in letters:
                    yield Button(c, id = c)

            with Vertical(classes="notes"):
                yield Static("Notes")
                yield TextArea.code_editor(self.instr().code, id = "urnotes")
            with Vertical(classes="column"):
                yield Static("Control")
                yield Button("▶️", id = "play")
                yield Static("",id="error")
    def instr(self):
        return self.instruments[self.curr_instr]
    def on_button_pressed(self, event):
        # if event.button.id in letters:
        #     self.instr().code += event.button.id
        if event.button.id == "play":
            try:
                self.samples = self.synthesis()
            except Exception as e:
                self.query_one("#error", Static).update(str(e))
        pass
    def synthesis(self):
        code = self.query_one("#urnotes", TextArea).text
        octave = 4
        chord = []
        isamples = np.empty((),dtype=np.int16)

        for i in code:
            try:
                octave = int(i)
            except:
                flat = i.islower()
                i = i.capitalize()
                if i.lower() in letters.lower():
                    i = letters.index(i.capitalize())
                    pitch = [0, 2, 4, 5, 7, 9, 11][i] + octave*12
                    if flat:
                        pitch -=1
                    f = 16.35*(2**(pitch/12))
                    chord.append(f)
                    continue
                dur = 1
                match i:
                    case "w": dur = 4
                    case "h": dur = 2
                    case "q": dur = 1
                    case "i": dur= 0.5
                    case "s": dur = 0.25
                    case _: continue
                lengh = dur/self.tempo
                csamples =  np.linspace(0, lengh, num =round(lengh* samplerate))
                for f in chord:
                    samples =  np.linspace(0, lengh, num =round(lengh* samplerate))
                    samples *= f * 2*pi
                    samples = np.sin(samples)
                    csamples += samples
                csamples *= 2**15 -1
                csamples = csamples.astype(np.int16)
                isamples = np.append(isamples,csamples)
        return isamples
                

                

if __name__ == "__main__":
    app = MusicApp()
    app.run()
    if app.samples:
        sa.play_buffer(app.samples, 1, 2, samplerate).wait_done()

# isamples = np.empty((),dtype=np.int16)
# samplerate = 44100
# lengh = 1
# csamples =  np.linspace(0, lengh, num =round(lengh* samplerate))
# csamples = csamples.astype(np.int16)
# for f in [220, 440]:
#     samples =  np.linspace(0, lengh, num =round(lengh* samplerate))
#     samples *= f * 2*pi
#     samples = np.sin(samples)
#     samples *= 2**15 -1
#     samples = samples.astype(np.int16)
#     csamples += samples
# isamples = np.append(isamples,csamples)

# sa.play_buffer(isamples, 1, 2, samplerate).wait_done()