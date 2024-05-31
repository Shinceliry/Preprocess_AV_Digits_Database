import os
import pandas as pd
from tqdm import tqdm
from moviepy.editor import VideoFileClip

DIR = "./AV-Digits-Database/Phrases" #AV-Digits-DatabaseのPhraseのパス

def cut_video(datadir):
    text_list = ["Excuse_me", "Goodbye", "Hello", "How_are_you", "Nice_to_meet_you", "See_you", "I_am_sorry", "Thank_you", "Have_a_good_time", "You_are_welcome"]
    dirnames = sorted([d for d in os.listdir(datadir) if os.path.isdir(os.path.join(datadir, d))])
    
    for dir in tqdm(dirnames, leave=False):
        ref_datadir = datadir + "/" + dir
        
        filename_left = str(dir[:21])
        
        #csvfile, movie chuusyutu
        for file in os.listdir(ref_datadir):
            if file.endswith('.csv') and len(file.rstrip(".csv")) == 20:
                csv_path = os.path.abspath(os.path.join(ref_datadir, file))
            elif file.endswith('.mp4') and len(file.rstrip(".mp4")) == 24:
                video_path = os.path.abspath(os.path.join(ref_datadir, file))
            else :
                continue
            
        #csvfilenosousa
        csvfile = pd.read_csv(csv_path)
        csvfile = csvfile.drop(csvfile.columns[-2], axis=1)
        csvfile = csvfile.drop(csvfile.columns[-2], axis=1)
        
        for i in range(10):
            csvfile['Utterance'].replace("p"+str(i), text_list[i], inplace=True)
        
        splits = csvfile.to_dict(orient='list')
        
        # print(splits)
        # {'Relative_Start_Time': [0, 23090000, 45320000, 65620000, 83480000, 99900000, 117250000, 135430000, 154500000, 172470000], 'Relative_Stop_Time': [23090000, 45320000, 65620000, 83480000, 99900000, 117250000, 135430000, 154500000, 172470000, 190830000], 'Utterance': ['How are you', 'Nice to meet you', 'Goodbye', 'Thank you', 'See you', 'Excuse me', 'I am sorry', 'You are welcome', 'Hello', 'Have a good time']}
        
        start_times = splits['Relative_Start_Time']
        end_times = splits['Relative_Stop_Time']
        utterances = splits['Utterance']
        
        # print(start_times)
        # print(end_times)
        # print(utterances)
        
        for start_time, end_time, utterance in zip(start_times, end_times, utterances):
            video = VideoFileClip(video_path)
            start_time_float = float(start_time) / 1.0e7
            end_time_float = float(end_time) / 1.0e7
            segment_name = utterance
            
            subclip = video.subclip(start_time_float, end_time_float)
            
            output_filename = f'{filename_left + "_" + segment_name}.mp4'
            output_path = os.path.join(ref_datadir, output_filename)
            
            # save movie
            subclip.write_videofile(output_path, codec='libx264')
            
            subclip.close()
            
            video.close()

cut_video(DIR)