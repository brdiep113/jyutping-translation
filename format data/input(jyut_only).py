from pympi import Elan
import os
import regex as re
import csv
import json
tup_dict = {}


def extract_data(directory, eaf_filename, destination, txt_filename):

    eaf_file = Elan.Eaf(directory + "/" + eaf_filename)
    speaker_id = eaf_filename[:6]
    jyutping_tier = speaker_id + "_jyutping"
    speaker_jyutping = eaf_file.get_annotation_data_for_tier(jyutping_tier)
    open(txt_filename, 'w').close()
    tup_lst = []
    # modify the tuples, removing english, punctuations and blanks
    with open(txt_filename, "a") as txt_file:
        txt_file.write("NUM, PINYIN, EXPECTED" + "\n")
    for i, tup in enumerate(speaker_jyutping):
        jyutping_pattern = r'[a-zA-Z]+[0-9]+'
        temp_lst = re.findall(jyutping_pattern, list(tup)[2])
        jyutping = ''.join(temp_lst)
        if jyutping:
            jyutping = re.sub("[. ， , ( ) \"]", "", jyutping).replace(" ", "")
            jyutping = re.sub(r"^A\d+", "", jyutping)
            new_tup = (tup[0], tup[1], jyutping)
            tup_lst.append(new_tup)
            with open(txt_filename, "a") as txt_file:
                txt_file.write(str(i+1) + "," + jyutping + "\n")
                # print(i, new_tup)
    tup_dict[str(speaker_id)] = tup_lst
    with open("tup_dict.json", "w") as f:
        json.dump(tup_dict, f)
    return speaker_id



# src_path = "eaf(jyut_only)"
# des_path = "inputs(jyut_only)"

src_path = "EAF/eaf(homeland jyut_only)"
des_path = "inputs/inputs(homeland jyut_only)"
if __name__ == '__main__':

    for path in os.listdir(src_path):
        # try:
            # path = "C1F54B_IV_anon.eaf(jyut+char)"
            if os.path.isfile(os.path.join(src_path + "/", path)) and path.endswith(".eaf"):
                speaker_id = extract_data(src_path, path, des_path, "processed.csv")
                if not os.path.exists(des_path):
                    os.makedirs(des_path)
                output_path = os.path.join(des_path, "{}_input.csv".format(speaker_id))
                with open("processed.csv") as input, open(output_path, 'w', newline='') as output:
                    writer = csv.writer(output)
                    for row in csv.reader(input):
                        if any(field.strip() for field in row):
                            writer.writerow(row)
                # print(tup_dict)
        # except Exception:
        #     print(path, "error")
