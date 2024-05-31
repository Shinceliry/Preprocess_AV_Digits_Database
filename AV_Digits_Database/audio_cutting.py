import os
import pandas as pd
from tqdm import tqdm
from pydub import AudioSegment

DIR = "./AV-Digits-Database/Phrases" #AV-Digits-DatabaseのPhraseのパス

def cut_normal_audio(datadir):
    text_list = ["Excuse_me", "Goodbye", "Hello", "How_are_you", "Nice_to_meet_you", "See_you", "I_am_sorry", "Thank_you", "Have_a_good_time", "You_are_welcome"]
    dirnames = sorted([d for d in os.listdir(datadir) if os.path.isdir(os.path.join(datadir, d))])
    
    for dir in tqdm(dirnames, leave=False):
        ref_datadir = datadir + "/" + dir
        
        ref_datadir_name = os.path.splitext(ref_datadir)[0]
        if not 'C01' in ref_datadir_name:
            continue
        
        filename_left = str(dir[:21])
        
        #csvfile, audio chuusyutu
        for file in os.listdir(ref_datadir):
            if file.endswith('.csv') and len(file.rstrip(".csv")) == 20:
                csv_path = os.path.abspath(os.path.join(ref_datadir, file))
            elif file.endswith('.wav') and len(file.rstrip(".wav")) == 24:
                audio_path = os.path.abspath(os.path.join(ref_datadir, file))
            else :
                continue
            
        #csvfilenosousa
        csvfile = pd.read_csv(csv_path)
        csvfile = csvfile.drop(csvfile.columns[-2], axis=1)
        csvfile = csvfile.drop(csvfile.columns[-2], axis=1)
        
        for i in range(10):
            csvfile['Utterance'].replace("p"+str(i), text_list[i], inplace=True)
        
        splits = csvfile.to_dict(orient='list')
        
        start_times = splits['Relative_Start_Time']
        end_times = splits['Relative_Stop_Time']
        utterances = splits['Utterance']
        
        for start_time, end_time, utterance in zip(start_times, end_times, utterances):
            audiofile = AudioSegment.from_wav(audio_path)
            start_time_float = float(start_time) / 1.0e7 * 1000. #mirissec
            end_time_float = float(end_time) / 1.0e7 * 1000. #mirisec
            segment_name = utterance
            
            subclipaudio = audiofile[start_time_float : end_time_float]
            
            output_filename = f'{filename_left + "_" + segment_name}.wav'
            output_path = os.path.join(ref_datadir, output_filename)
            
            # save movie
            subclipaudio.export(output_path, format='wav')

cut_normal_audio(DIR)