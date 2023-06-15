from pympi import Elan
import os

def extract_data(directory, eaf_filename, destination):

    eaf_file = Elan.Eaf(directory + "/" + eaf_filename)
    speaker_id = eaf_filename[:6]
    tier = "Main Speaker - Character"
    speaker_chi = eaf_file.get_annotation_data_for_tier(tier)

    for i, annotation in enumerate(speaker_chi):
        chi_char = list(annotation)[2]
        output_path = os.path.join(des_path, "{}_training_char.txt".format(speaker_id))
        with open(output_path, "a") as txt_file:
            txt_file.write(str(i) + "\t" + chi_char + "\n")


src_path = "EAF/eaf(jyut+char)"
des_path = "training_characters(txt)"
if __name__ == '__main__':

    if not os.path.exists(des_path):
        os.makedirs(des_path)

    for path in os.listdir(src_path):
        try:
            if os.path.isfile(os.path.join(src_path + "/", path)) and path.endswith(".eaf(jyut+char)"):
                extract_data(src_path, path, des_path)
        except Exception:
            print(path, "error")
