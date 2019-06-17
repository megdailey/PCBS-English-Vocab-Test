## PCBS English Vocab test

import random
import expyriment
import pandas as pd
import numpy as np

NTRIALS = 40
ITI = 2000
IAI = 1500


## Initialization
exp = expyriment.design.Experiment(name="English Vocabulary Test", background_colour=(255,255,255), foreground_colour=(255,255,255))
expyriment.control.initialize(exp)

## Loading stimuli and creating trials

instructions = expyriment.stimuli.TextLine("Welcome to today's experiment! In each trial, you will see four images and hear one word. Please click on the image that matches the word that you hear. When you are ready, click anywhere to begin.", text_colour=(0,0,0))
instructions.preload()

# Load visual stimuli
images = pd.read_csv('conditions.csv',)
images = images.applymap(str)

# for all image and audio stimuli, iterate through the file conditions.csv ..
block_two = expyriment.design.Block(name="Block 2")

for i in range(NTRIALS):
    test_trial = expyriment.design.Trial()
    photo1 = expyriment.stimuli.Picture(images.loc[i,'image'], position=(-350,250))
    photo1.preload()
    test_trial.add_stimulus(photo1)
    photo2 = expyriment.stimuli.Picture(images.loc[i,'image2'], position=(350,250))
    photo2.preload()
    test_trial.add_stimulus(photo2)
    photo3 = expyriment.stimuli.Picture(images.loc[i,'image3'], position=(-350,-250))
    photo3.preload()
    test_trial.add_stimulus(photo3)
    photo4 = expyriment.stimuli.Picture(images.loc[i,'image4'], position=(350,-250))
    photo4.preload()
    test_trial.add_stimulus(photo4)
    sound = expyriment.stimuli.Audio(images.loc[i,'audio'])
    sound.preload()
    test_trial.add_stimulus(sound)
    block_two.add_trial(test_trial, random_position=True)
exp.add_block(block_two)


kb = exp.keyboard
mouse = exp.mouse
exp.add_data_variable_names(['event_id','pos','rt'])

## Run experiment

expyriment.control.start()
mouse.show_cursor()

instructions.present()
mouse.wait_press()
expyriment.stimuli.BlankScreen().present()


mouse.show_cursor()

for t in block_two.trials:
    exp.clock.wait(ITI)
    expyriment.stimuli.BlankScreen().present()
    for s in t.stimuli[:4]:
        s.present(clear=False)
        s.present(clear=False)
    exp.clock.wait(IAI)
    t.stimuli[4].present()
    event_id, pos, rt = mouse.wait_press()
    exp.data.add([event_id, pos, rt])

expyriment.control.end()
