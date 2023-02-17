from pympi import Elan
import os
import regex as re
import csv
import json
tup_dict = {}


def extract_data(directory, eaf_filename, destination, txt_filename):
    """
    :param directory:
    :param eaf_filename:
    :param destination:
    """
    eaf_file = Elan.Eaf(directory + "/" + eaf_filename)
    speaker_id = eaf_filename[:6]
    jyutping_tier = "Main Speaker"
    chi_char_tier = "Main Speaker - Character"
    # speaker_jyutping = eaf_file.get_annotation_data_for_tier(jyutping_tier)
    speaker_chi_char = eaf_file.get_annotation_data_for_tier(chi_char_tier)
    open(txt_filename, 'w').close()
    tup_lst = []
    # modify the tuples, removing english, punctuations and blanks
    with open(txt_filename, "a") as txt_file:
        txt_file.write("NUM, PINYIN, EXPECTED" + "\n")
    for i, tup in enumerate(speaker_chi_char):
        jyutping_pattern = r'[a-zA-Z]+[0-9]+'
        temp_lst = re.findall(jyutping_pattern, list(tup)[3])
        jyutping = ''.join(temp_lst)
        chi_char = list(tup)[2]
        if jyutping:
            chi_char = re.sub(r"[^ \p{Han}]", "", chi_char).replace(" ", "")
            jyutping = re.sub("[. ， , ( ) \"]", "", jyutping).replace(" ", "")
            new_tup = (tup[0], tup[1], chi_char, jyutping)
            tup_lst.append(new_tup)
            with open(txt_filename, "a") as txt_file:
                txt_file.write(str(i+1) + "," + jyutping + "," + chi_char + "\n")
            print(i, new_tup)
    tup_dict[str(speaker_id)] = tup_lst
    with open("tup_dict.json", "w") as f:
        json.dump(tup_dict, f)
    return speaker_id



src_path = "eaf"
des_path = "inputs"
if __name__ == '__main__':

    for path in os.listdir(src_path):
        try:
            if os.path.isfile(os.path.join(src_path + "/", path)) and path.endswith(".eaf"):
                speaker_id = extract_data(src_path, path, des_path, "temp_file.csv")
                if not os.path.exists(des_path):
                    os.makedirs(des_path)
                output_path = os.path.join(des_path, "{}_input.csv".format(speaker_id))
                with open("temp_file.csv") as input, open(output_path, 'w', newline='') as output:
                    writer = csv.writer(output)
                    for row in csv.reader(input):
                        if any(field.strip() for field in row):
                            writer.writerow(row)
                print(tup_dict)
        except Exception:
            print(path, "error")

