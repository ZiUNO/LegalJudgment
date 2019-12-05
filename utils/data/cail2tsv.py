import json
import os
import pathlib
import re


def cail2tsv_multi(source, target):
    def json2tsv(json_file_path, tsv_file_path):
        print("MAKE %s TO %s" % (json_file_path, tsv_file_path))
        with open(json_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        tsv_data = [["fact",
                     "relevant_articles",
                     "accusation",
                     "punish_of_money",
                     "criminals",
                     "death_penalty",
                     "imprisonment",
                     "life_imprisonment"]]
        for line in lines:
            line = json.loads(line)
            accusation = line["meta"]["accusation"]
            accusation = [re.sub(u"[\[\]]", "", i) for i in accusation]
            line = [str(line["fact"]),
                    str(line["meta"]["relevant_articles"]),
                    str(accusation),
                    str(line["meta"]["punish_of_money"]),
                    str(line["meta"]["criminals"]),
                    str(line["meta"]["term_of_imprisonment"]["death_penalty"]),
                    str(line["meta"]["term_of_imprisonment"]["imprisonment"]),
                    str(line["meta"]["term_of_imprisonment"]["life_imprisonment"])]
            tsv_data.append(line)
        tsv_data = ["\t".join(line) + "\n" for line in tsv_data]
        tsv_data[-1] = tsv_data[-1].strip()
        with open(tsv_file_path, 'w', encoding="utf-8", newline="\n") as f:
            f.writelines(tsv_data)

    def dir2dir(source_dir_path, target_dir_path):
        if not pathlib.Path(target_dir_path).exists():
            os.makedirs(target_dir_path)
        for file_or_dir in os.listdir(source_dir_path):
            source_path = os.path.join(source_dir_path, file_or_dir)
            target_path = os.path.join(target_dir_path, file_or_dir)
            if pathlib.Path(source_path).is_dir():
                dir2dir(source_path, target_path)
            elif source_path.endswith(".json"):
                target_path = "%s.tsv" % target_path.split(".")[0]
                json2tsv(source_path, target_path)

    dir2dir(source, target)


def cail2tsv(source, target):
    def json2tsv(json_file_path, tsv_file_path):
        print("MAKE %s TO %s" % (json_file_path, tsv_file_path))
        with open(json_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        tsv_data = [["fact",
                     "relevant_articles",
                     "accusation",
                     "punish_of_money",
                     "criminals",
                     "death_penalty",
                     "imprisonment",
                     "life_imprisonment"]]
        for line in lines:
            line = json.loads(line)
            line = [str(line["fact"]),
                    str(line["meta"]["relevant_articles"][0]),
                    str(re.sub(u"[\[\]]", "", line["meta"]["accusation"][0])),
                    str(line["meta"]["punish_of_money"]),
                    str(line["meta"]["criminals"][0]),
                    str(line["meta"]["term_of_imprisonment"]["death_penalty"]),
                    str(line["meta"]["term_of_imprisonment"]["imprisonment"]),
                    str(line["meta"]["term_of_imprisonment"]["life_imprisonment"])]
            tsv_data.append(line)
        tsv_data = ["\t".join(line) + "\n" for line in tsv_data]
        tsv_data[-1] = tsv_data[-1].strip()
        with open(tsv_file_path, 'w', encoding="utf-8", newline="\n") as f:
            f.writelines(tsv_data)

    def dir2dir(source_dir_path, target_dir_path):
        if not pathlib.Path(target_dir_path).exists():
            os.makedirs(target_dir_path)
        for file_or_dir in os.listdir(source_dir_path):
            source_path = os.path.join(source_dir_path, file_or_dir)
            target_path = os.path.join(target_dir_path, file_or_dir)
            if pathlib.Path(source_path).is_dir():
                dir2dir(source_path, target_path)
            elif source_path.endswith(".json"):
                target_path = "%s.tsv" % target_path.split(".")[0]
                json2tsv(source_path, target_path)

    dir2dir(source, target)


if __name__ == '__main__':
    source_path = r"E:\PyCharmWorkspace\models\final_all_data"
    # target_path = r"E:\PyCharmWorkspace\models\testing\bert\data_dir"
    multi_target_path = r"E:\PyCharmWorkspace\models\testing\torch_pretrained_bert_multi\multi_data_dir"
    # cail2tsv(source_path, target_path)
    cail2tsv_multi(source_path, multi_target_path)
