import numpy as np
import simpleaudio as sa
from math import pi

samplerate = 44100
lengh = 400
samples =  np.linspace(0, lengh, num =lengh* samplerate)
samples *= 1002432 * 2*pi
samples = np.sin(samples)
samples *= 2**15 -1
samples = samples.astype(np.int16)

sa.play_buffer(samples, 1, 2, samplerate).wait_done()