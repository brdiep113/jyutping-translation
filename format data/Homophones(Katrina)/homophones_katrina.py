from pympi import Elan
import os
import regex as re
import csv
import json


class chineseChar:
    def __init__(self, char):
        self.char = char
        self.count = 1
        self.frequency = 0


def homophones(directory, eaf_filename):
    """
    takes an eaf files and returns a homophone dictionary
    keys: a single jyutping
    values: a list of chinese characters that matches the same jyutping as in the key
    """
    global homophones_dict
    # get annotations from 2 tiers, chinese characters and jyutping
    eaf_file = Elan.Eaf(directory + "/" + eaf_filename)
    speaker_id = eaf_filename[8:14]
    cn_tier = speaker_id + "_sent_cn_all"
    jp_tier = speaker_id + "_sent_all"
    cn = eaf_file.get_annotation_data_for_tier(cn_tier)
    jp = eaf_file.get_annotation_data_for_tier(jp_tier)

    # print(cn)
    jyutping_pattern = r'[a-zA-Z]+[0-9]+'
    for i, (cn_tup, jp_tup) in enumerate(zip(cn, jp)):
        # filter out non chin char
        cn_list = re.sub(r"[^ \p{Han}]", "", cn_tup[2]).replace(" ", "")
        # filter out non jyutping
        jp_list = re.findall(jyutping_pattern, jp_tup[2])

        # number of cn_char and jp_char must be the same

        if len(cn_list) != len(jp_list):
            break
        for i, (cn_char, jp_char) in enumerate(zip(cn_list, jp_list)):
            # create a new list of cn_char if jp_char not in the dictionary
            if jp_char not in homophones_dict:
                c = chineseChar(cn_char)
                c.count = 1
                homophones_dict[jp_char] = [c]

            else:  # append the cn_char if jp_char already exist in the dictionary but not in the cn_char_list
                cn_char_list = homophones_dict[jp_char]

                if isCharInList(cn_char, cn_char_list):  # not homophone
                    index = indexInList(cn_char, cn_char_list)
                    # increment char count by 1
                    cn_char_list[index].count += 1
                else:  # new homophone
                    c = chineseChar(cn_char)
                    c.count = 1
                    cn_char_list.append(c)

    return homophones_dict


def get_total_count(cn_char_list):
    total_count = 0
    for c in cn_char_list:
        total_count += c.count
    return total_count


def isCharInList(cn_char, cn_char_list):
    lst_len = len(cn_char_list)
    i = 0
    while i < lst_len:
        if cn_char == cn_char_list[i].char:
            return True
        i += 1
    return False


def indexInList(cn_char, cn_char_list):
    lst_len = len(cn_char_list)
    i = 0
    while i < lst_len:
        if cn_char == cn_char_list[i].char:
            return i
        i += 1
    return 0


src_path = "/home/jose/jyutping-translation/format data/Homophones(Katrina)/Transcription EAFS + POS & prescribed jyutping (Katrina's files)"

if __name__ == '__main__':
    homophones_dict = {}
    for path in os.listdir(src_path):
        # try:
        # path = "Katrina_C1F50A_IV_anon.eaf"
        if os.path.isfile(os.path.join(src_path + "/", path)) and path.endswith(".eaf"):
            homophones_dict = homophones(src_path, path)
        # print(len(homophones_dict))

    # except Exception:
    #     print(path, "error")

    # sort number of homophones in descending order
    sorted_keys = sorted(homophones_dict.keys())
    # for key in sorted_keys:
    #     print(key, ":", homophones_dict[key])

    sorted_dict = dict(sorted(homophones_dict.items(), key=lambda item: len(item[1]), reverse=True))

    # for add_homophone()
    processed_homophone_dict = {}
    for key, value in sorted_dict.items():
        ch_homophones = ""
        if len(value) > 1:
            for ch in value:
                ch_homophones = ch_homophones + "/" + ch.char
            ch_homophones = ch_homophones[1:]
            processed_homophone_dict[key] = ch_homophones

            print(ch_homophones)
    json_string = json.dumps(processed_homophone_dict)
    with open("sorted_dict_homophone.json", "w") as file:
        file.write(json_string)

    # calculate frequency
    # less_than_10 = 0
    # less_than_20 = 0
    # less_than_30 = 0
    # less_than_40 = 0
    # less_than_50 = 0
    # more_than_50 = 0
    # one_homophone = 0
    # more_than_one_homophone_10 = 0
    # frequency_less_than_75percent_10 = 0
    # more_than_one_homophone_20 = 0
    # frequency_less_than_75percent_20 = 0
    # more_than_one_homophone_30 = 0
    # frequency_less_than_75percent_30 = 0
    # more_than_one_homophone_40 = 0
    # frequency_less_than_75percent_40 = 0
    # more_than_one_homophone_l50 = 0
    # frequency_less_than_75percent_l50 = 0
    # more_than_one_homophone_m50 = 0
    # frequency_more_than_75percent_m50 = 0
    # frequency_more_than_75percent_all = 0
    #
    # for jp_char in homophones_dict.keys():
    #     cn_char_list = homophones_dict[jp_char]
    #     total_count = get_total_count(cn_char_list)
    #     for c in cn_char_list:
    #         c.frequency = c.count / total_count
    #     if total_count <= 10:
    #         if len(sorted_dict[jp_char]) == 1:
    #             one_homophone += 1
    #         else:
    #             more_than_one_homophone_10 += 1
    #             for c in cn_char_list:
    #                 if 0.75 > c.frequency > 0.25:
    #                     frequency_less_than_75percent_10 += 1
    #                     break
    #         less_than_10 += 1
    #     elif total_count <= 20:
    #         if len(sorted_dict[jp_char]) == 1:
    #             one_homophone += 1
    #         else:
    #             more_than_one_homophone_20 += 1
    #             for c in cn_char_list:
    #                 if 0.75 > c.frequency > 0.25:
    #                     frequency_less_than_75percent_20 += 1
    #                     frequency_more_than_75percent_all += 1
    #                     break
    #         less_than_20 += 1
    #     elif total_count <= 30:
    #         if len(sorted_dict[jp_char]) == 1:
    #             one_homophone += 1
    #         else:
    #             more_than_one_homophone_30 += 1
    #             for c in cn_char_list:
    #                 if 0.75 > c.frequency > 0.25:
    #                     frequency_less_than_75percent_30 += 1
    #                     frequency_more_than_75percent_all += 1
    #                     break
    #         less_than_30 += 1
    #     elif total_count <= 40:
    #         if len(sorted_dict[jp_char]) == 1:
    #             one_homophone += 1
    #         else:
    #             more_than_one_homophone_40 += 1
    #             for c in cn_char_list:
    #                 if 0.75 > c.frequency > 0.25:
    #                     frequency_less_than_75percent_40 += 1
    #                     frequency_more_than_75percent_all += 1
    #                     break
    #         less_than_40 += 1
    #     elif total_count <= 50:
    #         if len(sorted_dict[jp_char]) == 1:
    #             one_homophone += 1
    #         else:
    #             more_than_one_homophone_l50 += 1
    #             for c in cn_char_list:
    #                 if 0.75 > c.frequency > 0.25:
    #                     frequency_less_than_75percent_l50 += 1
    #                     frequency_more_than_75percent_all += 1
    #                     break
    #         less_than_50 += 1
    #     else:
    #         if len(sorted_dict[jp_char]) == 1:
    #             one_homophone += 1
    #         else:
    #             more_than_one_homophone_m50 += 1
    #             for c in cn_char_list:
    #                 if 0.75 > c.frequency > 0.25:
    #                     frequency_more_than_75percent_m50 += 1
    #                     frequency_more_than_75percent_all += 1
    #                     break
    #         more_than_50 += 1
    # print("words appeared less than 10 times:", less_than_10)
    # print("words appeared less than 10 times and with more than one homophone:", more_than_one_homophone_10)
    # print("words appeared less than 10 times and with more than one homophone and no frequency greater than 75%:", frequency_less_than_75percent_10)
    # print("words appeared less than 20 times:", less_than_20)
    # print("words appeared less than 20 times and with more than one homophone:", more_than_one_homophone_20)
    # print("words appeared less than 20 times and with more than one homophone and no frequency greater than 75%:", frequency_less_than_75percent_20)
    # print("words appeared less than 30 times:", less_than_30)
    # print("words appeared less than 30 times and with more than one homophone:", more_than_one_homophone_30)
    # print("words appeared less than 30 times and with more than one homophone and no frequency greater than 75%:", frequency_less_than_75percent_30)
    # print("words appeared less than 40 times:", less_than_40)
    # print("words appeared less than 40 times and with more than one homophone:", more_than_one_homophone_40)
    # print("words appeared less than 40 times and with more than one homophone and no frequency greater than 75%:", frequency_less_than_75percent_40)
    # print("words appeared less than 50 times:", less_than_50)
    # print("words appeared less than 50 times and with more than one homophone:", more_than_one_homophone_l50)
    # print("words appeared less than 50 times and with more than one homophone and no frequency greater than 75%:", frequency_less_than_75percent_l50)
    # print("words appeared more than 50 times:", more_than_50)
    # print("words appeared more than 50 times and with more than one homophone:", more_than_one_homophone_m50)
    # print("words appeared more than 50 times and with more than one homophone and no frequency greater than 75%:", frequency_more_than_75percent_m50)
    # print("---------------------------------------------------------------------------------------------------------------------------------------")
    # print("words appeared more than 10 times and frequency more than 75%", frequency_more_than_75percent_all)
    # count homophones frequencies
    count_dict = {}
    for key in homophones_dict:
        value_count = len(homophones_dict[key])
        if value_count not in count_dict:
            count_dict[value_count] = 1
        else:
            count_dict[value_count] += 1

    # print result to homophones(katrina).txt
    with open("homophones_katrina.txt", "w") as f:
        for key, value in sorted_dict.items():
            cn_char_list = [c.char for c in value]
            f.write(f"number of homophones{len(value)}\n{key}: {cn_char_list} \n")
            value.sort(key=lambda x: x.count, reverse=True)
            for c in value:
                freq = round(float(c.frequency * 100), 3)
                f.write(f"char: {c.char} count: {c.count}  frequency : {freq}%\n")
            total_count = get_total_count(value)
            f.write(f"total count:{total_count}\n")
            f.write("\n")
        for count, num_keys in count_dict.items():
            f.write(f"There are {num_keys} jyutping with {count} homophones.\n")
