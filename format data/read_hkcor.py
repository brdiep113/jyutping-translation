import pycantonese
import regex as re

def build_hkcancor_corpus(output_file):
    """
        Returns:
      A tuple of jyutping and cantonese sentence.
    """
    corpus = pycantonese.hkcancor()
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
            # with codecs.open("formatted_data.tsv", 'w', 'utf-8') as fout:
            #     fout.write(u"{}\t{}\t{}\n".format(i, jyutping_list, chi_char))
        except:
            continue  # it's okay as we have a pretty big corpus!

    avg = number_of_character / number_of_sentence
    print(f"{output_file}")
    print(f"Number of sentences: {number_of_sentence}")
    print(f"Number of characters: {number_of_character}")
    print(f"Average number of characters per sentence:{round(avg, 2)}")
    print("------------------------------------------------ \n")
    return number_of_sentence, number_of_character


if __name__ == "__main__":
    build_hkcancor_corpus("hkcancor_data.tsv")

