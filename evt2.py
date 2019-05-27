## PCBS English Vocab test

import random
import expyriment
import pandas as pd
import numpy as np

NTRIALS = 40
ITI = 2000
IAI = 1000

#expyriment.control.set_develop_mode(on=True)

## Initialization
exp = expyriment.design.Experiment(name="English Vocabulary Test", background_colour=(255,255,255), foreground_colour=(255,255,255))
expyriment.control.initialize(exp)

## Loading stimuli and creating trials

# Load instructions as block
block_one = expyriment.design.Block(name="Block 1")
trial_one = expyriment.design.Trial()
instructions = expyriment.stimuli.TextLine("Welcome to today's experiment! In each trial, you will see four images and hear one word. Please click on the image that matches the word that you hear. When you are ready, click anywhere (with the mouse) to begin.", text_colour=(0,0,0))
instructions.preload()
trial_one.add_stimulus(instructions)
block_one.add_trial(trial_one)
exp.add_block(block_one)

# Load visual stimuli
images = pd.read_csv('conditions.csv',)
images = images.applymap(str)

# for all image and audio stimuli, iterate through the file conditions.csv ..
block_two = expyriment.design.Block(name="Block 2")

for i in range(NTRIALS):
    test_trial = expyriment.design.Trial()
    photo1 = expyriment.stimuli.Picture(images.loc[i,'image'], position=(-300,250))
    photo1.preload()
    test_trial.add_stimulus(photo1)
    photo2 = expyriment.stimuli.Picture(images.loc[i,'image2'], position=(300,250))
    photo2.preload()
    test_trial.add_stimulus(photo2)
    photo3 = expyriment.stimuli.Picture(images.loc[i,'image3'], position=(-300,-250))
    photo3.preload()
    test_trial.add_stimulus(photo3)
    photo4 = expyriment.stimuli.Picture(images.loc[i,'image4'], position=(300,-250))
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
#key, rt = kb.wait([expyriment.misc.constants.K_LEFT, expyriment.misc.constants.K_RIGHT])
mouse.show_cursor()

instructions.present()
mouse.wait_press()
#kb.wait([expyriment.misc.constants.K_LEFT, expyriment.misc.constants.K_RIGHT])
expyriment.stimuli.BlankScreen().present()

# for t in block_one.trials:
#     for s in t.stimuli:
#         s.present()
#         #event_id, pos, rt = mouse.wait_press()
#         kb.wait([expyriment.misc.constants.K_LEFT, expyriment.misc.constants.K_RIGHT])

#maybe here present first block, then iterate through trials of second block
#for b in exp.blocks:


mouse.show_cursor()



for t in block_two.trials:
    exp.clock.wait(ITI)
    expyriment.stimuli.BlankScreen().present()
    for s in t.stimuli[:4]:
        s.present(clear=False)
        s.present(clear=False)
    #t.stimuli[2].present()
    #t.stimuli[3].present()
    exp.clock.wait(IAI)
    t.stimuli[4].present()
    event_id, pos, rt = mouse.wait_press()
    exp.data.add([event_id, pos, rt])

# experimenting .. how to present stimuli at the same time??
#for t in block_two.trials:
#    exp.clock.wait(ITI)
#    event_id, pos, rt = mouse.wait_press()
##        for s in t.stimuli:
#            s.present()
#    exp.data.add([event_id, pos, rt])


expyriment.control.end()
