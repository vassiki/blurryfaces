import pandas as pd
import os
import time
from psychopy import visual, event, core, gui


win = visual.Window(size=(1280,800),screen=0,fullscr=True,colorSpace='rgb',color='black')
fixation = visual.TextStim(win, pos=(0,0), text="+", height=0.1, color='white')

CURDIR = os.path.abspath(os.path.dirname(__file__)) #current path of this file
CSVDIR = os.path.join(CURDIR,'csv') #going in csv folder
PRESENTSTIMDIR = os.path.join(CURDIR,'present_stimuli') #going in stimuli folder

FN = os.path.join(CSVDIR,"present_stim.csv")
trials = pd.read_csv(FN)
trials = trials.sample(frac=1).reset_index(drop=True)

present_stim = []
for i in range(trials.shape[0]):
    stim = os.path.join(PRESENTSTIMDIR,trials.loc[i,'Stimuli'])
    pre_stim = visual.ImageStim(win, pos=(0,0), image=stim, name='Stim_Image')
    present_stim.append(pre_stim)

instr_text = "Please familiarize yourself with the following faces. Press the space bar to continue." 
instructions = visual.TextStim(win, pos=(0,0), text=instr_text)

stim_dur = 2.5
fix_dur = 0.5

instrOn = 1
while instrOn:
    instructions.draw()
    win.flip()
    keys = event.getKeys()
    if 'space' in keys:
        instrOn = 0

for i in range(trials.shape[0]):
    fix_start = time.time()
    while time.time() - fix_start < fix_dur:
        fixation.draw()
        win.flip()
    
    stim_start = time.time()
    while time.time() - stim_start < stim_dur:
        present_stim[i].draw()
        win.flip()
    keys = event.getKeys()
    if 'q' in keys or 'escape' in keys:
        core.quit()

win.flip()
core.quit()