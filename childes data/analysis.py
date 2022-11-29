import pycantonese
import regex as re

def build_corpus_childes(url, output_file):
    """
        Returns:
      A tuple of jyutping and cantonese sentence.
    """
    corpus = pycantonese.read_chat(url)
    tokens_by_utterances = corpus.tokens(by_utterances=True)[:20]
    open(output_file, 'w').close()
    sentence_with_same_len = 0
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
            sentence_with_same_len += 1

        assert len(jyutping_list) == len(chi_char)
        try:
            with open(output_file, "a") as fout:
                fout.write(u"{}\t{}\t{}\n".format(i, jyutping_list, chi_char))
            # with codecs.open("formatted_data.tsv", 'w', 'utf-8') as fout:
            #     fout.write(u"{}\t{}\t{}\n".format(i, jyutping_list, chi_char))
        except:
            continue  # it's okay as we have a pretty big corpus!
    print(sentence_with_same_len)
    # return jyutping_list, chi_char
    #     pattern = re.compile(r"[a-z]+[0-9]{1}", re.IGNORECASE)
    #     jyutping_len = len(re.findall(pattern, jyutping_list))
    #
    #     if jyutping_len != len(word_strings):
    #         print(i)
    #         print(jyutping_list)
    #         print(jyutping_len)
    #         print(chi_char)
    #         print(word_strings)


def clean(text):
    if re.search("[A-Za-z0-9]", text) is not None:  # For simplicity, roman alphanumeric characters are removed.
        return ""
    text = re.sub(u"[^ \p{Han}。，！？]", "", text)
    return text


if __name__ == "__main__":
    LeoCorpus = "https://childes.talkbank.org/data/Biling/Leo.zip"
    LeoCorpus_formatted_data = "TestCorpus.tsv"
    build_corpus_childes(LeoCorpus, LeoCorpus_formatted_data)

