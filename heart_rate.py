
#Add Phidgets Library
from Phidget22.Phidget import *
from Phidget22.Devices.VoltageRatioInput import *
import heartpy as hp
#Required for sleep statement
import time
import collections

raw_data = []
collect_samples = False
num_samples = 0
def onVoltageRatioChange(self, voltageRatio):
    if(collect_samples):
        raw_data.append(voltageRatio)

def processSamples():
    try:
        filtered_data = hp.filter_signal(raw_data, cutoff = 5, sample_rate = 100.0, order = 3, filtertype='lowpass')
        scaled_data = hp.scale_data(filtered_data)
        working_data, measures = hp.process(scaled_data, 100.0, )

        print("\nHEART RATE: " + str(measures['bpm']) + " BPM\n") #returns BPM value
    except:
        print("\nUnable to determine heart rate. Try adjusting pulse sensor!\n")
        raw_data.clear()
        collectSamples()
    
def collectSamples():
    global collect_samples
    timer = 3
    collect_samples = True
    while(timer > 0):
        print("Collecting Samples " + str(timer))
        timer -= 1
        time.sleep(1)
    collect_samples = False
    processSamples()
#Create
pulse = VoltageRatioInput()

#Address
pulse.setHubPort(0)
pulse.setIsHubPortDevice(True)

#Register for Data Events
pulse.setOnVoltageRatioChangeHandler(onVoltageRatioChange)

#Open
pulse.openWaitForAttachment(1000)

#Set Data Interval
pulse.setDataInterval(10) #Set data interval to 10ms (100Hz sample rate)


collectSamples()
while(True):
    time.sleep(1)


  