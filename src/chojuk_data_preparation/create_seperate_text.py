from pathlib import Path
import csv


def read_tsv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        data = [row for row in reader]
    return data


def create_seperate_text(text_path, output_tibetan_path, output_english_path):
    texts = read_tsv(text_path)
    num = 1
    tibetan_text = ""
    english_text = ""
    for text in texts:
        Tibetan = text[0]
        English = text[1]
        tibetan_text += f"{str(num)}. " + Tibetan + "\n"
        english_text += f"{str(num)}. " + English + "\n"
        num += 1
    output_tibetan_path.write_text(tibetan_text, encoding='utf-8')
    output_english_path.write_text(english_text, encoding='utf-8')



filename = "chonjuk_trans_align"
create_seperate_text(Path(f"./data/{filename}.tsv"), Path(f"./data/{filename}_tibetan.txt"), Path(f"./data/{filename}_english.txt"))