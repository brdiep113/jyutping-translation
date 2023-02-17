from pympi import Elan
import os
import regex as re
import csv
import sys
import json
import shutil


def add_annotation(directory, eaf_filename):
    dst_file = directory + "/" + eaf_filename
    eaf_file = Elan.Eaf(dst_file)
    speaker_id = eaf_filename[:6]
    with open("tup_dict.json", "r") as f:
        tup_dict = json.load(f)
    tup_lst = tup_dict.get(str(speaker_id))
    print(tup_lst)
    for path in os.listdir("csv"):
        csv_file = speaker_id + "_output.csv"
        if path == csv_file:
            with open("./csv/" + path, "r") as f:
                reader = csv.reader(f)
                for i, row in enumerate(reader):
                    if len(row) > 1 and i >= 1:
                        char_transcription = row[2]
                        tup_lst[i-1][2] = char_transcription

    print(tup_lst)

    tier_name = str(speaker_id) + "_" + "character"
    eaf_file.add_tier(tier_name)
    for annotation in tup_lst:
        eaf_file.add_annotation(tier_name, annotation[0], annotation[1], annotation[2])
    eaf_file.to_file(dst_file)


def new_tier(file, tup_lst):
    with open(file, "r") as f:
        csv_reader = csv.reader(f)
        new_tup_lst = []
        for i, line in enumerate(csv_reader):
            transcription = line[1]
            tup = tup_lst[i]
            new_tup = (tup[0], tup[1], transcription)
            new_tup_lst.append(new_tup)
    return new_tup_lst


def get_speaker_id(filepath):
    filename = os.path.basename(filepath)
    speaker_id = filename[:6]
    return speaker_id


def get_eaf_file(speaker_id):
    for path in os.listdir("eaf"):
        filename = os.path.basename(path)
        if filename[:6] == speaker_id:
            return path
    return "file not found"


src_path_csv = "csv"
src_path_eaf = "eaf"
des_path = "auto_transcription_results"
if __name__ == '__main__':

    for path in os.listdir(src_path_eaf):
        # try:
            if os.path.isfile(os.path.join(src_path_eaf + "/", path)) and path.endswith(".eaf"):
                if not os.path.exists(des_path):
                    os.makedirs(des_path)
                shutil.copy(os.path.join(src_path_eaf + "/", path), os.path.join(des_path + "/", path))
                speaker_id = get_speaker_id(os.path.join(src_path_csv + "/", path))
                eaf_file = get_eaf_file(speaker_id)
                add_annotation(des_path, eaf_file)

        # except Exception:
        #     print(path, "error")
