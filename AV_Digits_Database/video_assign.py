import os
import shutil
from tqdm import tqdm

DIR = "./AV-Digits-Database/Phrases" #AV-Digits-DatabaseのPhraseのパス
target_directory1 = "./normal" #有声発話に分類されたデータの格納先パス
target_directory2 = "./silent" #無声発話に分類されたデータの格納先パス

def assign_dataset(datadir):
    dirnames = sorted([d for d in os.listdir(datadir) if os.path.isdir(os.path.join(datadir, d))])
    for dir in tqdm(dirnames, leave=False):
        ref_datadir = datadir + "/" + dir
        for filename in os.listdir(ref_datadir):
            # Check if the file is a .mp4 file
            if filename.endswith('.mp4'):
                # Remove the extension and check the length of the filename
                name_without_extension = os.path.splitext(filename)[0]
                if len(name_without_extension) >= 25:
                    # Check if the file contains ‘C01’ or ‘C03’ in its name
                    if 'C01' in name_without_extension:
                        # Copy to directory 1
                        shutil.copy(os.path.join(ref_datadir, filename),
                                    os.path.join(target_directory1, filename))
                    elif 'C03' in name_without_extension:
                        # Copy to directory 2
                        shutil.copy(os.path.join(ref_datadir, filename),
                                    os.path.join(target_directory2, filename))
                    else:
                        continue
                else:
                    continue
            else:
                continue
            

assign_dataset(DIR)