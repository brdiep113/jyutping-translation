from pympi import Elan
import os
import regex as re
import csv
import sys
import json
import shutil

IS_HOMELAND = False


def add_annotation(dest_dir, eaf_filename):
    dst_file = dest_dir + "/" + eaf_filename
    eaf_file = Elan.Eaf(dst_file)
    speaker_id = eaf_filename[:6]
    directory = ""

    if IS_HOMELAND:
        csv_directory = "CSV/csv(homeland jyut+char)/"
        processed_directory = "processed/processed(homeland jyut+char)/"
    else:
        csv_directory = "CSV/csv(jyut+char)/"
        processed_directory = "processed/processed(jyut+char)/"

    for path in os.listdir(csv_directory):
        csv_file = speaker_id + "_output.csv"
        if path == csv_file:
            with open(csv_directory + path, "r") as cf:  # get row count of model output file
                reader = csv.reader(cf)
                row_count = sum(1 for _ in reader)
            processed_filename = speaker_id + "_processed.csv"
            with open(processed_directory + processed_filename, "r") as pf:
                reader = csv.reader(pf)
                annotations = []
                for row in reader:
                    annotation = [int(row[0]), int(row[1]), ""]
                    annotations.append(annotation)
            with open(csv_directory + path, "r") as f:  # open model output file
                reader = csv.reader(f)
                for i, row in enumerate(reader):
                    if 1 <= i < row_count - 1 and i <= len(annotations):
                        char_transcription = row[2]  # get transcription of the model
                        annotations[i - 1][2] = char_transcription
    # add annotations to eaf file
    tier_name = str(speaker_id) + "_auto_characters"
    eaf_file.add_tier(tier_name)
    for annotation in annotations:
        eaf_file.add_annotation(tier_name, annotation[0], annotation[1],
                                annotation[2])  # (start_time, end_time, char_transcription)
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
    if IS_HOMELAND:
        directory = "EAF/eaf(homeland jyut+char)"
    else:
        directory = "EAF/eaf(jyut+char)"
    for path in os.listdir(directory):
        filename = os.path.basename(path)
        if filename[:6] == speaker_id and filename.endswith(".eaf"):
            return path
    return "file not found"


if IS_HOMELAND:
    src_path_csv = "CSV/csv(homeland jyut+char)"
    src_path_eaf = "EAF/eaf(homeland jyut+char)"
    des_path = "auto_transcription_results/auto_transcription_results(homeland jyut+char)"
else:
    src_path_csv = "CSV/csv(jyut+char)"
    src_path_eaf = "EAF/eaf(jyut+char)"
    des_path = "auto_transcription_results/auto_transcription_results(jyut+char)"

if __name__ == '__main__':
    for path in os.listdir(src_path_eaf):
        try:
            # path = "C1F50A_IV_anon.eaf"
            if os.path.isfile(os.path.join(src_path_eaf + "/", path)) and path.endswith(".eaf"):
                if not os.path.exists(des_path):
                    os.makedirs(des_path)
                shutil.copy(os.path.join(src_path_eaf + "/", path), os.path.join(des_path + "/", path))
                speaker_id = get_speaker_id(os.path.join(src_path_csv + "/", path))
                eaf_file = get_eaf_file(speaker_id)
                add_annotation(des_path, eaf_file)

        except Exception:
            print(path, "error")
