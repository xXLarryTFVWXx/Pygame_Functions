import pygame.mixer

pygame.mixer.pre_init(44100, -16, 1, 512)
# hertz, bitdepth, channels, buffersize
def setup(hertz, bitdepth, channels, buffersize):
    pygame.mixer.pre_init(hertz, bitdepth, channels, buffersize)

def ON():
    pygame.mixer.init()