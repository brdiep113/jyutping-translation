from pympi import Elan
import os
import regex as re
import csv
import json
tup_dict = {}
"""
Set is_HOMELAND to True for homeland files, False for Heritage files
"""
is_HOMELAND = False


def extract_data(directory, eaf_filename, input_file, processed_with_time_file):
    # get a list of annotations from the speaker_id_character tier of the form: [(start_time, end_time, chi_char, jp_char)]
    eaf_file = Elan.Eaf(directory + "/" + eaf_filename)
    speaker_id = eaf_filename[:6]
    chi_char_tier = speaker_id + "_characters"
    speaker_chi_char = eaf_file.get_annotation_data_for_tier(chi_char_tier)
    # print(speaker_chi_char)
    open(input_file, 'w').close()
    open(processed_with_time_file, 'w').close()
    processed_annotation = []
    # modify the tuples, removing english, punctuations and blanks
    with open(input_file, "a") as txt_file:
        txt_file.write("NUM, PINYIN, EXPECTED" + "\n")
    for i, tup in enumerate(speaker_chi_char):
        jyutping_pattern = r'[a-zA-Z]+[0-9]+'
        temp_lst = re.findall(jyutping_pattern, list(tup)[3])
        jyutping = ''.join(temp_lst)
        chi_char = list(tup)[2]
        # print(tup)
        if jyutping:
            chi_char = re.sub(r"[^ \p{Han}]", "", chi_char).replace(" ", "")
            jyutping = re.sub("[. ， , ( ) \"]", "", jyutping).replace(" ", "")
            jyutping = re.sub(r"^A\d+", "", jyutping)
            new_tup = (tup[0], tup[1], chi_char, jyutping)
            processed_annotation.append(new_tup)
            if jyutping and chi_char:
                #input_file is an input file for the model
                with open(input_file, "a") as txt_file:
                    txt_file.write(str(i+1) + "," + jyutping + "," + chi_char + "\n")
                #processed_with_time_file is for
                with open(processed_with_time_file, "a") as txt_file:
                    txt_file.write(str(tup[0]) + "," + str(tup[1]) + "," + jyutping + "," + chi_char + "\n")
                # print(i, new_tup)

    # print(processed_annotation)
    # tup_dict[str(speaker_id)] = processed_annotation
    # with open("tup_dict.json", "w") as f:
    #     json.dump(tup_dict, f)
    return speaker_id


if is_HOMELAND:
    src_path = "EAF/eaf(homeland jyut+char)"
    des_path_input = "inputs/inputs(homeland jyut+char)/"
    des_path_processed_with_time = "processed/processed(jyut+char)/"
else:
    src_path = "EAF/eaf(jyut+char)"
    des_path_input = "inputs/inputs(jyut+char)/"
    des_path_processed_with_time = "processed/processed(jyut+char)/"


if __name__ == '__main__':
    for path in os.listdir(src_path):
        try:
                # path = "C1F50A_IV_anon.eaf"
            if os.path.isfile(os.path.join(src_path + "/", path)) and path.endswith(".eaf"):
                speaker_id = extract_data(src_path, path, "processed.csv", "processed_with_time.csv")
                if not os.path.exists(des_path_input):
                    os.makedirs(des_path_input)

                output_path_processed = os.path.join(des_path_input, "{}_input.csv".format(speaker_id))
                output_path_processed_with_time = os.path.join(des_path_processed_with_time, "{}_processed.csv".format(speaker_id))
                with open("processed.csv") as input, open(output_path_processed, 'w', newline='') as output: #input file
                    writer = csv.writer(output)
                    for row in csv.reader(input):
                        if any(field.strip() for field in row):
                            writer.writerow(row)
                with open("processed_with_time.csv") as input, open(output_path_processed_with_time, 'w', newline='') as output: #processed file with time
                    writer = csv.writer(output)
                    for row in csv.reader(input):
                        if any(field.strip() for field in row):
                            writer.writerow(row)
        except Exception:
            print(path, "error")

