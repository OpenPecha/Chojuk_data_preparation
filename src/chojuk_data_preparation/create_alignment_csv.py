from pathlib import Path
import pandas as pd
import csv


def create_alignment_csv(root_path, commentary_path, output_csv_path):
    text = []
    root_text = root_path.read_text(encoding='utf-8').splitlines()
    commentary_text = commentary_path.read_text(encoding="utf-8").splitlines()
    for num in range(len(root_text)):
        if num%2 == 0:
            root = root_text[num]
            commentary = commentary_text[num]
        else:
            continue
        text.append([root, commentary])
    
    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Root', 'Commentary'])  # Writing header
        writer.writerows(text)







if __name__ == "__main__":
    file_name = "Thokme"
    root_path = Path(f"./data/{file_name}-final/ཐུན་མོང་གི་རྩ་བ།.txt")
    commentary_path = Path(f"./data/{file_name}-final/Commentary.txt")
    output_csv_path = Path(f"./data/{file_name}_alignment.csv")
    create_alignment_csv(root_path, commentary_path, output_csv_path)