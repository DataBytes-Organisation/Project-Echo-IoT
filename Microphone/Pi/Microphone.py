import pyaudio
import wave
import time
import threading
from gpiozero import Button

form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 4096 # 2^12 samples for buffer
record_secs = 5 # seconds to record
dev_index = 1 # device index found by p.get_device_info_by_index(ii)
fileNumber = 0
wav_output_filename = 'test1.wav' # name of .wav file
audio = pyaudio.PyAudio() # create pyaudio instantiation
recording = False

def fileName():
    fileNumber = time.time()
    fileNumber = str(fileNumber).replace(".","_")
    fileName = 'EchoRecording'+ fileNumber +'.wav'
    return(fileName)

def saveFile():
    # save the audio frames as .wav file
    wavefile = wave.open(wav_output_filename,'wb')
    wavefile.setnchannels(chans)
    wavefile.setsampwidth(audio.get_sample_size(form_1))
    wavefile.setframerate(samp_rate)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()

def recordingEnableButton():
    button = Button(2)
    global recording
    while(True):
        button.wait_for_press()
        time.sleep(0.5)
        if(recording):
            recording = False
        else:
            recording = True
        print(recording)

        
        




    # create pyaudio stream
stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                        input_device_index = dev_index,input = True, \
                        frames_per_buffer=chunk)

t1 = threading.Thread(target =recordingEnableButton)
t1.start()
try:
    while(True):
        if(recording):
            try:
                stream.start_stream()
                print("recording")
                frames = []

                # loop through stream and append audio chunks to frame array
                for ii in range(0,int((samp_rate/chunk)*record_secs)):
                    data = stream.read(chunk)
                    frames.append(data)

                print("finished recording")

                wav_output_filename = fileName()
                # stop the stream, close it, and terminate the pyaudio instantiation
                saveFile()
                stream.stop_stream()
            except OSError:
                print("OS error caught")
                stream.close()
                audio.terminate()
                audio = pyaudio.PyAudio()
                stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                                input_device_index = dev_index,input = True, \
                                frames_per_buffer=chunk)
finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
    t1.join()