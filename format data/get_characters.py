from pympi import Elan
import os

def extract_data(directory, eaf_filename, destination, txt_filename):
    """
    :param directory:
    :param eaf_filename:
    :param destination:
    """
    eaf_file = Elan.Eaf(directory + "/" + eaf_filename)
    speaker_id = eaf_filename[:6]
    tier = "Main Speaker - CHI"
    speaker_chi = eaf_file.get_annotation_data_for_tier(tier)

    for i, annotation in enumerate(speaker_chi):
        chi_char = list(annotation)[2]
        with open(txt_filename, "a") as txt_file:
            txt_file.write(str(i) + "\t" + chi_char + "\n")
        print(chi_char)


src_path = "eaf"
des_path = "eaf_result"
if __name__ == '__main__':

    for path in os.listdir(src_path):
        try:
            if os.path.isfile(os.path.join(src_path + "/", path)):
                extract_data(src_path, path, des_path, "chi_char.txt")
        except Exception:
            print(path, "error")
