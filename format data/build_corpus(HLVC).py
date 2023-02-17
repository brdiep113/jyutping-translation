from __future__ import print_function
import codecs
import os
import regex as re  # pip install regex
import pycantonese
from pycantonese.word_segmentation import Segmenter

def align(sent):
    '''
    Args:
      sent: A string. A sentence.

    Returns:
      A tuple of jyutping and cantonese sentence.
    '''
    # segmenter = Segmenter(max_word_length=2)
    # pycantonese.segment(sent, cls=segmenter)
    jyutping_string = ""
    for tup in pycantonese.characters_to_jyutping(sent):
        jyutping_string += list(tup)[1]
    # print(jyutping_string)
    jyutping_list = re.split('(?<=[a-z]+\d{1})', jyutping_string)
    print(sent)
    print(jyutping_list)

    chi_char = []
    for char, p in zip(sent.replace(" ", ""), jyutping_list):
        chi_char.extend([char] + ["_"] * (len(p) - 1))

    jyutping_list = "".join(jyutping_list)
    chi_char = "".join(chi_char)

    assert len(jyutping_list) == len(chi_char), "The hanzis and the pinyins must be the same in length."
    return jyutping_list, chi_char


def clean(text):
    if re.search("[A-Za-z0-9]", text) is not None:  # For simplicity, roman alphanumeric characters are removed.
        return ""
    text = re.sub(u"[^ \p{Han}。，！？]", "", text)
    return text


def build_corpus(eaf_filename, src_path, des_path):
    speaker_id = eaf_filename[:6]
    read_path = os.path.join(src_path, "{}_training_char.txt".format(speaker_id))
    write_path = os.path.join(des_path, "{}_training_char.tsv".format(speaker_id))

    with codecs.open(write_path, 'w', 'utf-8') as fout:
        with codecs.open(read_path, 'r', 'utf-8') as fin:
            i = 1
            while 1:
                line = fin.readline()
                if not line: break

                try:
                    idx, sent = line.strip().split("\t")
                    sent = clean(sent)
                    if len(sent) > 0:
                        pnyns, hanzis = align(sent)
                        fout.write(u"{}\t{}\t{}\n".format(idx, pnyns, hanzis))
                except:
                    continue  # it's okay as we have a pretty big corpus!

                if i % 10000 == 0: print(i, )
                i += 1


src_path = "training_characters(txt)"
des_path = "training_characters(tsv)"
if __name__ == '__main__':

    for path in os.listdir(src_path):
        if not os.path.exists(des_path):
            os.makedirs(des_path)
        try:
            if os.path.isfile(os.path.join(src_path + "/", path)) and path.endswith(".txt"):
                build_corpus(path, src_path, des_path)
        except Exception:
            print(path, "error")
