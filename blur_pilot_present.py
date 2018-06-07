import pandas as pd
import os
import time
import re
#from collections import OrderedDict
from psychopy import visual, event, core, gui

# ToDo:

# 1. (complete) Figure out better size for response images.
#    Preferably save probe and response images in separate directories,
#    with different original sizes. Simply call them from the right location.
# 2. (complete) Create correct conditions file.
# 3. (complete - not implemented) Draw response box around selection.
# 4. (TO BE COMPLETED) Record all positions of images to output file.
#    Especially the distance of correct image from the center.
# 5. (complete) Counterbalance hemifield specific occurence of correct image.
# 6. (will be done post-hoc) Record which face was selected, not just the mouse positions.
# 7. (???) Give participants accuracy feedback at every break.
# 8. (complete) Add breaks.

# 9. Change in image reading logic:
#       Read all the unique images and save them with the same name as row entries
#       Dictionary containing 10 test image visual stims, with key names from row names
#       Dictionary containing 10 names of images per trial, 550*10 as key, with value as position
#       Loop through image stim dict and assign correct positions to each one in presentation loop

participant = '00'

run_configuration = gui.Dlg(title='Participant Information')
run_configuration.addField("Participant:", participant)
run_configuration.show()

if run_configuration.OK:
    participant = str(run_configuration.data[0])
elif not run_configuration.OK:
    core.quit()

win = visual.Window(size=(1280,800),screen=0,fullscr=True,colorSpace='rgb',color='black')
fixation = visual.TextStim(win, pos=(0,0), text="+", height=0.1, color='white')

CURDIR = os.path.abspath(os.path.dirname(__file__)) #current path of this file
CSVDIR = os.path.join(CURDIR,'csv') #going in csv folder
PROBESTIMDIR = os.path.join(CURDIR,'probe_stimuli') #going in stimuli folder
TESTSTIMDIR = os.path.join(CURDIR,'test_stimuli')
RESDIR = os.path.join(CURDIR,'results') #going in results folder

#directing to conditions folder, reading it in with pandas, shuffling the conditions (because blur levels listed in order)
FN = os.path.join(CSVDIR,"conditions.csv")
#FN = os.path.join(CSVDIR,"conditions_try.csv")
trials = pd.read_csv(FN)
trials = trials.sample(frac=1).reset_index(drop=True)

#getting the now-shuffled stimuli for the experiment

#stim_size_resp = (0.5, 1)

stimuli_probe = {}
stimuli_resp = {}

resp_positions = [(-0.8,0.5),(-0.4,0.5),(0,0.5),(0.4,0.5),(0.8,0.5),(-0.8,-0.5),(-0.4,-0.5),(0,-0.5),(0.4,-0.5),(0.8,-0.5)]

#test_images = []

loading_text = "Please wait while the images are loading..."
loading = visual.TextStim(win, pos=(0,0), text=loading_text)
for i in range(trials.shape[0]):
    loading.draw()
    win.flip()
    #probe = os.path.join(PROBESTIMDIR,trials.loc[i,'Probe_Img'])
    probe = os.path.join(PROBESTIMDIR,trials.loc[i,'ImageProbe'])
    trial_probe = visual.ImageStim(win, pos=(0,0), image=probe, name='Probe_Img')
    stimuli_probe[i] = trial_probe
    #print "TRIAL NUMBER {0}".format(i)
#    test_images = []
#    for j in range(10): # for 10 positions
#        image_col = 'Image{0}'.format(j)
#        #print image_col
#        image_name = os.path.join(TESTSTIMDIR,trials.loc[i,image_col])
#        image = visual.ImageStim(win, pos=resp_positions[j],image=image_name, name='Resp_Img')
#        test_images.append(image)
    pos_list = {}
    for j in range(10):
        image_col = 'Image{0}'.format(j)
        image_n = trials.loc[i,image_col]
       # print image_col,image_n
        pos_list[image_n] = resp_positions[j]
    stimuli_resp[i] = pos_list
    keys = event.getKeys()
    if 'q' in keys or 'escape' in keys:
        core.quit()
    
test_images = {}
for i,image_n in enumerate(os.listdir(TESTSTIMDIR)):
    if '.jpg' in image_n:
        image_path = os.path.join(TESTSTIMDIR,image_n)
        test_images[image_n] = visual.ImageStim(win,image=image_path, name='Resp_Img_{0}'.format(i))

#establishing the instruction and thanks text    
instr_text = ("For each trial, you will see a target face at varying degrees of blurriness. " 
             "After the target is presented, you will see 10 response faces. "
             "Click on the response face that matches the target face you previously saw. "
             "Make sure to click the center (i.e. nose) of the response face you choose. "
             "Press the space bar to continue on to the experiment.")
instructions = visual.TextStim(win, pos=(0,0), text=instr_text)

thanks_text = "You have now reached the end of the experiment. Thanks for your participation!"
thanks = visual.TextStim(win, pos=(0,0), text=thanks_text)

#establish durations of fixation cross, stimuli, and response
fix_dur = 0.5
stim_dur = 1
resp_dur = 5  

#show instructions screen
instrOn = 1
while instrOn:
    instructions.draw()
    win.flip()
    keys = event.getKeys()
    if 'space' in keys:
        instrOn = 0

reaction_times = []
mouse_start = []
mouse_click = []

#boxVert = [[(-.5,-.5),(-.5,.5),(.5,.5),(.5,-.5)],[(-.48,-.48),(-.48,.48),(.48,.48),(.48,-.48)]]
#box = visual.ShapeStim(win, vertices=boxVert, fillColor='red', lineWidth=0, pos=(0,0))

break_text = 'You can take a short break now. Press space to continue.'
breaks = visual.TextStim(win, pos=(0,0), text=break_text)
break_trials = range(55,500,55)

mouse = event.Mouse()

#experiment loop
for i in range(len(stimuli_probe)):
    if i in break_trials:
        breakOn = 1
        while breakOn:
            breaks.draw()
            win.flip()
            keys = event.getKeys()
            if 'space' in keys:
                breakOn = 0            
    
    event.clearEvents() #clears button presses from previous trials
    mouse.setVisible(0)
    
    #showing fixation cross
    fix_start = time.time()
    while time.time() - fix_start < fix_dur:
        fixation.draw()
        win.flip()
    
    #showing stimuli    
    stim_start = time.time()
    while time.time() - stim_start < stim_dur:
        stimuli_probe[i].draw()
        win.flip()
    
    #showing response options and giving them time to respond    
    resp_start = time.time()
    respMade = 0 
    #start_mouse_pos = re.findall("\d+\.\d+",trials.loc[i,'Mouse'])
    start_mouse_pos = [round(trials.loc[i,'MouseX'],1),round(trials.loc[i,'MouseY'],1)]
    #mouse = event.Mouse(newPos=start_mouse_pos)
    #mouse.setPos(newPos=(float(start_mouse_pos[0]),float(start_mouse_pos[1]))) #not reading the negatives in the input file?
    mouse.setPos(newPos=(start_mouse_pos[0],start_mouse_pos[1])) 
    
    for trial_images in stimuli_resp[i].keys():
        #print i, stimuli_resp[i]
        test_images[trial_images].pos = stimuli_resp[i][trial_images]
        
    while not respMade and time.time() - resp_start < resp_dur:
        mouse.setVisible(1)
#        for j in range(10):
        for j in test_images.keys():
            test_images[j].draw()
#            stimuli_resp[i][j].draw()

        win.flip()
        mouse_resp_0, mouse_resp_1, mouse_resp_2 = mouse.getPressed()
        
        keys = event.getKeys()
        if mouse_resp_0:
            resp = mouse.getPos() 
            rt = time.time() - resp_start
            for im in test_images:
                if mouse.isPressedIn(test_images[im],buttons=[0]):
                    resp = im
            respMade = 1
            #box.pos = resp #box only stays for a flip, no point in drawing
            #box.draw()
            #win.flip()
        elif 'q' in keys or 'escape' in keys:
            resp_made = 1
            core.quit()
        #elif mouse_resp_1:
        #    resp = mouse.getPos()
        #    rt = time.time() - resp_start
        #    respMade = 1
        #elif mouse_resp_2:
        #    resp = mouse.getPos()
        #    rt = time.time() - resp_start
        #    respMade = 1
        else:
           resp = 'other'
           rt = 0
           if time.time() - resp_start == resp_dur:
              respMade = 1
    
    #appending all rts and mcs in the experiment into lists (see above)         
    reaction_times.append(rt)
    mouse_start.append(start_mouse_pos)
    mouse_click.append(resp)

#getting the probe images and response images  used in the experiment in the order they were shown            
probe_images = []
for h in range(trials.shape[0]):
    probe_images.append(trials.loc[h,'ImageProbe'])

corr_images = []
for i in range(trials.shape[0]):
    corr_images.append(trials.loc[i, 'Correct'])

loc_images = []  #Appending the same values to each row and not even 1-10 (some numbers are repeated and others are excluded -- this fixed with writing out each image)
for j in range(trials.shape[0]):
    resp_images = []
    #for k in range(10):
    resp_images.append(trials.loc[j, 'Image0'])
    resp_images.append(trials.loc[j, 'Image1'])
    resp_images.append(trials.loc[j, 'Image2'])
    resp_images.append(trials.loc[j, 'Image3'])
    resp_images.append(trials.loc[j, 'Image4'])
    resp_images.append(trials.loc[j, 'Image5'])
    resp_images.append(trials.loc[j, 'Image6'])
    resp_images.append(trials.loc[j, 'Image7'])
    resp_images.append(trials.loc[j, 'Image8'])
    resp_images.append(trials.loc[j, 'Image9'])
    loc_images.append(resp_images)

correct = []
for idx in range(trials.shape[0]):
    realim = probe_images[idx].split('_')[0]
    if isinstance(mouse_click[idx],str):
        respim = mouse_click[idx].split('_')[0]
        if respim == realim:
            correct.append(1)
        else:
            correct.append(0)
    else:
        correct.append(0)

#for k in range(10):
    #image_num = 'Image{0}'.format(k)
    #resp_images.append(trials.loc[k, image_num])

#resp_images = [] 
#for j in range(trials.shape[0]):
    #resp_images.append(trials.loc[j, 'Image0'])
    #resp_images.append(trials.loc[j, 'Image1'])
    #resp_images.append(trials.loc[j, 'Image2'])
    #resp_images.append(trials.loc[j, 'Image3'])
    #resp_images.append(trials.loc[j, 'Image4'])
    #resp_images.append(trials.loc[j, 'Image5'])
    #resp_images.append(trials.loc[j, 'Image6'])
    #resp_images.append(trials.loc[j, 'Image7'])
    #resp_images.append(trials.loc[j, 'Image8'])   
    #resp_images.append(trials.loc[j, 'Image9'])


#saving the files in participant folders
#out_dict = {'Probe_Img': probe_images,'start_mouse_pos': mouse_start, 'Response': mouse_click, 'RT': reaction_times, 'Correct_Img': corr_images,'RL': loc_images}
out_dict = {'Probe_Img': probe_images,'start_mouse_pos': mouse_start, 'Response': mouse_click, 'RT': reaction_times, 'RL': loc_images, 'Correct':correct}
df_to_save = pd.DataFrame(out_dict)
FN_TO_SAVE = os.path.join(RESDIR,"blur_pilot_sub{0}.csv".format(participant))
df_to_save.to_csv(FN_TO_SAVE, sep=",",index=False)

#showing thanks screen and exit
thanks.draw()
win.flip()
core.wait(2)

core.quit()
