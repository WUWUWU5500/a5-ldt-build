#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2026.2.4),
    on November 17, 2026, at 20:15
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout, hardware
from psychopy.tools import environmenttools
from psychopy.constants import (
    NOT_STARTED, STARTED, PLAYING, PAUSED, STOPPED, STOPPING, FINISHED, PRESSED, 
    RELEASED, FOREVER, priority
)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

from psychopy.hardware import keyboard

# --- Setup global variables (available in all functions) ---
# create a device manager to handle hardware (keyboards, mice, mirophones, speakers, etc.)
deviceManager = hardware.DeviceManager()
# ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
# store info about the experiment session
psychopyVersion = '2026.2.4'
expName = 'ldt'  # from the Builder filename that created this script
expVersion = ''
# a list of functions to run when the experiment ends (starts off blank)
runAtExit = []
# information about this experiment
expInfo = {
    'participant': '1',
    'session': '001',
    'date|hid': data.getDateStr(),
    'expName|hid': expName,
    'expVersion|hid': expVersion,
    'psychopyVersion|hid': psychopyVersion,
}

# --- Define some variables which will change depending on pilot mode ---
'''
To run in pilot mode, either use the run/pilot toggle in Builder, Coder and Runner, 
or run the experiment with `--pilot` as an argument. To change what pilot 
#mode does, check out the 'Pilot mode' tab in preferences.
'''
# work out from system args whether we are running in pilot mode
PILOTING = core.setPilotModeFromArgs()
# start off with values from experiment settings
_fullScr = True
_winSize = (1024, 768)
# if in pilot mode, apply overrides according to preferences
if PILOTING:
    # force windowed mode
    if prefs.piloting['forceWindowed']:
        _fullScr = False
        # set window size
        _winSize = prefs.piloting['forcedWindowSize']
    # replace default participant ID
    if prefs.piloting['replaceParticipantID']:
        expInfo['participant'] = 'pilot'

def showExpInfoDlg(expInfo):
    """
    Show participant info dialog.
    Parameters
    ==========
    expInfo : dict
        Information about this experiment.
    
    Returns
    ==========
    dict
        Information about this experiment.
    """
    # show participant info dialog
    dlg = gui.DlgFromDict(
        dictionary=expInfo, sortKeys=False, title=expName, alwaysOnTop=True
    )
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    # return expInfo
    return expInfo


def setupData(expInfo, dataDir=None):
    """
    Make an ExperimentHandler to handle trials and saving.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    dataDir : Path, str or None
        Folder to save the data to, leave as None to create a folder in the current directory.    
    Returns
    ==========
    psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    # remove dialog-specific syntax from expInfo
    for key, val in expInfo.copy().items():
        newKey, _ = data.utils.parsePipeSyntax(key)
        expInfo[newKey] = expInfo.pop(key)
    
    # data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    if dataDir is None:
        dataDir = _thisDir
    filename = 'data/' + expInfo['participant'] + '_' + expName + '_' + expInfo['date']
    # make sure filename is relative to dataDir
    if os.path.isabs(filename):
        dataDir = os.path.commonprefix([dataDir, filename])
        filename = os.path.relpath(filename, dataDir)
    
    # an ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(
        name=expName, version=expVersion,
        extraInfo=expInfo, runtimeInfo=None,
        originPath='C:\\Users\\zhaoc\\Desktop\\a5-ldt-build\\ldt.py',
        savePickle=True, saveWideText=True,
        dataFileName=dataDir + os.sep + filename, sortColumns='time'
    )
    # store pilot mode in data file
    thisExp.addData('piloting', PILOTING, priority=priority.LOW)
    thisExp.setPriority('thisRow.t', priority.CRITICAL)
    thisExp.setPriority('expName', priority.LOW)
    # return experiment handler
    return thisExp


def setupLogging(filename):
    """
    Setup a log file and tell it what level to log at.
    
    Parameters
    ==========
    filename : str or pathlib.Path
        Filename to save log file and data files as, doesn't need an extension.
    
    Returns
    ==========
    psychopy.logging.LogFile
        Text stream to receive inputs from the logging system.
    """
    # set how much information should be printed to the console / app
    if PILOTING:
        logging.console.setLevel(
            prefs.piloting['pilotConsoleLoggingLevel']
        )
    else:
        logging.console.setLevel('warning')
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log')
    if PILOTING:
        logFile.setLevel(
            prefs.piloting['pilotLoggingLevel']
        )
    else:
        logFile.setLevel(
            logging.getLevel('info')
        )
    
    return logFile


def setupWindow(expInfo=None, win=None):
    """
    Setup the Window
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    win : psychopy.visual.Window
        Window to setup - leave as None to create a new window.
    
    Returns
    ==========
    psychopy.visual.Window
        Window in which to run this experiment.
    """
    if PILOTING:
        logging.debug('Fullscreen settings ignored as running in pilot mode.')
    
    if win is None:
        # if not given a window to setup, make one
        win = visual.Window(
            size=_winSize, fullscr=_fullScr, screen=0,
            winType='pyglet', allowGUI=False, allowStencil=False,
            monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='height',
            checkTiming=False  # we're going to do this ourselves in a moment
        )
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [0,0,0]
        win.colorSpace = 'rgb'
        win.backgroundImage = ''
        win.backgroundFit = 'none'
        win.units = 'height'
    if expInfo is not None:
        # get/measure frame rate if not already in expInfo
        if win._monitorFrameRate is None:
            win._monitorFrameRate = win.getActualFrameRate(infoMsg='Attempting to measure frame rate of screen, please wait...')
        expInfo['frameRate'] = win._monitorFrameRate
    win.hideMessage()
    if PILOTING:
        # show a visual indicator if we're in piloting mode
        if prefs.piloting['showPilotingIndicator']:
            win.showPilotingIndicator()
        # always show the mouse in piloting mode
        if prefs.piloting['forceMouseVisible']:
            win.mouseVisible = True
    
    return win


def setupDevices(expInfo, thisExp, win):
    """
    Setup whatever devices are available (mouse, keyboard, speaker, eyetracker, etc.) and add them to 
    the device manager (deviceManager)
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window in which to run this experiment.
    Returns
    ==========
    bool
        True if completed successfully.
    """
    # --- Setup input devices ---
    ioConfig = {}
    ioSession = ioServer = eyetracker = None
    
    # store ioServer object in the device manager
    deviceManager.ioServer = ioServer
    
    # create a default keyboard (e.g. to check for escape)
    if deviceManager.getDevice('defaultKeyboard') is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='ptb'
        )
    # return True if completed successfully
    return True

def pauseExperiment(thisExp, win=None, timers=[], currentRoutine=None):
    """
    Pause this experiment, preventing the flow from advancing to the next routine until resumed.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    timers : list, tuple
        List of timers to reset once pausing is finished.
    currentRoutine : psychopy.data.Routine
        Current Routine we are in at time of pausing, if any. This object tells PsychoPy what Components to pause/play/dispatch.
    """
    # if we are not paused, do nothing
    if thisExp.status != PAUSED:
        return
    
    # start a timer to figure out how long we're paused for
    pauseTimer = core.Clock()
    # pause any playback components
    if currentRoutine is not None:
        for comp in currentRoutine.getPlaybackComponents():
            comp.pause()
    # make sure we have a keyboard
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        defaultKeyboard = deviceManager.addKeyboard(
            deviceClass='keyboard',
            deviceName='defaultKeyboard',
            backend='PsychToolbox',
        )
    # run a while loop while we wait to unpause
    while thisExp.status == PAUSED:
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=['escape']):
            endExperiment(thisExp, win=win)
        # dispatch messages on response components
        if currentRoutine is not None:
            for comp in currentRoutine.getDispatchComponents():
                comp.device.dispatchMessages()
        # sleep 1ms so other threads can execute
        clock.time.sleep(0.001)
    # if stop was requested while paused, quit
    if thisExp.status == FINISHED:
        endExperiment(thisExp, win=win)
    # resume any playback components
    if currentRoutine is not None:
        for comp in currentRoutine.getPlaybackComponents():
            comp.play()
    # reset any timers
    for timer in timers:
        timer.addTime(-pauseTimer.getTime())


def run(expInfo, thisExp, win, globalClock=None, thisSession=None):
    """
    Run the experiment flow.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    psychopy.visual.Window
        Window in which to run this experiment.
    globalClock : psychopy.core.clock.Clock or None
        Clock to get global time from - supply None to make a new one.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    # mark experiment as started
    thisExp.status = STARTED
    # update experiment info
    expInfo['date'] = data.getDateStr()
    expInfo['expName'] = expName
    expInfo['expVersion'] = expVersion
    expInfo['psychopyVersion'] = psychopyVersion
    # make sure window is set to foreground to prevent losing focus
    win.winHandle.activate()
    # make sure variables created by exec are available globally
    exec = environmenttools.setExecEnvironment(globals())
    # get device handles from dict of input devices
    ioServer = deviceManager.ioServer
    # get/create a default keyboard (e.g. to check for escape)
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='PsychToolbox'
        )
    eyetracker = deviceManager.getDevice('eyetracker')
    # make sure we're running in the directory for this experiment
    os.chdir(_thisDir)
    # get filename from ExperimentHandler for convenience
    filename = thisExp.dataFileName
    frameTolerance = 0.001  # how close to onset before 'same' frame
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    # get frame duration from frame rate in expInfo
    if 'frameRate' in expInfo and expInfo['frameRate'] is not None:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess
    
    # Start Code - component code to be run after the window creation
    
    # --- Initialize components for Routine "instructions" ---
    # Run 'Begin Experiment' code from instructionCode
    # Use the refresh rate actually measured by PsychoPy at startup.
    _measured_hz = expInfo.get('frameRate')
    if _measured_hz is None or float(_measured_hz) <= 0:
        raise RuntimeError("Q5 requires a measurable, stable screen frame rate.")
    ldt_hz = int(round(float(_measured_hz)))
    if ldt_hz <= 0:
        raise RuntimeError("Invalid measured screen frame rate")
    # Store the rounded rate required by Q5 in the output file.
    expInfo['frameRate'] = ldt_hz
    fixFrames = int(round(500 * ldt_hz / 1000))
    primeFrames = int(round(150 * ldt_hz / 1000))
    targetFrames = int(round(2000 * ldt_hz / 1000))
    feedbackFrames = int(round(1000 * ldt_hz / 1000))
    itiFrames = int(round(500 * ldt_hz / 1000))
    endFrames = int(round(2000 * ldt_hz / 1000))
    # Run 'Begin Experiment' code from a6SessionFrameCode
    # A6 I1/I2: log ONLY trial-screen flips, with a 1.5-frame drop threshold.
    # frameDur was calculated by Builder from the measured, rounded frame rate.
    win.refreshThreshold = 1.5 * frameDur
    win.recordFrameIntervals = False
    # Exclude anything accumulated during startup / frame-rate measurement.
    win.frameIntervals = []
    win.nDroppedFrames = 0
    instructionsText = visual.TextStim(win=win, name='instructionsText',
        text='',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    instructionsKey = keyboard.Keyboard(deviceName='defaultKeyboard', backend='PsychToolbox')
    
    # --- Initialize components for Routine "trial" ---
    fixation = visual.TextStim(win=win, name='fixation',
        text='+',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    primeStim = visual.TextStim(win=win, name='primeStim',
        text='',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-3.0);
    targetStim = visual.TextStim(win=win, name='targetStim',
        text='',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-4.0);
    trialKey = keyboard.Keyboard(deviceName='defaultKeyboard', backend='PsychToolbox')
    
    # --- Initialize components for Routine "practiceFeedback" ---
    feedbackText = visual.TextStim(win=win, name='feedbackText',
        text='',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    
    # --- Initialize components for Routine "iti" ---
    blankText = visual.TextStim(win=win, name='blankText',
        text=' ',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # --- Initialize components for Routine "breakScreen" ---
    breakText = visual.TextStim(win=win, name='breakText',
        text='Practice complete. Press SPACE to begin the main experiment.',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    breakKey = keyboard.Keyboard(deviceName='defaultKeyboard', backend='PsychToolbox')
    
    # --- Initialize components for Routine "trial" ---
    fixation = visual.TextStim(win=win, name='fixation',
        text='+',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    primeStim = visual.TextStim(win=win, name='primeStim',
        text='',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-3.0);
    targetStim = visual.TextStim(win=win, name='targetStim',
        text='',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-4.0);
    trialKey = keyboard.Keyboard(deviceName='defaultKeyboard', backend='PsychToolbox')
    
    # --- Initialize components for Routine "iti" ---
    blankText = visual.TextStim(win=win, name='blankText',
        text=' ',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # --- Initialize components for Routine "endScreen" ---
    endText = visual.TextStim(win=win, name='endText',
        text='Thank you for participating!',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # create some handy timers
    
    # global clock to track the time since experiment started
    if globalClock is None:
        # create a clock if not given one
        globalClock = core.Clock()
    if isinstance(globalClock, str):
        # if given a string, make a clock accoridng to it
        if globalClock == 'float':
            # get timestamps as a simple value
            globalClock = core.Clock(format='float')
        elif globalClock == 'iso':
            # get timestamps in ISO format
            globalClock = core.Clock(format='%Y-%m-%d_%H:%M:%S.%f%z')
        else:
            # get timestamps in a custom format
            globalClock = core.Clock(format=globalClock)
    if ioServer is not None:
        ioServer.syncClock(globalClock)
    logging.setDefaultClock(globalClock)
    if eyetracker is not None:
        eyetracker.enableEventReporting()
    # routine timer to track time remaining of each (possibly non-slip) routine
    routineTimer = core.Clock()
    win.flip()  # flip window to reset last flip timer
    # store the exact time the global clock started
    expInfo['expStart'] = data.getDateStr(
        format='%Y-%m-%d %Hh%M.%S.%f %z', fractionalSecondDigits=6
    )
    
    # --- Prepare to start Routine "instructions" ---
    # create an object to store info about Routine instructions
    instructions = data.Routine(
        name='instructions',
        components=[instructionsText, instructionsKey],
    )
    instructions.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from instructionCode
    if int(expInfo['participant']) % 2 == 1:
        instruction_msg = "Press F for WORD and J for NONWORD.\n\nPress SPACE to begin."
    else:
        instruction_msg = "Press J for WORD and F for NONWORD.\n\nPress SPACE to begin."
    instructionsText.setText(instruction_msg)
    # create starting attributes for instructionsKey
    instructionsKey.keys = []
    instructionsKey.rt = []
    _instructionsKey_allKeys = []
    # store start times for instructions
    instructions.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    instructions.tStart = globalClock.getTime(format='float')
    instructions.status = STARTED
    thisExp.addData('instructions.started', instructions.tStart)
    instructions.maxDuration = None
    # keep track of which components have finished
    instructionsComponents = instructions.components
    for thisComponent in instructions.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "instructions" ---
    thisExp.currentRoutine = instructions
    instructions.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *instructionsText* updates
        
        # if instructionsText is starting this frame...
        if instructionsText.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            instructionsText.frameNStart = frameN  # exact frame index
            instructionsText.tStart = t  # local t and not account for scr refresh
            instructionsText.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instructionsText, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'instructionsText.started')
            # update status
            instructionsText.status = STARTED
            instructionsText.setAutoDraw(True)
        
        # if instructionsText is active this frame...
        if instructionsText.status == STARTED:
            # update params
            pass
        
        # *instructionsKey* updates
        waitOnFlip = False
        
        # if instructionsKey is starting this frame...
        if instructionsKey.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            instructionsKey.frameNStart = frameN  # exact frame index
            instructionsKey.tStart = t  # local t and not account for scr refresh
            instructionsKey.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instructionsKey, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'instructionsKey.started')
            # update status
            instructionsKey.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(instructionsKey.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(instructionsKey.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if instructionsKey.status == STARTED and not waitOnFlip:
            theseKeys = instructionsKey.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _instructionsKey_allKeys.extend(theseKeys)
            if len(_instructionsKey_allKeys):
                instructionsKey.keys = _instructionsKey_allKeys[0].name  # just the first key pressed
                instructionsKey.rt = _instructionsKey_allKeys[0].rt
                instructionsKey.duration = _instructionsKey_allKeys[0].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer, globalClock], 
                currentRoutine=instructions,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            instructions.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if instructions.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in instructions.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "instructions" ---
    for thisComponent in instructions.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for instructions
    instructions.tStop = globalClock.getTime(format='float')
    instructions.tStopRefresh = tThisFlipGlobal
    thisExp.addData('instructions.stopped', instructions.tStop)
    # check responses
    if instructionsKey.keys in ['', [], None]:  # No response was made
        instructionsKey.keys = None
    thisExp.addData('instructionsKey.keys',instructionsKey.keys)
    if instructionsKey.keys != None:  # we had a response
        thisExp.addData('instructionsKey.rt', instructionsKey.rt)
        thisExp.addData('instructionsKey.duration', instructionsKey.duration)
    thisExp.nextEntry()
    # the Routine "instructions" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    practiceLoop = data.TrialHandler2(
        name='practiceLoop',
        nReps=1, 
        method='sequential', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=data.importConditions(
        'trial_lists/trials_p%02d.csv' % int(expInfo['participant']), 
        selection=list(range(0, 8))
    )
    , 
        seed=None, 
        isTrials=True, 
    )
    thisExp.addLoop(practiceLoop)  # add the loop to the experiment
    thisPracticeLoop = practiceLoop.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisPracticeLoop.rgb)
    if thisPracticeLoop != None:
        for paramName in thisPracticeLoop:
            globals()[paramName] = thisPracticeLoop[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisPracticeLoop in practiceLoop:
        practiceLoop.status = STARTED
        if hasattr(thisPracticeLoop, 'status'):
            thisPracticeLoop.status = STARTED
        currentLoop = practiceLoop
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisPracticeLoop.rgb)
        if thisPracticeLoop != None:
            for paramName in thisPracticeLoop:
                globals()[paramName] = thisPracticeLoop[paramName]
        
        # --- Prepare to start Routine "trial" ---
        # create an object to store info about Routine trial
        trial = data.Routine(
            name='trial',
            components=[fixation, primeStim, targetStim, trialKey],
        )
        trial.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from trialTimingCode
        # Selected SOA comes from the CSV for the current trial.
        soaFrames = int(round(float(soa) * ldt_hz / 1000))
        if soaFrames < primeFrames:
            raise ValueError("SOA shorter than prime duration")
        # Run 'Begin Routine' code from a6FrameCode
        # Start recording before the fixation-onset flip. PsychoPy ignores the
        # first interval after enabling recording, excluding the preceding screen.
        a6_drop_start = win.nDroppedFrames
        win.recordFrameIntervals = True
        primeStim.setText(prime)
        targetStim.setText(target.upper())
        # create starting attributes for trialKey
        trialKey.keys = []
        trialKey.rt = []
        _trialKey_allKeys = []
        # store start times for trial
        trial.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        trial.tStart = globalClock.getTime(format='float')
        trial.status = STARTED
        thisExp.addData('trial.started', trial.tStart)
        trial.maxDuration = None
        # keep track of which components have finished
        trialComponents = trial.components
        for thisComponent in trial.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "trial" ---
        thisExp.currentRoutine = trial
        trial.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # if trial has changed, end Routine now
            if hasattr(thisPracticeLoop, 'status') and thisPracticeLoop.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            # Run 'Each Frame' code from a6FrameCode
            # The trial routine contains fixation, prime, and target only.
            # Feedback and ITI are separate routines, so the end-routine hook below
            # switches recording off after the last target-visible flip.
            
            # *fixation* updates
            
            # if fixation is starting this frame...
            if fixation.status == NOT_STARTED and frameN >= 0:
                # keep track of start time/frame for later
                fixation.frameNStart = frameN  # exact frame index
                fixation.tStart = t  # local t and not account for scr refresh
                fixation.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fixation, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fixation.started')
                # update status
                fixation.status = STARTED
                fixation.setAutoDraw(True)
            
            # if fixation is active this frame...
            if fixation.status == STARTED:
                # update params
                pass
            
            # if fixation is stopping this frame...
            if fixation.status == STARTED:
                if frameN >= (fixation.frameNStart + fixFrames):
                    # keep track of stop time/frame for later
                    fixation.tStop = t  # not accounting for scr refresh
                    fixation.tStopRefresh = tThisFlipGlobal  # on global time
                    fixation.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'fixation.stopped')
                    # update status
                    fixation.status = FINISHED
                    fixation.setAutoDraw(False)
            
            # *primeStim* updates
            
            # if primeStim is starting this frame...
            if primeStim.status == NOT_STARTED and frameN >= fixFrames:
                # keep track of start time/frame for later
                primeStim.frameNStart = frameN  # exact frame index
                primeStim.tStart = t  # local t and not account for scr refresh
                primeStim.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(primeStim, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'primeStim.started')
                # update status
                primeStim.status = STARTED
                primeStim.setAutoDraw(True)
            
            # if primeStim is active this frame...
            if primeStim.status == STARTED:
                # update params
                pass
            
            # if primeStim is stopping this frame...
            if primeStim.status == STARTED:
                if frameN >= (primeStim.frameNStart + primeFrames):
                    # keep track of stop time/frame for later
                    primeStim.tStop = t  # not accounting for scr refresh
                    primeStim.tStopRefresh = tThisFlipGlobal  # on global time
                    primeStim.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'primeStim.stopped')
                    # update status
                    primeStim.status = FINISHED
                    primeStim.setAutoDraw(False)
            
            # *targetStim* updates
            
            # if targetStim is starting this frame...
            if targetStim.status == NOT_STARTED and frameN >= fixFrames + soaFrames:
                # keep track of start time/frame for later
                targetStim.frameNStart = frameN  # exact frame index
                targetStim.tStart = t  # local t and not account for scr refresh
                targetStim.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(targetStim, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'targetStim.started')
                # update status
                targetStim.status = STARTED
                targetStim.setAutoDraw(True)
            
            # if targetStim is active this frame...
            if targetStim.status == STARTED:
                # update params
                pass
            
            # if targetStim is stopping this frame...
            if targetStim.status == STARTED:
                if frameN >= (targetStim.frameNStart + targetFrames):
                    # keep track of stop time/frame for later
                    targetStim.tStop = t  # not accounting for scr refresh
                    targetStim.tStopRefresh = tThisFlipGlobal  # on global time
                    targetStim.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'targetStim.stopped')
                    # update status
                    targetStim.status = FINISHED
                    targetStim.setAutoDraw(False)
            
            # *trialKey* updates
            waitOnFlip = False
            
            # if trialKey is starting this frame...
            if trialKey.status == NOT_STARTED and frameN >= fixFrames + soaFrames:
                # keep track of start time/frame for later
                trialKey.frameNStart = frameN  # exact frame index
                trialKey.tStart = t  # local t and not account for scr refresh
                trialKey.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(trialKey, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'trialKey.started')
                # update status
                trialKey.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(trialKey.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(trialKey.clearEvents, eventType='keyboard')  # clear events on next screen flip
            
            # if trialKey is stopping this frame...
            if trialKey.status == STARTED:
                if frameN >= (trialKey.frameNStart + targetFrames):
                    # keep track of stop time/frame for later
                    trialKey.tStop = t  # not accounting for scr refresh
                    trialKey.tStopRefresh = tThisFlipGlobal  # on global time
                    trialKey.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'trialKey.stopped')
                    # update status
                    trialKey.status = FINISHED
                    trialKey.status = FINISHED
            if trialKey.status == STARTED and not waitOnFlip:
                theseKeys = trialKey.getKeys(keyList=['f', 'j'], ignoreKeys=["escape"], waitRelease=False)
                _trialKey_allKeys.extend(theseKeys)
                if len(_trialKey_allKeys):
                    trialKey.keys = _trialKey_allKeys[0].name  # just the first key pressed
                    trialKey.rt = _trialKey_allKeys[0].rt
                    trialKey.duration = _trialKey_allKeys[0].duration
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=trial,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                trial.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if trial.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in trial.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "trial" ---
        for thisComponent in trial.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for trial
        trial.tStop = globalClock.getTime(format='float')
        trial.tStopRefresh = tThisFlipGlobal
        thisExp.addData('trial.stopped', trial.tStop)
        # Run 'End Routine' code from a6FrameCode
        # End the recording BEFORE the feedback/ITI or the next trial's first flip.
        # nDroppedFrames increments on each recorded interval > refreshThreshold.
        win.recordFrameIntervals = False
        thisExp.addData('dropped_frames', int(win.nDroppedFrames - a6_drop_start))
        # check responses
        if trialKey.keys in ['', [], None]:  # No response was made
            trialKey.keys = None
        practiceLoop.addData('trialKey.keys',trialKey.keys)
        if trialKey.keys != None:  # we had a response
            practiceLoop.addData('trialKey.rt', trialKey.rt)
            practiceLoop.addData('trialKey.duration', trialKey.duration)
        # Run 'End Routine' code from trialRecordCode
        # Built-in Builder components have now finished presenting and listening.
        # tStartRefresh is on the same experiment clock as the *.started columns.
        shown_prime = str(primeStim.text)
        shown_target = str(targetStim.text)
        pressed = trialKey.keys
        if isinstance(pressed, (list, tuple)):
            pressed = pressed[0] if pressed else None
        if pressed not in ('f', 'j'):
            pressed = None
        raw_rt = trialKey.rt
        if isinstance(raw_rt, (list, tuple)):
            raw_rt = raw_rt[0] if raw_rt else None
        ldt_timeout = int(pressed is None)
        ldt_rt = float(raw_rt) if not ldt_timeout and raw_rt is not None else None
        word_key = 'f' if int(expInfo['participant']) % 2 else 'j'
        expected_key = word_key if str(correct_response) == 'word' else ('j' if word_key == 'f' else 'f')
        ldt_accuracy = int(pressed is not None and pressed == expected_key)
        thisExp.addData('prime_shown', shown_prime)
        thisExp.addData('target_shown', shown_target)
        thisExp.addData('prime_onset', primeStim.tStartRefresh)
        thisExp.addData('target_onset', targetStim.tStartRefresh)
        thisExp.addData('key', pressed if pressed is not None else '')
        thisExp.addData('rt', ldt_rt if ldt_rt is not None else '')
        thisExp.addData('accuracy', ldt_accuracy)
        thisExp.addData('timeout', ldt_timeout)
        # the Routine "trial" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "practiceFeedback" ---
        # create an object to store info about Routine practiceFeedback
        practiceFeedback = data.Routine(
            name='practiceFeedback',
            components=[feedbackText],
        )
        practiceFeedback.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from feedbackCode
        response = trialKey.keys
        
        if response is None or response == []:
            feedback_msg = "Too slow"
        else:
            word_key = 'f' if int(expInfo['participant']) % 2 == 1 else 'j'
            nonword_key = 'j' if word_key == 'f' else 'f'
        
            expected_key = word_key if correct_response == 'word' else nonword_key
        
            if response == expected_key:
                feedback_msg = "Correct"
            else:
                feedback_msg = "Incorrect"
        feedbackText.setText(feedback_msg)
        # store start times for practiceFeedback
        practiceFeedback.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        practiceFeedback.tStart = globalClock.getTime(format='float')
        practiceFeedback.status = STARTED
        thisExp.addData('practiceFeedback.started', practiceFeedback.tStart)
        practiceFeedback.maxDuration = None
        # keep track of which components have finished
        practiceFeedbackComponents = practiceFeedback.components
        for thisComponent in practiceFeedback.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "practiceFeedback" ---
        thisExp.currentRoutine = practiceFeedback
        practiceFeedback.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # if trial has changed, end Routine now
            if hasattr(thisPracticeLoop, 'status') and thisPracticeLoop.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *feedbackText* updates
            
            # if feedbackText is starting this frame...
            if feedbackText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                feedbackText.frameNStart = frameN  # exact frame index
                feedbackText.tStart = t  # local t and not account for scr refresh
                feedbackText.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(feedbackText, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'feedbackText.started')
                # update status
                feedbackText.status = STARTED
                feedbackText.setAutoDraw(True)
            
            # if feedbackText is active this frame...
            if feedbackText.status == STARTED:
                # update params
                pass
            
            # if feedbackText is stopping this frame...
            if feedbackText.status == STARTED:
                if frameN >= (feedbackText.frameNStart + feedbackFrames):
                    # keep track of stop time/frame for later
                    feedbackText.tStop = t  # not accounting for scr refresh
                    feedbackText.tStopRefresh = tThisFlipGlobal  # on global time
                    feedbackText.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'feedbackText.stopped')
                    # update status
                    feedbackText.status = FINISHED
                    feedbackText.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=practiceFeedback,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                practiceFeedback.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if practiceFeedback.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in practiceFeedback.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "practiceFeedback" ---
        for thisComponent in practiceFeedback.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for practiceFeedback
        practiceFeedback.tStop = globalClock.getTime(format='float')
        practiceFeedback.tStopRefresh = tThisFlipGlobal
        thisExp.addData('practiceFeedback.stopped', practiceFeedback.tStop)
        # the Routine "practiceFeedback" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "iti" ---
        # create an object to store info about Routine iti
        iti = data.Routine(
            name='iti',
            components=[blankText],
        )
        iti.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # store start times for iti
        iti.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        iti.tStart = globalClock.getTime(format='float')
        iti.status = STARTED
        thisExp.addData('iti.started', iti.tStart)
        iti.maxDuration = None
        # keep track of which components have finished
        itiComponents = iti.components
        for thisComponent in iti.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "iti" ---
        thisExp.currentRoutine = iti
        iti.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # if trial has changed, end Routine now
            if hasattr(thisPracticeLoop, 'status') and thisPracticeLoop.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *blankText* updates
            
            # if blankText is starting this frame...
            if blankText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                blankText.frameNStart = frameN  # exact frame index
                blankText.tStart = t  # local t and not account for scr refresh
                blankText.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(blankText, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'blankText.started')
                # update status
                blankText.status = STARTED
                blankText.setAutoDraw(True)
            
            # if blankText is active this frame...
            if blankText.status == STARTED:
                # update params
                pass
            
            # if blankText is stopping this frame...
            if blankText.status == STARTED:
                if frameN >= (blankText.frameNStart + itiFrames):
                    # keep track of stop time/frame for later
                    blankText.tStop = t  # not accounting for scr refresh
                    blankText.tStopRefresh = tThisFlipGlobal  # on global time
                    blankText.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'blankText.stopped')
                    # update status
                    blankText.status = FINISHED
                    blankText.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=iti,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                iti.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if iti.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in iti.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "iti" ---
        for thisComponent in iti.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for iti
        iti.tStop = globalClock.getTime(format='float')
        iti.tStopRefresh = tThisFlipGlobal
        thisExp.addData('iti.stopped', iti.tStop)
        # the Routine "iti" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        # mark thisPracticeLoop as finished
        if hasattr(thisPracticeLoop, 'status'):
            thisPracticeLoop.status = FINISHED
        # if awaiting a pause, pause now
        if practiceLoop.status == PAUSED:
            thisExp.status = PAUSED
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[globalClock], 
            )
            # once done pausing, restore running status
            practiceLoop.status = STARTED
        thisExp.nextEntry()
        
    # completed 1 repeats of 'practiceLoop'
    practiceLoop.status = FINISHED
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # --- Prepare to start Routine "breakScreen" ---
    # create an object to store info about Routine breakScreen
    breakScreen = data.Routine(
        name='breakScreen',
        components=[breakText, breakKey],
    )
    breakScreen.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for breakKey
    breakKey.keys = []
    breakKey.rt = []
    _breakKey_allKeys = []
    # store start times for breakScreen
    breakScreen.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    breakScreen.tStart = globalClock.getTime(format='float')
    breakScreen.status = STARTED
    thisExp.addData('breakScreen.started', breakScreen.tStart)
    breakScreen.maxDuration = None
    # keep track of which components have finished
    breakScreenComponents = breakScreen.components
    for thisComponent in breakScreen.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "breakScreen" ---
    thisExp.currentRoutine = breakScreen
    breakScreen.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *breakText* updates
        
        # if breakText is starting this frame...
        if breakText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            breakText.frameNStart = frameN  # exact frame index
            breakText.tStart = t  # local t and not account for scr refresh
            breakText.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(breakText, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'breakText.started')
            # update status
            breakText.status = STARTED
            breakText.setAutoDraw(True)
        
        # if breakText is active this frame...
        if breakText.status == STARTED:
            # update params
            pass
        
        # *breakKey* updates
        waitOnFlip = False
        
        # if breakKey is starting this frame...
        if breakKey.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            breakKey.frameNStart = frameN  # exact frame index
            breakKey.tStart = t  # local t and not account for scr refresh
            breakKey.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(breakKey, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'breakKey.started')
            # update status
            breakKey.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(breakKey.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(breakKey.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if breakKey.status == STARTED and not waitOnFlip:
            theseKeys = breakKey.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _breakKey_allKeys.extend(theseKeys)
            if len(_breakKey_allKeys):
                breakKey.keys = _breakKey_allKeys[0].name  # just the first key pressed
                breakKey.rt = _breakKey_allKeys[0].rt
                breakKey.duration = _breakKey_allKeys[0].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer, globalClock], 
                currentRoutine=breakScreen,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            breakScreen.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if breakScreen.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in breakScreen.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "breakScreen" ---
    for thisComponent in breakScreen.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for breakScreen
    breakScreen.tStop = globalClock.getTime(format='float')
    breakScreen.tStopRefresh = tThisFlipGlobal
    thisExp.addData('breakScreen.stopped', breakScreen.tStop)
    # check responses
    if breakKey.keys in ['', [], None]:  # No response was made
        breakKey.keys = None
    thisExp.addData('breakKey.keys',breakKey.keys)
    if breakKey.keys != None:  # we had a response
        thisExp.addData('breakKey.rt', breakKey.rt)
        thisExp.addData('breakKey.duration', breakKey.duration)
    thisExp.nextEntry()
    # the Routine "breakScreen" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    mainLoop = data.TrialHandler2(
        name='mainLoop',
        nReps=1, 
        method='sequential', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=data.importConditions(
        'trial_lists/trials_p%02d.csv' % int(expInfo['participant']), 
        selection=list(range(8, 104))
    )
    , 
        seed=None, 
        isTrials=True, 
    )
    thisExp.addLoop(mainLoop)  # add the loop to the experiment
    thisMainLoop = mainLoop.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisMainLoop.rgb)
    if thisMainLoop != None:
        for paramName in thisMainLoop:
            globals()[paramName] = thisMainLoop[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisMainLoop in mainLoop:
        mainLoop.status = STARTED
        if hasattr(thisMainLoop, 'status'):
            thisMainLoop.status = STARTED
        currentLoop = mainLoop
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisMainLoop.rgb)
        if thisMainLoop != None:
            for paramName in thisMainLoop:
                globals()[paramName] = thisMainLoop[paramName]
        
        # --- Prepare to start Routine "trial" ---
        # create an object to store info about Routine trial
        trial = data.Routine(
            name='trial',
            components=[fixation, primeStim, targetStim, trialKey],
        )
        trial.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from trialTimingCode
        # Selected SOA comes from the CSV for the current trial.
        soaFrames = int(round(float(soa) * ldt_hz / 1000))
        if soaFrames < primeFrames:
            raise ValueError("SOA shorter than prime duration")
        # Run 'Begin Routine' code from a6FrameCode
        # Start recording before the fixation-onset flip. PsychoPy ignores the
        # first interval after enabling recording, excluding the preceding screen.
        a6_drop_start = win.nDroppedFrames
        win.recordFrameIntervals = True
        primeStim.setText(prime)
        targetStim.setText(target.upper())
        # create starting attributes for trialKey
        trialKey.keys = []
        trialKey.rt = []
        _trialKey_allKeys = []
        # store start times for trial
        trial.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        trial.tStart = globalClock.getTime(format='float')
        trial.status = STARTED
        thisExp.addData('trial.started', trial.tStart)
        trial.maxDuration = None
        # keep track of which components have finished
        trialComponents = trial.components
        for thisComponent in trial.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "trial" ---
        thisExp.currentRoutine = trial
        trial.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # if trial has changed, end Routine now
            if hasattr(thisMainLoop, 'status') and thisMainLoop.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            # Run 'Each Frame' code from a6FrameCode
            # The trial routine contains fixation, prime, and target only.
            # Feedback and ITI are separate routines, so the end-routine hook below
            # switches recording off after the last target-visible flip.
            
            # *fixation* updates
            
            # if fixation is starting this frame...
            if fixation.status == NOT_STARTED and frameN >= 0:
                # keep track of start time/frame for later
                fixation.frameNStart = frameN  # exact frame index
                fixation.tStart = t  # local t and not account for scr refresh
                fixation.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fixation, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fixation.started')
                # update status
                fixation.status = STARTED
                fixation.setAutoDraw(True)
            
            # if fixation is active this frame...
            if fixation.status == STARTED:
                # update params
                pass
            
            # if fixation is stopping this frame...
            if fixation.status == STARTED:
                if frameN >= (fixation.frameNStart + fixFrames):
                    # keep track of stop time/frame for later
                    fixation.tStop = t  # not accounting for scr refresh
                    fixation.tStopRefresh = tThisFlipGlobal  # on global time
                    fixation.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'fixation.stopped')
                    # update status
                    fixation.status = FINISHED
                    fixation.setAutoDraw(False)
            
            # *primeStim* updates
            
            # if primeStim is starting this frame...
            if primeStim.status == NOT_STARTED and frameN >= fixFrames:
                # keep track of start time/frame for later
                primeStim.frameNStart = frameN  # exact frame index
                primeStim.tStart = t  # local t and not account for scr refresh
                primeStim.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(primeStim, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'primeStim.started')
                # update status
                primeStim.status = STARTED
                primeStim.setAutoDraw(True)
            
            # if primeStim is active this frame...
            if primeStim.status == STARTED:
                # update params
                pass
            
            # if primeStim is stopping this frame...
            if primeStim.status == STARTED:
                if frameN >= (primeStim.frameNStart + primeFrames):
                    # keep track of stop time/frame for later
                    primeStim.tStop = t  # not accounting for scr refresh
                    primeStim.tStopRefresh = tThisFlipGlobal  # on global time
                    primeStim.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'primeStim.stopped')
                    # update status
                    primeStim.status = FINISHED
                    primeStim.setAutoDraw(False)
            
            # *targetStim* updates
            
            # if targetStim is starting this frame...
            if targetStim.status == NOT_STARTED and frameN >= fixFrames + soaFrames:
                # keep track of start time/frame for later
                targetStim.frameNStart = frameN  # exact frame index
                targetStim.tStart = t  # local t and not account for scr refresh
                targetStim.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(targetStim, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'targetStim.started')
                # update status
                targetStim.status = STARTED
                targetStim.setAutoDraw(True)
            
            # if targetStim is active this frame...
            if targetStim.status == STARTED:
                # update params
                pass
            
            # if targetStim is stopping this frame...
            if targetStim.status == STARTED:
                if frameN >= (targetStim.frameNStart + targetFrames):
                    # keep track of stop time/frame for later
                    targetStim.tStop = t  # not accounting for scr refresh
                    targetStim.tStopRefresh = tThisFlipGlobal  # on global time
                    targetStim.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'targetStim.stopped')
                    # update status
                    targetStim.status = FINISHED
                    targetStim.setAutoDraw(False)
            
            # *trialKey* updates
            waitOnFlip = False
            
            # if trialKey is starting this frame...
            if trialKey.status == NOT_STARTED and frameN >= fixFrames + soaFrames:
                # keep track of start time/frame for later
                trialKey.frameNStart = frameN  # exact frame index
                trialKey.tStart = t  # local t and not account for scr refresh
                trialKey.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(trialKey, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'trialKey.started')
                # update status
                trialKey.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(trialKey.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(trialKey.clearEvents, eventType='keyboard')  # clear events on next screen flip
            
            # if trialKey is stopping this frame...
            if trialKey.status == STARTED:
                if frameN >= (trialKey.frameNStart + targetFrames):
                    # keep track of stop time/frame for later
                    trialKey.tStop = t  # not accounting for scr refresh
                    trialKey.tStopRefresh = tThisFlipGlobal  # on global time
                    trialKey.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'trialKey.stopped')
                    # update status
                    trialKey.status = FINISHED
                    trialKey.status = FINISHED
            if trialKey.status == STARTED and not waitOnFlip:
                theseKeys = trialKey.getKeys(keyList=['f', 'j'], ignoreKeys=["escape"], waitRelease=False)
                _trialKey_allKeys.extend(theseKeys)
                if len(_trialKey_allKeys):
                    trialKey.keys = _trialKey_allKeys[0].name  # just the first key pressed
                    trialKey.rt = _trialKey_allKeys[0].rt
                    trialKey.duration = _trialKey_allKeys[0].duration
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=trial,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                trial.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if trial.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in trial.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "trial" ---
        for thisComponent in trial.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for trial
        trial.tStop = globalClock.getTime(format='float')
        trial.tStopRefresh = tThisFlipGlobal
        thisExp.addData('trial.stopped', trial.tStop)
        # Run 'End Routine' code from a6FrameCode
        # End the recording BEFORE the feedback/ITI or the next trial's first flip.
        # nDroppedFrames increments on each recorded interval > refreshThreshold.
        win.recordFrameIntervals = False
        thisExp.addData('dropped_frames', int(win.nDroppedFrames - a6_drop_start))
        # check responses
        if trialKey.keys in ['', [], None]:  # No response was made
            trialKey.keys = None
        mainLoop.addData('trialKey.keys',trialKey.keys)
        if trialKey.keys != None:  # we had a response
            mainLoop.addData('trialKey.rt', trialKey.rt)
            mainLoop.addData('trialKey.duration', trialKey.duration)
        # Run 'End Routine' code from trialRecordCode
        # Built-in Builder components have now finished presenting and listening.
        # tStartRefresh is on the same experiment clock as the *.started columns.
        shown_prime = str(primeStim.text)
        shown_target = str(targetStim.text)
        pressed = trialKey.keys
        if isinstance(pressed, (list, tuple)):
            pressed = pressed[0] if pressed else None
        if pressed not in ('f', 'j'):
            pressed = None
        raw_rt = trialKey.rt
        if isinstance(raw_rt, (list, tuple)):
            raw_rt = raw_rt[0] if raw_rt else None
        ldt_timeout = int(pressed is None)
        ldt_rt = float(raw_rt) if not ldt_timeout and raw_rt is not None else None
        word_key = 'f' if int(expInfo['participant']) % 2 else 'j'
        expected_key = word_key if str(correct_response) == 'word' else ('j' if word_key == 'f' else 'f')
        ldt_accuracy = int(pressed is not None and pressed == expected_key)
        thisExp.addData('prime_shown', shown_prime)
        thisExp.addData('target_shown', shown_target)
        thisExp.addData('prime_onset', primeStim.tStartRefresh)
        thisExp.addData('target_onset', targetStim.tStartRefresh)
        thisExp.addData('key', pressed if pressed is not None else '')
        thisExp.addData('rt', ldt_rt if ldt_rt is not None else '')
        thisExp.addData('accuracy', ldt_accuracy)
        thisExp.addData('timeout', ldt_timeout)
        # the Routine "trial" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "iti" ---
        # create an object to store info about Routine iti
        iti = data.Routine(
            name='iti',
            components=[blankText],
        )
        iti.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # store start times for iti
        iti.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        iti.tStart = globalClock.getTime(format='float')
        iti.status = STARTED
        thisExp.addData('iti.started', iti.tStart)
        iti.maxDuration = None
        # keep track of which components have finished
        itiComponents = iti.components
        for thisComponent in iti.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "iti" ---
        thisExp.currentRoutine = iti
        iti.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # if trial has changed, end Routine now
            if hasattr(thisMainLoop, 'status') and thisMainLoop.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *blankText* updates
            
            # if blankText is starting this frame...
            if blankText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                blankText.frameNStart = frameN  # exact frame index
                blankText.tStart = t  # local t and not account for scr refresh
                blankText.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(blankText, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'blankText.started')
                # update status
                blankText.status = STARTED
                blankText.setAutoDraw(True)
            
            # if blankText is active this frame...
            if blankText.status == STARTED:
                # update params
                pass
            
            # if blankText is stopping this frame...
            if blankText.status == STARTED:
                if frameN >= (blankText.frameNStart + itiFrames):
                    # keep track of stop time/frame for later
                    blankText.tStop = t  # not accounting for scr refresh
                    blankText.tStopRefresh = tThisFlipGlobal  # on global time
                    blankText.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'blankText.stopped')
                    # update status
                    blankText.status = FINISHED
                    blankText.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=iti,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                iti.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if iti.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in iti.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "iti" ---
        for thisComponent in iti.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for iti
        iti.tStop = globalClock.getTime(format='float')
        iti.tStopRefresh = tThisFlipGlobal
        thisExp.addData('iti.stopped', iti.tStop)
        # the Routine "iti" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        # mark thisMainLoop as finished
        if hasattr(thisMainLoop, 'status'):
            thisMainLoop.status = FINISHED
        # if awaiting a pause, pause now
        if mainLoop.status == PAUSED:
            thisExp.status = PAUSED
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[globalClock], 
            )
            # once done pausing, restore running status
            mainLoop.status = STARTED
        thisExp.nextEntry()
        
    # completed 1 repeats of 'mainLoop'
    mainLoop.status = FINISHED
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # --- Prepare to start Routine "endScreen" ---
    # create an object to store info about Routine endScreen
    endScreen = data.Routine(
        name='endScreen',
        components=[endText],
    )
    endScreen.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # store start times for endScreen
    endScreen.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    endScreen.tStart = globalClock.getTime(format='float')
    endScreen.status = STARTED
    thisExp.addData('endScreen.started', endScreen.tStart)
    endScreen.maxDuration = None
    # keep track of which components have finished
    endScreenComponents = endScreen.components
    for thisComponent in endScreen.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "endScreen" ---
    thisExp.currentRoutine = endScreen
    endScreen.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *endText* updates
        
        # if endText is starting this frame...
        if endText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            endText.frameNStart = frameN  # exact frame index
            endText.tStart = t  # local t and not account for scr refresh
            endText.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(endText, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'endText.started')
            # update status
            endText.status = STARTED
            endText.setAutoDraw(True)
        
        # if endText is active this frame...
        if endText.status == STARTED:
            # update params
            pass
        
        # if endText is stopping this frame...
        if endText.status == STARTED:
            if frameN >= (endText.frameNStart + endFrames):
                # keep track of stop time/frame for later
                endText.tStop = t  # not accounting for scr refresh
                endText.tStopRefresh = tThisFlipGlobal  # on global time
                endText.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'endText.stopped')
                # update status
                endText.status = FINISHED
                endText.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer, globalClock], 
                currentRoutine=endScreen,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            endScreen.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if endScreen.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in endScreen.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "endScreen" ---
    for thisComponent in endScreen.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for endScreen
    endScreen.tStop = globalClock.getTime(format='float')
    endScreen.tStopRefresh = tThisFlipGlobal
    thisExp.addData('endScreen.stopped', endScreen.tStop)
    thisExp.nextEntry()
    # the Routine "endScreen" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    # Run 'End Experiment' code from a6SessionFrameCode
    # Preserve I1's interval sequence (seconds, comma-separated).
    # The path mirrors the main CSV stem used by thisExp.saveAsWideText().
    win.recordFrameIntervals = False
    win.saveFrameIntervals(fileName=thisExp.dataFileName + '_frameIntervals.log')
    
    # mark experiment as finished
    endExperiment(thisExp, win=win)


def saveData(thisExp):
    """
    Save data from this experiment
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    filename = thisExp.dataFileName
    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsWideText(filename + '.csv', delim='auto')
    thisExp.saveAsPickle(filename)


def endExperiment(thisExp, win=None):
    """
    End this experiment, performing final shut down operations.
    
    This function does NOT close the window or end the Python process - use `quit` for this.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    """
    # stop any playback components
    if thisExp.currentRoutine is not None:
        for comp in thisExp.currentRoutine.getPlaybackComponents():
            comp.stop()
    if win is not None:
        # remove autodraw from all current components
        win.clearAutoDraw()
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed
        win.flip()
    # return console logger level to WARNING
    logging.console.setLevel(logging.WARNING)
    # mark experiment handler as finished
    thisExp.status = FINISHED
    # run any 'at exit' functions
    for fcn in runAtExit:
        fcn()
    logging.flush()


def quit(thisExp, win=None, thisSession=None):
    """
    Fully quit, closing the window and ending the Python process.
    
    Parameters
    ==========
    win : psychopy.visual.Window
        Window to close.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    thisExp.abort()  # or data files will save again on exit
    # make sure everything is closed down
    if win is not None:
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()
        win.close()
    logging.flush()
    if thisSession is not None:
        thisSession.stop()
    # terminate Python process
    core.quit()


# if running this experiment as a script...
if __name__ == '__main__':
    # call all functions in order
    expInfo = showExpInfoDlg(expInfo=expInfo)
    thisExp = setupData(expInfo=expInfo)
    logFile = setupLogging(filename=thisExp.dataFileName)
    win = setupWindow(expInfo=expInfo)
    setupDevices(expInfo=expInfo, thisExp=thisExp, win=win)
    run(
        expInfo=expInfo, 
        thisExp=thisExp, 
        win=win,
        globalClock='float'
    )
    saveData(thisExp=thisExp)
    quit(thisExp=thisExp, win=win)
