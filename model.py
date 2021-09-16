import numpy as np
import json
import requests
import soundfile as sf
from pydub import AudioSegment
import fleep
import glob
import math
import os
from scipy import signal

MODEL_URI='http://localhost:8501/v1/models/test:predict'
reverse = True
framelength = 300
Tx = 6860
Ty = 846
nFreq = 46

def get_prediction(file_dir):
    X = loadAudioFiles(file_dir, framelength, Tx, nFreq, reverse)    
    y_pred = np.zeros([X.shape[0], Ty, 1])
    for i in range(X.shape[0]):
        X_pred = np.zeros([1, X.shape[1], X.shape[2]])
        X_pred[0,] = X[i]
        data = json.dumps({ 'instances': X_pred.tolist() })
        response = requests.post(MODEL_URI, data=data)
        y_pred[i] = np.array(json.loads(response.text)['predictions'])
    prediction = postProcessModel(y_pred, framelength, Ty, reverse)
    return prediction

# get audio file(s) spectrogram and normalize generated data    
def loadAudioFiles(inputdir, framelength, Tx, nFreq, reverse):
    files = glob.glob(inputdir+'/*')
    files.sort()
    rate = 0
    recData = np.array([])
    for file in files : 
        # get file format 
        with open(file, "rb") as f:
            info = fleep.get(f.read(128))
        format = info.extension[0]
        sound = AudioSegment.from_file(file, format=format)
        sound = sound.set_channels(1)
        # set frame rate to 48000 and convert to wav
        if sound.frame_rate != 48000 :
            sound = sound.set_frame_rate(48000)
        recData = sound.get_array_of_samples()
        rate = sound.frame_rate
    step = framelength
    length = framelength   
    log = ""    
    if len(recData) < rate*framelength :
        log = 'Error !! Sound clip length should be more than '+str(framelength)+ ' secs.'
        return [], rate, log  
    
    maxData = max(recData)
    X = np.zeros([int(len(recData)/(rate*step)), Tx, nFreq]) 
    for i in range(int(len(recData)/(rate*step))):    
        dataSeg = recData[i*(rate*step):i*(rate*step)+rate*length]
        dataSeg = np.multiply(dataSeg, 1/maxData)
        f, t, Sxx = signal.spectrogram(dataSeg, rate, window=('hamming'),nperseg=600 )      
        Sxx = Sxx.T                                                             
        SxxFinal = np.log(abs(Sxx)) 
        if reverse:
            X[int(len(recData)/(rate*step))-i-1] = SxxFinal[::-1].astype('float32')  
        else:
            X[i] = SxxFinal.astype('float32')        
    normData = X[0]
    for i in range(1,X.shape[0]):
        normData = np.concatenate((normData, X[i]))
    mean = np.zeros(normData.shape[1])
    std = np.zeros(normData.shape[1])
    for i in range(normData.shape[1]):
      mean[i] = np.mean(normData[:,i])  
      std[i] = np.std(normData[:,i]) 
      if std[i] == 0.0:
        std[i] = 1 
    X = (X-mean)/std
             
    return X 

def postProcessModel(y_pred, framelength, Ty, reverse):
    y_pred = 1*(y_pred > 0.5)
    y_pred = y_pred.flatten()
    if reverse :
        y_pred = y_pred[::-1]
    # code that processes y_pred and returns a string result
    result = ''
    return result 