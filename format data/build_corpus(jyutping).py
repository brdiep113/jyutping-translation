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
      A tuple of pinyin and chinese sentence.
    '''
    # segmenter = Segmenter(max_word_length=2)
    # pycantonese.segment(sent, cls=segmenter)
    jyutping_string = ""
    for tup in pycantonese.characters_to_jyutping(sent):
        jyutping_string += list(tup)[1]
    # print(jyutping_string)
    jyutping_list = re.split('(?<=[a-z]+\d{1})', jyutping_string)
    # print(jyutping_list)

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


def build_corpus():
    with codecs.open("formatted_data.tsv", 'w', 'utf-8') as fout:
        with codecs.open("chi_char.txt", 'r', 'utf-8') as fin:
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


if __name__ == "__main__":
    build_corpus();
    print("Done")
    # print(align("哎呀咁都問嘅"))
