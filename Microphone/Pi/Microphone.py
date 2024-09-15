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
    #fileNumber = 0
    #wav_output_filename = 'test1.wav' # name of .wav file
    audio = pyaudio.PyAudio() # create pyaudio instantiation
    stream = 0
    recording = True

    def __init__(resolution = pyaudio.paInt16, no_channels = 1, sample_rate = 44100, chunk = 4096,
    recording_time = 2, device_index = 1, ):
        self.form_1 = resolution
        self.chans = no_channels
        self.samp_rate = samp_rate
        self.chunk = chunk
        self.record_secs = recording_time
        self.dev_index = device_index
        


    def fileName(self):
        fileNumber = time.time()
        fileNumber = str(fileNumber).replace(".","_")
        fileName = 'EchoRecording'+ fileNumber +'.wav'
        return(fileName)

    def saveFile(self,wav_output_filename,frames):
        # save the audio frames as .wav file
        wavefile = wave.open(wav_output_filename,'wb')
        wavefile.setnchannels(self.chans)
        wavefile.setsampwidth(self.audio.get_sample_size(self.form_1))
        wavefile.setframerate(self.samp_rate)
        wavefile.writeframes(b''.join(frames))
        wavefile.close()


    
    def init_stream(self):
        self.stream = self.audio.open(format = self.form_1,rate = self.samp_rate,channels = self.chans, \
                                input_device_index = self.dev_index,input = True, \
                                frames_per_buffer= self.chunk)
    
    def stop_stream(self):

            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()

    def stop_recording(self):
        self.recording = False   
    
    def re_start_recording(self):
        self.recording = True

            
            
    def startRecording(self):
                # create pyaudio stream
        self.init_stream(self)

 
        try:
            while(True):
                if(self.recording):
                    try:
                        self.stream.start_stream()
                        print("recording")
                        frames = []

                        # loop through stream and append audio chunks to frame array
                        for ii in range(0,int((self.samp_rate/self.chunk)*self.record_secs)):
                            data = self.stream.read(self.chunk)
                            frames.append(data)

                        print("finished recording")
                        # stop the stream, close it, and terminate the pyaudio instantiation
                        self.saveFile( self,self.fileName(self),frames)
                        self.stream.stop_stream()
                    except OSError:
                        try:
                       
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