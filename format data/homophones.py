from pympi import Elan
import os
import regex as re
import csv


def homophones(directory, eaf_filename, homophones_dict):
    eaf_file = Elan.Eaf(directory + "/" + eaf_filename)
    speaker_id = eaf_filename[:6]
    jyutping_tier = speaker_id + "_jyutping"
    chi_char_tier = speaker_id + "_characters"
    speaker_chi_char = eaf_file.get_annotation_data_for_tier(chi_char_tier)
    # print(speaker_chi_char)
    tup_lst = []
    for i, tup in enumerate(speaker_chi_char):
        jyutping_pattern = r'[a-zA-Z]+[0-9]+'
        if len(tup) == 4:
            temp_lst = re.findall(jyutping_pattern, list(tup)[3])
            jyutping_anotation = ''.join(temp_lst)
            chi_char = list(tup)[2]
            if jyutping_anotation:
                chi_char = re.sub(r"[^ \p{Han}]", "", chi_char).replace(" ", "")
                jyutping_anotation = re.sub("[. ， , ( ) \"]", "", jyutping_anotation).replace(" ", "")
                jyutping_anotation = re.sub(r"^A\d+", "", jyutping_anotation)
                # change all to lowercase
                jyutping_anotation = re.sub(r'[A-Z]', lambda x: x.group(0).lower(), jyutping_anotation)
                #  find all the numbers in the string and replace them with the number followed by a comma
                jyutping_anotation = re.sub(r'(\d+)', r'\1,', jyutping_anotation)
                # Remove the extra comma at the end of the string
                jyutping_anotation = jyutping_anotation.rstrip(',')
                chi_char = re.findall(r'[\u4e00-\u9fff]', chi_char)  # Match all Chinese characters
                chi_char = ','.join(chi_char)  # Join the matched characters with comma separator
                char_substrings = chi_char.split(',')
                jyutping_substrings = jyutping_anotation.split(',')
                for j, char in enumerate(char_substrings):
                    if len(jyutping_substrings) == len(char_substrings):
                        if jyutping_substrings[j] not in homophones_dict:
                            homophones_dict[jyutping_substrings[j]] = [char]
                        else:
                            char_lst = homophones_dict[jyutping_substrings[j]]
                            if char not in char_lst:
                                char_lst.append(char)
                            homophones_dict[jyutping_substrings[j]] = char_lst
                new_tup = (chi_char, jyutping_anotation)
                tup_lst.append(new_tup)


    # print((tup_lst))
    return homophones_dict
src_path = "EAF/eaf(jyut+char)"

if __name__ == '__main__':
    homophones_dict = {}
    for path in os.listdir(src_path):
        try:
            if os.path.isfile(os.path.join(src_path + "/", path)) and path.endswith(".eaf"):
                homophones_dict = homophones(src_path, path, homophones_dict)
                # if not os.path.exists(des_path):
                #     os.makedirs(des_path)

        except Exception:
            print(path, "error")
    # print(homophones_dict)
    sorted_keys = sorted(homophones_dict.keys())
    for key in sorted_keys:
        print(key, ":", homophones_dict[key])

