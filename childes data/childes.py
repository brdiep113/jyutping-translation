from __future__ import print_function
import codecs
import os

import regex as re  # pip install regex
import pycantonese


def build_corpus_childes(url, output_file):
    """
        Returns:
      A tuple of jyutping and cantonese sentence.
    """
    # get specific cantonese file from Leo
    if url == "https://childes.talkbank.org/data/Biling/Leo.zip":
        Leo_cantoneseo_only = pycantonese.read_chat(url)
        corpus = Leo_cantoneseo_only.filter("Cantonese")
    # conventional way
    else:
        corpus = pycantonese.read_chat(url)

    tokens_by_utterances = corpus.tokens(by_utterances=True)
    open(output_file, 'w').close()

    number_of_sentence = 0
    number_of_character = 0

    for i in range(len(tokens_by_utterances)):
        word_strings = ""
        jyutping_list = []
        for token in tokens_by_utterances[i]:
            if not token.jyutping is None:
                word_strings += token.word
                # print(token.jyutping)
                # print(token.word)
                if len(token.jyutping) > 1:
                    l = re.split('(?<=[a-z]+\d{1})', token.jyutping)
                    jyutping_list.extend(l)
                else:
                    jyutping_list.append(token.jyutping)
        jyutping_list = [character for character in jyutping_list if character != ""]

        if re.search("[A-Za-z0-9]", word_strings) is not None or len(jyutping_list) != len(word_strings):
            word_strings = ""
            jyutping_list = ""
        # print(jyutping_list)
        # print(word_strings)
        chi_char = []

        for char, p in zip(word_strings.replace(" ", ""), jyutping_list):
            chi_char.extend([char] + ["_"] * (len(p) - 1))

        jyutping_list = "".join(jyutping_list)
        chi_char = "".join(chi_char)
        # print(chi_char)
        if jyutping_list != "":
            number_of_sentence += 1
            number_of_character += len(word_strings)

        assert len(jyutping_list) == len(chi_char)
        try:
            with open(output_file, "a") as fout:
                fout.write(u"{}\t{}\t{}\n".format(i, jyutping_list, chi_char))
        except:
            continue

    avg = number_of_character / number_of_sentence
    print(f"{output_file}")
    print(f"Number of sentences: {number_of_sentence}")
    print(f"Number of characters: {number_of_character}")
    print(f"Average number of characters per sentence:{round(avg, 2)}")
    print("------------------------------------------------ \n")
    return number_of_sentence, number_of_character


if __name__ == "__main__":
    HKU70Corpus = "https://childes.talkbank.org/data/Chinese/Cantonese/HKU.zip"
    LeeWongLeungCorpus = "https://childes.talkbank.org/data/Chinese/Cantonese/LeeWongLeung.zip"
    LeoCorpus = "https://childes.talkbank.org/data/Biling/Leo.zip"
    YipMatthewsBilingualCorpus = "https://childes.talkbank.org/data/Biling/YipMatthews.zip"

    HKU70Corpus_formatted_data = "HKU70Corpus_formatted_data.tsv"
    LeeWongLeungCorpus_formatted_data = "LeeWongLeungCorpus_formatted_data.tsv"
    LeoCorpus_formatted_data = "LeoCorpus_formatted_data.tsv"
    YipMatthewsBilingualCorpus_formatted_data = "YipMatthewsBilingualCorpus_formatted_data.tsv"

    corpus_list = [HKU70Corpus, LeeWongLeungCorpus, LeoCorpus, YipMatthewsBilingualCorpus]
    output_file_list = [HKU70Corpus_formatted_data, LeeWongLeungCorpus_formatted_data, LeoCorpus_formatted_data,
                        YipMatthewsBilingualCorpus_formatted_data]
    total_sentence = 0
    total_char = 0
    for c, f in zip(corpus_list,output_file_list):
        number_of_sentence, number_of_char = build_corpus_childes(c, f)
        total_sentence += number_of_sentence
        total_char += number_of_char

    avg = total_char / total_sentence
    print(f"Total")
    print(f"Number of sentences: {total_sentence}")
    print(f"Number of characters: {total_char}")
    print(f"Average number of characters per sentence:{round(avg, 2)}")
    print("------------------------------------------------ \n")
