from pympi import Elan
import os
import regex as re
import csv
import sys
import json
import shutil
from homophones_katrina import homophones

IS_HOMELAND = False


def add_homophones(src_dir, dest_dir, eaf_filename, processed_homophone_dict):
    src_file = os.path.join(src_dir + "/", eaf_filename)
    dest_file = os.path.join(dest_dir + "/", eaf_filename)
    shutil.copy(src_file, dest_file)
    speaker_id = eaf_filename[:6]
    new_eaf_file = os.path.join(dest_dir, speaker_id + "_homophone.eaf")
    os.rename(dest_file, new_eaf_file)
    dst_eaf_file = Elan.Eaf(new_eaf_file)
    directory = ""

    # add homophones to eaf file
    homophone_tier_name = str(speaker_id) + "_homophones"
    dst_eaf_file.add_tier(homophone_tier_name)
    jp_tier = str(speaker_id) + "_jyutping_tokenized"
    jp_annotations = dst_eaf_file.get_annotation_data_for_tier(jp_tier)
    annotations = []
    for i, tup in enumerate(jp_annotations):
        start = int(tup[0])
        end = int(tup[1])
        ch = find_match(str(tup[2]), processed_homophone_dict)
        annotations.append((start, end, ch))
    for annotation in annotations:
        dst_eaf_file.add_annotation(homophone_tier_name, annotation[0], annotation[1],
                                    annotation[2])  # (start_time, end_time, homophone choices(if len > 1))
    dst_eaf_file.to_file(new_eaf_file)


def find_match(jp, processed_homophone_dict):
    """
    given a jyutping, find the list of homophones if number of homophone is greater than 1
    """
    if jp in processed_homophone_dict:
        if len(processed_homophone_dict[jp]) > 1:
            return processed_homophone_dict[jp]
    return ""


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


src_path_k = "/home/jose/jyutping-translation/format data/Homophones(Katrina)/Transcription EAFS + POS & prescribed jyutping (Katrina's files)"

if IS_HOMELAND:
    src_path_eaf = "../auto_transcription_results/auto_transcription_results(homeland jyut+char)"
    des_path = "../homophones/homophones_homeland_jp_ch"
else:
    src_path_eaf = "../auto_transcription_results/auto_transcription_results(jyut+char)"
    des_path = "../homophones/homophones_jp_ch"

if __name__ == '__main__':
    with open("sorted_dict_homophone.json", "r") as file:
        json_string = file.read()
        processed_homophone_dict = json.loads(json_string)

        for path in os.listdir(src_path_eaf):
            # try:
                # path = "C1F50A_IV_anon.eaf"
                eaf_file = os.path.join(src_path_eaf + "/", path)
                if eaf_file and path.endswith(".eaf"):
                    if not os.path.exists(des_path):
                        os.makedirs(des_path)

                    eaf_filename = path
                    add_homophones(src_path_eaf, des_path, eaf_filename, processed_homophone_dict)

            # except Exception:
            #     print(path, "error")
