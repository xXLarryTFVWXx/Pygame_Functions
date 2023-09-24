import pygame.mixer

available_channels = []

channels = {
    "sound": [None for channel in range(pygame.mixer.get_num_channels())],
    "Music": None
}

def setup(hertz=44001, bitdepth=-16, buffersize=512, use_mono=0):
    if not isinstance(use_mono, (bool, int)):
        raise TypeError(f"use_mono must be of either type bool or type int, not{type(use_mono)}")
    pygame.mixer.pre_init(hertz, bitdepth, 2-use_mono, buffersize)

def ON():
    pygame.mixer.init()
    c = None
    for channel in range(pygame.mixer.get_num_channels()):
        if not c is None:
            old_channel = c
        c = pygame.mixer.find_channel()
        if c is None:
            raise Exception("No channels available")
        if c is old_channel:
            break
        c.load("test.wav")
        c.set_volume(0)
        c.play()
        available_channels.append(c)

def config_channels(location, *channel_objects):
    if not isinstance(location, str):
        raise TypeError(f"location must be of type str, not {type(location)}")
    if location == "sound":
        if len(*channel_objects) == 0:
            return channels[location]

def OFF():
    pygame.mixer.quit()

if __name__ == "__main__":
    setup()
    ON()
    print(pygame.mixer.get_num_channels())
    OFF()