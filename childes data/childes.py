from __future__ import print_function
import codecs
import os
import regex as re  # pip install regex
import pycantonese


def show_childes_info(url):
    corpus = pycantonese.read_chat(url)

    # print(corpus.words())
    return corpus.info(verbose=True)


def show_childes_tokens_by_utterances_info(url):
    corpus = pycantonese.read_chat(url)
    tokens_by_utterances = corpus.tokens(by_utterances=True)
    for i in range(10):
        for token in tokens_by_utterances[i]:
            print(f"word: {token.word}")
            print(f"jyutping: {token.jyutping}")
            print()
    return


def build_corpus_childes(url, output_file):
    """
        Returns:
      A tuple of jyutping and cantonese sentence.
    """
    corpus = pycantonese.read_chat(url)
    tokens_by_utterances = corpus.tokens(by_utterances=True)
    open(output_file, 'w').close()
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

        assert len(jyutping_list) == len(chi_char)
        try:
            with open(output_file, "a") as fout:
                fout.write(u"{}\t{}\t{}\n".format(i, jyutping_list, chi_char))
            # with codecs.open("formatted_data.tsv", 'w', 'utf-8') as fout:
            #     fout.write(u"{}\t{}\t{}\n".format(i, jyutping_list, chi_char))
        except:
            continue  # it's okay as we have a pretty big corpus!

    # return jyutping_list, chi_char

def clean(text):
    if re.search("[A-Za-z0-9]", text) is not None:  # For simplicity, roman alphanumeric characters are removed.
        return ""
    text = re.sub(u"[^ \p{Han}。，！？]", "", text)
    return text

if __name__ == "__main__":
    # build_corpus(url);
    # print("Done")
    # print(show_childes_info(url))
    GuthrieBilingualCorpus = "https://childes.talkbank.org/data/Biling/Guthrie.zip"
    HKU70Corpus = "https://childes.talkbank.org/data/Chinese/Cantonese/HKU.zip"
    LeeWongLeungCorpus = "https://childes.talkbank.org/data/Chinese/Cantonese/LeeWongLeung.zip"
    LeoCorpus = "https://childes.talkbank.org/data/Biling/Leo.zip"
    PaidologosCorpusCantonese = "https://phonbank.talkbank.org/data/Chinese/Cantonese/PaidoCantonese.zip"
    YipMatthewsBilingualCorpus = "https://childes.talkbank.org/data/Biling/YipMatthews.zip"

    GuthrieBilingualCorpus_formatted_data = "GuthrieBilingualCorpus_formatted_data.tsv"
    HKU70Corpus_formatted_data = "HKU70Corpus_formatted_data.tsv"
    LeeWongLeungCorpus_formatted_data = "LeeWongLeungCorpus_formatted_data.tsv"
    LeoCorpus_formatted_data = "LeoCorpus_formatted_data.tsv"
    PaidologosCorpusCantonese_formatted_data = "PaidologosCorpusCantonese_formatted_data.tsv"
    YipMatthewsBilingualCorpus_formatted_data = "YipMatthewsBilingualCorpus_formatted_data.tsv"

    corpus_list = [GuthrieBilingualCorpus, HKU70Corpus, LeeWongLeungCorpus, LeoCorpus,
                   PaidologosCorpusCantonese, YipMatthewsBilingualCorpus]
    output_file_list = [GuthrieBilingualCorpus_formatted_data,
                       HKU70Corpus_formatted_data,LeeWongLeungCorpus_formatted_data, LeoCorpus_formatted_data,
                       PaidologosCorpusCantonese_formatted_data,YipMatthewsBilingualCorpus_formatted_data]
    for c, f in zip(corpus_list,output_file_list):
        build_corpus_childes(c, f)
    # build_corpus_childes(HKU70Corpus,HKU70Corpus_formatted_data)
