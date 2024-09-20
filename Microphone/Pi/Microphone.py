import pyaudio
import wave
import time



class echoMicrophone:
    form_1 = pyaudio.paInt16 # 16-bit resolution
    chans = 1 # 1 channel
    samp_rate = 44100 # 44.1kHz sampling rate
    chunk = 4096 # 2^12 samples for buffer
    record_secs = 5 # seconds to record
    dev_index = 1 # device index found by p.get_device_info_by_index(ii)
    audio = pyaudio.PyAudio() # create pyaudio instantiation
    stream = 0
    recording = True
    frames= []
# set up for the module with the defualt values will provide CD like quality sound reproduction and should geive a good ballance
#beteen fedality and file size
    def __init__(resolution = pyaudio.paInt16, no_channels = 1, sample_rate = 44100, chunk = 4096,
    recording_time = 2, device_index = 1, ):
        self.form_1 = resolution
        self.chans = no_channels
        self.samp_rate = sample_rate
        self.chunk = chunk
        self.record_secs = recording_time
        self.dev_index = device_index
        

# function for setting the flile name currently will take the unix time in scoods since th epoch and append that to the file name
    def fileName(self):
        fileNumber = time.time()
        fileNumber = str(fileNumber).replace(".","_")
        fileName = 'EchoRecording'+ fileNumber +'.wav'
        return(fileName)



# save the audio frames as .wav file
    def saveFile(self,wav_output_filename,frames):
        
        wavefile = wave.open(wav_output_filename,'wb')
        wavefile.setnchannels(self.chans)
        wavefile.setsampwidth(self.audio.get_sample_size(self.form_1))
        wavefile.setframerate(self.samp_rate)
        wavefile.writeframes(b''.join(frames))
        wavefile.close()


    # set up the port audio stream with our sound smapling variables
    def init_stream(self):
        self.stream = self.audio.open(format = self.form_1,rate = self.samp_rate,channels = self.chans, \
                                input_device_index = self.dev_index,input = True, \
                                frames_per_buffer= self.chunk)
    
    def stop_stream(self):

            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()

# call this function to stop recording
    def stop_recording(self):
        self.recording = False   
# call this function to re-start after using the stop recording 
    def re_start_recording(self):
        self.recording = True

# call this to get the raw MIDI data from the portaudio/pyaudio stream could be used to more simply tranfer the data
#and then reassemble using wave or other conversion after transmission
    def get_frames(self):
        return self.frames

            
# call this funtion in your program in order to begin recording          
    def startRecording(self):
                # create pyaudio stream
        self.init_stream(self)

 
        try:
            while(True):
                if(self.recording):
                    try:
                        self.stream.start_stream()
                        print("recording")
                        
                        self.frames= []
                        # loop through stream and append audio chunks to frame array
                        for ii in range(0,int((self.samp_rate/self.chunk)*self.record_secs)):
                            data = self.stream.read(self.chunk)
                            self.frames.append(data)

                        print("finished recording")
                        # stop the stream, close it, and terminate the pyaudio instantiation
                        self.saveFile( self,self.fileName(self),self.frames)
                        self.stream.stop_stream()
                    except OSError:
                        try:
                       
                       # due to buffer on the pi 3 overflowing this will re intiate the portaudio stream and restart recoding 
                            print("OS error caught")
                            self.stop_stream(self)
                            self.audio = pyaudio.PyAudio()
                            self.init_stream(self)
                            self.stream.start_stream()
                        except OSError:
                            self.audio = pyaudio.PyAudio()
                            self.init_stream(self)
                            self.stream.start_stream()


        finally:
            self.stop_stream(self)