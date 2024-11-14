######Code Version of Stroop Test Example Experiment
'''
Procedure Based on GUI
1. Display welcome_message routine (a e text stimuli) in the beginning of the experiment for 1 second
2. Display a trial routine
    a. have a textstim for fixation that contains information regarding the experiment
    b. have a textstim for the word that will display the variable "thisWord" on the screen, based on the variable from 
     the excel sheet, in the color of the variable "thisColor" from the Excel sheet
    c. keep track of the keys on the machine (whether they are left o right) and determine whether it is the right answer,
     record the data
3. Make a loop that reads in the conditions from the rows in thee Excel sheet that provides the conditions
'''

'''
1. import the valid libraries
2. make a csv file to save the data (check which variables need to be saved, and save them)
3. Find a way to  read the Excel sheet data
3. Create the loop handler for looping through the rows in the Excel Sheet
4. Assign the different rows into variables that can be referenced later
5. Create window and stimuli for the fixation and the word
6. Create some handy clocks
7. Display instructions and wait
8. Control the presentation of the word stimuli
9. Get input from the subject and save it to the csv file with response answers

'''

from psychopy import core, visual, gui, data, event
from psychopy.tools.filetools import fromFile, toFile
import numpy, random, csv

########Dont need to use the below because i dont want to borrow from the last parameters...
#try: #try to get a previous parameters file
#    expInfo = fromFile('lastParams.pickle')
#except: #if not there, can use a default set
#    expInfo = {'observer':'Lastname_Firstname'}
#expInfo['dateStr'] = data.getDateStr()# add the current time

expInfo = {'Last Name': ' ', 'First Name':' '}
expInfo['dateStr'] = data.getDateStr()

#present a dialogue to change params
dlg = gui.DlgFromDict(expInfo, title='Stroop Test', fixed=['dateStr'])
if dlg.OK:
    toFile('lastParams.pickle', expInfo) #save params to file for next time
else:
    core.quit() #the user hit cancel, so exit
    
csvfiledata = []
#Find a way to read the Excel sheet data
#https://python.land/data-processing/python-csv
#Dont need to do this tbh- I can use the importConditions() method
#with open('stroopconditions.csv', newline='') as f:
#    csvfile = csv.reader(f)
#    for row in csvfile:
#        csvfiledata.append(row)
#    
#    print(csvfiledata)
    
###How will the variables be iterated? When iterating through csvfiledata using x, $thisWord is csvfiledata[x][0]
#$thisColor is csvfiledata[x][1], $condition is csvfiledata[x][2], and $corrAns is csvfiledata[x][3] 
#Dont need to do this tbh- I can use the importConditions() method

conditions = data.importConditions('stroopconditions.xlsx')
#print(conditions)


##make a csv file to save the data
fileName = expInfo['Last Name'] + '_' + expInfo['First Name'] + 'StroopTest' + expInfo['dateStr']
dataFile = open(fileName + '.csv', 'w') # a simple text file with comma seperated values
dataFile.write('thisWord,thisColor,condition,corrAns,thisTrialN,thisRepN,key_resp.keys(),key_resp.corr,key_resp.rt,key_resp.duration,trials.thisRepN,trials.thisTrialN,trial.thisN,trials.thisIndex,notes,\n')

##Create the loop handler for looping through the different rows in csvfiledata
#will probably need to use TrialHandler class since I am dealing with a single loop (not Experiment Handler, which is used for multiple loops)
sequence = data.TrialHandler(trialList=conditions,nReps=2,method='sequential',originPath=None)
#print(sequence.trialList)


#while sequence.nRemaining:
#    print(sequence.thisTrial)
#    sequence.next()
 
 
#for item in sequence:
#    print(sequence.thisTrial)
#    sequence.next()

#Clocks
globalClock = core.Clock()
trialClock = core.Clock()

#Create window and stimuli for the message, fixation, and the word
win = visual.Window([800,600], allowGUI=True,monitor='testMonitor', units='deg')
welcome_message = visual.TextStim(win, pos=[0,0], text='Welcome to the Stroop Test! Press a button to continue.')
word = visual.TextStim(win, pos=[0,0])
fixation = visual.TextStim(win, pos=[0,-5], text='If the word says "red", press the left key. If the word says "blue", press the right key.')
#Display instructions and wait
welcome_message.draw()
win.flip()
event.waitKeys()
#print('check1')

#Control the presentation of the stimuli
for thisIncrement in sequence: #will continue the staircase until it terminates
    #set display of stimuli
    word.setText(thisIncrement["thisWord"])
    word.setColor(thisIncrement["thisColor"])
    
    #draw the stimuli
    word.draw()
    fixation.draw()
    win.flip()
    
    #get response
    thisResp = None
    pressedKey = None
    while thisResp == None:
        allKeys = event.waitKeys(keyList=['left','right'], timeStamped=True) ##making timestamped True because the docs say that you can record the timestamp, but allkeys will instead return a tuple of (key, timestamp)
        #print('check2')
        for thisKey in allKeys:
            if thisKey[0] == 'left':
                if thisIncrement['corrAns'] == 'left':
                    thisResp = 1
                elif thisIncrement['corrAns'] == 'right':
                    thisResp = 0
            if thisKey[0] == 'right':
                if thisIncrement['corrAns'] == 'right':
                    thisResp = 1
                elif thisIncrement['corrAns'] == 'left':
                    thisResp = 0
            if thisKey[0] in ['q','escape']:
                core.quit() #abort experiment
                event.clearEvents() #clear other (eg mouse) events - they clog the buffer
            pressedKey = thisKey[0]
            
        #add the data to the staircase so it can calculate the next level
        sequence.addData("corr",thisResp)
        
        thisWord = thisIncrement['thisWord']
        thisColor = thisIncrement['thisColor']
        condition = thisIncrement['condition']
        corrAns = thisIncrement['corrAns']
        ##All other TrialHandler variables
        thisTrialN = sequence.thisTrialN
        thisRepN = sequence.thisRepN
        key_resp_keys = pressedKey #pressedKey is present in the forloop
        key_resp_corr = thisResp
        key_resp_rt = thisKey[1]
        key_resp_duration = None
        trials_thisRepN = sequence.thisRepN
        trials_thisTrialN = sequence.thisTrialN
        trials_thisN = sequence.thisN
        trials_thisIndex = sequence.thisIndex
        notes = "None"
        #thisRow.t = thisRow.t
        
        #dataFile.write('thisTrialN,thisRepN,key_resp.keys(),key_resp.corr,key_resp.rt,key_resp.duration,trials.thisRepN,trials.thisTrialN,trial.thisN,trials.thisIndex,notes,\n')
        #dataFile.write('%i,%i,%i,%i,%.3f,%i,%i,%i,%i,%i,%i,\n' %(thisTrialN, thisRepN, key_resp_keys, key_resp_corr, key_resp_rt, key_resp_duration, trials_thisRepN, trials_thisTrialN, trials_thisN, trials_thisIndex, notes ))
        dataFile.write(f"{thisWord},{thisColor},{condition},{corrAns},{thisTrialN},{thisRepN},{key_resp_keys},{key_resp_corr},{key_resp_rt},{key_resp_duration},{trials_thisRepN},{trials_thisTrialN},{trials_thisN},{trials_thisIndex},{notes}, \n")
        core.wait(1)
        
#sequence has ended
dataFile.close()
sequence.saveAsPickle(fileName) #special python binary file to save all the info
#Need to keep track of time stamps for when words appear and when button is pressed
    
    
    
    
    
    










