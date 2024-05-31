import os
from tqdm import tqdm

DIR = "/home/ssd2/sakaya/av_digits_database/normal"
TXT_DIR = "/home/mic/Desktop/sakaya/Wav2Lip/filelists"
train_list = [1,3,5,6,7,10,12,14,15,18,20,22,25,28,31,36,43,45,48,52]
valid_list = [13,16,21,24,35,42,49,53]
test_list = [2,4,8,11,17,29,41,44,46,50,51]
txt_list = ["train", "val", "test"]
original_lists = [train_list, valid_list, test_list]
formatted_lists = []

for list in original_lists:
    formatted_list = [f"{num:03d}" for num in list]
    formatted_lists.append(formatted_list)

def generation_txt(DIR, TXT_DIR):
    filenames = sorted(d for d in os.listdir(DIR))
    txt_files = {name: open(os.path.join(TXT_DIR, f"{name}.txt"), "a") for name in txt_list}

    for file in tqdm(filenames, leave=False):
        for idx, list in enumerate(formatted_lists):
            if any("S" + num in file for num in list):
                # 拡張子を除外したファイル名を取得
                dataname, _ = os.path.splitext(file)
                txt_files[txt_list[idx]].write(dataname + '\n')
                
generation_txt(DIR, TXT_DIR)