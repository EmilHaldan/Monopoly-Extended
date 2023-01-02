from pydub import AudioSegment


file_name = "trump_small_potatos"

newAudio = AudioSegment.from_wav("{}.wav".format(file_name))

t1 = 0
t2 =  1150 #Works in milliseconds

newAudio = newAudio[t1:t2]
newAudio.export('{}NEW.wav'.format(file_name), format="wav") #Exports to a wav file in the current path.