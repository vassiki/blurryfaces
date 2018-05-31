#!/usr/bin/env/ python

import pandas as pd
import numpy as np
import random

def cond_df():
    # go through all identities and all morphs
    ids = ["uf{0}_{1}.jpg".format(x,y) for x in range(1,11,1) for y in range(0,51,5)]

    # generate stimnames 
    all_stim = {}
    for i in ids:
        all_stim[i] = ["uf{0}_0.jpg".format(x) for x in range(1,11,1)]
        # shuffle first 10 columns
        random.shuffle(all_stim[i])
        all_stim[i].append(i)
    df_once = pd.DataFrame(all_stim,index=None)
    
    return df_once.transpose()

def rand_df():
    all_runs = pd.DataFrame()
    #generate 6 dataframes and concatenate them
    for i in range(5):
        df = cond_df()
        combined = [all_runs,df]
        all_runs = pd.concat(combined)
        
    # generate "correct" locations 
    all_runs["correct"] = [val for val in range(10)] * 55
    # shuffle the rows
    df = all_runs.sample(frac=1)
    
    df = df.reset_index(drop=True)
    #df["mouse"] = ""
    df["mousex"] = ""
    df["mousey"] = ""
    # put the id in 11th column in the correct location
    for i in range(df.shape[0]):
        str_frg = df.loc[i,10].split('_')[0]
        corr_pos = df.loc[i,'correct']
        
        orig_pos_id = df.loc[i,corr_pos]
        row = df.iloc[i]
        # find where the correct face originally is
        id_pos = row[row==str_frg+"_0.jpg"].index[0]
        df.loc[i,corr_pos] = str_frg+"_0.jpg"
        df.loc[i,id_pos] = orig_pos_id
        # generate a column for randomized mouse position
        polarity = [1,-1]
        x_id = random.sample(polarity,1)[0]
        y_id = random.sample(polarity,1)[0]
        #df.at[i,"mouse"] = [[np.round(random.random()*x_id,decimals=1)],[np.round(random.random()*y_id,decimals=1)]]  
        df.at[i,"mousex"] = np.round(random.random()*x_id,decimals=1)
        df.at[i,"mousey"] = np.round(random.random()*y_id,decimals=1)
        df.loc[i,"correct"] = "Image"+str(df.loc[i,"correct"])
        #print "Original image in location {0} is {1} and new image is {2}".format(id_pos,orig_pos_id,str_frg+"_0.jpg")
    
    
    # rename the columns
    df.columns = ["Image0", "Image1", "Image2", "Image3", "Image4", "Image5", "Image6", "Image7", "Image8", "Image9","ImageProbe","Correct","MouseX","MouseY"]
    fn = '/Users/vassiki/Desktop/blur_pilot/csv/conditions.csv'
    #return df
    df.to_csv(fn,index=False)
