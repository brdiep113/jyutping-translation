import pycantonese


def build_hkcancor_corpus(output_file):
    """
        Returns:
      A tuple of jyutping and cantonese sentence.
    """
    corpus = pycantonese.hkcancor()
    tokens_by_utterances = corpus.tokens(by_utterances=True)
    open(output_file, 'w').close()
    for i in range(len(tokens_by_utterances)):
        word_strings = ""
        jyutping_list = []
        for token in tokens_by_utterances[i]:
            if not token.jyutping is None:
                word_strings += token.word
                jyutping_list.append(token.jyutping)

        chi_char = []
        for char, p in zip(word_strings.replace(" ", ""), jyutping_list):
            chi_char.extend([char] + ["_"] * (len(p) - 1)
                            )
        jyutping_list = "".join(jyutping_list)
        chi_char = "".join(chi_char)

        # print(jyutping_list)
        # print(chi_char)

        assert len(jyutping_list) == len(chi_char)
        try:
            with open(output_file, "a") as fout:
                fout.write(u"{}\t{}\t{}\n".format(i, jyutping_list, chi_char))
            # with codecs.open("formatted_data.tsv", 'w', 'utf-8') as fout:
            #     fout.write(u"{}\t{}\t{}\n".format(i, jyutping_list, chi_char))
        except:
            continue  # it's okay as we have a pretty big corpus! TO DO: maybe keep track of which sentneces fail to write? at least a count

    # return jyutping_list, chi_char

if __name__ == "__main__":
    build_hkcancor_corpus("hkcancor_data.tsv")

