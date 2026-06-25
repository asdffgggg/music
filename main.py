import sounddevice as sd
import numpy as np
from enum import Enum
from math import pi, sqrt
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Static, Button, TextArea, Input
# from textual.reactive import reactive

class Sound(Enum):
    Sine = 0
    Piano = 1
letters = "CDEFGAB"
samplerate = 44100
class Instrument:
    def __init__(self, id) -> None:
        self.id = id
        self.name = "default"
        self.code = ""
        self.sound = Sound.Sine
class MusicApp(App):
    instruments = [Instrument("i0")]
    curr_instr = 0
    CSS_PATH = "style.tcss"
    tempo = 120
    samples = None
    played = False
    def on_mount(self):
        self.tick_time = self.set_interval(0.001, self.tick)
    def tick(self):
        try:
            if self.played and not sd.get_stream().active:
                self.query_one("#play", Button).label = "▶️"
        except:
            pass
    def compose(self) -> ComposeResult:
        with Horizontal(classes = "instruments"):
            yield Static("Instruments:")
            for i, insta in enumerate(self.instruments):
                yield Button(insta.name, id = insta.id)
            yield Button("+", id = "new_ins")
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
                yield Input(placeholder="TEMPO", type="integer", value=str(self.tempo) , id="tempo")
                yield Static("",id="error")
    def instr(self):
        return self.instruments[self.curr_instr]
    def on_button_pressed(self, event):
        if event.button.id[0] == 'i':
            try:
                self.tracking_you()
                self.curr_instr = int(event.button.id[1:])
                self.refresh(recompose=True)
                return
            except: 
             pass
        match event.button.id:
            case "play":
                try:
                    if event.button.label == "▶️":
                        self.played = True
                        samples = self.synthesis()
                        sd.play(samples, samplerate)
                        self.query_one("#play", Button).label = "⏹️"
                    elif not sd.get_stream().active:
                        self.query_one("#play", Button).label = "▶️"
                    else:
                        sd.stop()
                        self.query_one("#play", Button).label = "▶️"
                except Exception as e:
                    self.query_one("#error", Static).update(str(e))
            case "new_ins":
                self.instruments.append(Instrument(f"i{len(self.instruments)}"))
                self.reload()
    def tracking_you(self):
        self.instr().code = self.query_one("#urnotes", TextArea).text 
        tempo = int(self.query_one("#tempo", Input).value)
    def reload(self):
        self.tracking_you()
        self.refresh(recompose=True)
    def synthesis(self):
        self.tracking_you()
        all_samples = np.empty((0,),dtype=np.int16)
        for instr in self.instruments:
            octave = 4
            chord = []
            isamples = np.empty((0,),dtype=np.int16)
            dot = 1
            phase = 0 
            tempo = self.tempo

            for i in instr.code:
                try:
                    octave = int(i)
                except:
                    flat = i.islower()
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
                        case ".": 
                            dot = 1 + dot/2
                            continue
                        case _: continue
                    dur *= dot
                    dot = 1
                    seconds = dur*60/tempo
                    csamples =  np.zeros(round(seconds* samplerate))
                    volume = 0.4
                    if len(chord) > 0:
                        volume /= len(chord)
                    for f in chord:
                        samples =  np.linspace(0, seconds, num =round(seconds* samplerate))
                        samples *= f * 2*pi
                        match instr.sound:
                            case Sound.Sine:
                                samples = np.sin(samples + phase*2*pi)
                            case Sound.Piano:
                                a = -0.2 * np.cos(3*samples)
                                b = 0.25 * np.sin(samples)
                                c = sqrt(3)/2 *np.cos(samples)
                                over = a+b+c
                                samples = np.sin(over) * np.exp(-0.0004*samples)
                        csamples += volume* samples
                    csamples *= 2**15 -1
                    csamples = csamples.astype(np.int16)
                    isamples = np.append(isamples,csamples)
                    if len(chord) == 0:
                        phase = 0
                    else:    
                        phase += seconds * chord[0]
                    chord.clear()
            all_samples = pad(all_samples, len(isamples))
            isamples = pad(isamples, len(all_samples))
            all_samples += isamples
        return all_samples

def pad(arr, size):
    if len(arr) >= size:
        return arr
    return np.pad(arr, (0, size - len(arr)))

# C.q CE.q EGq 
# GB4Ei EBi EAi EGi Dgq Gigi
# Ei gi Ei Di D3BGEw h
# 5Eq 4Eq 2B3E.w

# 4b5dFah
# 4eGb5dh
# 4CeGbh
# 4FA5Ceh
                

if __name__ == "__main__":
    app = MusicApp()
    app.run()

# isamples = np.empty((),dtype=np.int16)
# samplerate = 44100
# lengh = 1
# csamples =  np.linspace(0, lengh, num =round(lengh* samplerate))
# csamples = csamples.astype(np.int16)
# for f in [220]:
#     samples =  np.linspace(0, lengh, num =round(lengh* samplerate))
#     samples *= f * 2*pi
#     samples = np.sin(samples)
#     samples *= 2**15 -1
#     samples = samples.astype(np.int16)
#     csamples += samples
# isamples = np.append(isamples,csamples)

# sa.play_buffer(isamples, 1, 2, samplerate).wait_done()