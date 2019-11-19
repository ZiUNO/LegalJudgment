import json
import os
import pathlib
import re

"""
标记：['title', 'content', '[PIECE]']
"""
from tensorflow_estimator.python.estimator.gc import Path

"""
用于转换原始法律条文（度小法）
若更换爬虫需重写转换函数（重写__trans_main_body函数即可）
"""


def __dxf_trans_main_body(raw_main_body):
    """
    转换mainBody部分（若爬虫更改则需重写）
    :param raw_main_body: 未处理的mainBody部分
    :return: 格式转换后的mainBody
    """

    def handle_title(title):
        try:
            title = re.findall(u'(第[零一二三四五六七八九十百千万亿]+[编章条节]之*[零一二三四五六七八九十百千万亿]*\s|附则)(.*)$', title)[0]
        except:
            return [title]
        title = list(title)
        title[0] = title[0].strip()
        if len(title) == 2:
            title[1] = title[1].replace(u'\u3000', u'')
            if title[1] == '':
                del title[1]
        return title

    def handle_content(content):
        # return re.sub('\s*', '', content)
        return content  # 保留条文中的换行符

    main_body = {}
    for piece in raw_main_body:
        piece_num = piece["pieceNum"]
        piece_content = piece["content"]
        piece_num_split = handle_title(piece_num)
        if piece_num_split[0] not in main_body:
            main_body[piece_num_split[0]] = {}
            main_body[piece_num_split[0]]["content"] = {}
            if len(piece_num_split) == 2:
                main_body[piece_num_split[0]]["title"] = piece_num_split[1]
        for chapter in piece_content:
            chapter_title = chapter["title"]
            chapter_content = chapter["content"]
            chapter_title_split = handle_title(chapter_title)
            if chapter_title_split[0] not in main_body[piece_num_split[0]]["content"]:
                main_body[piece_num_split[0]]["content"][chapter_title_split[0]] = {}
                main_body[piece_num_split[0]]['content'][chapter_title_split[0]]["content"] = {}
                if len(chapter_title_split) == 2:
                    main_body[piece_num_split[0]]['content'][chapter_title_split[0]]["title"] = \
                        chapter_title_split[1]
            for item in chapter_content:
                item_title = item["title"]
                item_text = item["text"]
                item_title_split = handle_title(item_title)
                if item_title_split[0] not in main_body[piece_num_split[0]]["content"][chapter_title_split[0]]:
                    main_body[piece_num_split[0]]['content'][chapter_title_split[0]]["content"][
                        item_title_split[0]] = {}
                    if len(item_title_split) == 2:
                        main_body[piece_num_split[0]]['content'][chapter_title_split[0]]["content"][
                            item_title_split[0]]["title"] = \
                            item_title_split[1]
                    main_body[piece_num_split[0]]['content'][chapter_title_split[0]]["content"][
                        item_title_split[0]][
                        'content'] = handle_content(item_text)

    return main_body


def __dxf_trans_json(source_file, target_file):
    """
    json文件转换
    :param source_file: 需转换的源文件路径
    :param target_file: 转换后需保存的目标路径
    """
    with open(source_file, 'r', encoding='utf-8') as f:
        raw_laws = json.load(f)
    raw_main_body = raw_laws['data']["mainBody"]
    main_body = __dxf_trans_main_body(raw_main_body)
    with open(target_file, 'w', encoding='utf-8') as f:
        json.dump(main_body, f, ensure_ascii=False)


def __dxf_trans_dir(source_dir, target_dir):
    """
    文件夹转换（内含json文件）
    :param source_dir: 源文件夹
    :param target_dir: 目标存储文件夹
    """
    if not pathlib.Path(target_dir).exists():
        os.makedirs(target_dir)
    for item in os.listdir(source_dir):
        s_item = os.path.join(source_dir, item)
        t_item = os.path.join(target_dir, item)
        if pathlib.Path(s_item).is_dir():
            __dxf_trans_dir(s_item, t_item)
        else:
            __dxf_trans_json(s_item, t_item)


def dxf_to_law(source_dir, target_dir):
    """
    转换为法律条文格式
    :param source_dir: 源文件夹
    :param target_dir: 存储目标文件夹
    """
    print('TRANSFORMING DXF TO LAW...')
    if not pathlib.Path(source_dir).exists():
        raise RuntimeError("源文件夹不存在")
    __dxf_trans_dir(source_dir, target_dir)
    print('DONE')


def to_dir(source_dir, target_dir):
    """
    将源文件夹展开，即对其中json文件进行展开
    注：在执行该函数前，需手动调整：专利法.json 第五章第四十四条、第四十七条，将部分内容调整至content中，否则会报错
    :param source_dir:
    :param target_dir:
    """
    def json_to_dir(json_data, dir_path):
        print("TRANSFORMING %s TO DIR..." % dir_path)
        for title in json_data:
            content = json_data[title]
            title = re.sub('\s*', '', title)
            title = '[PIECE]' if not len(title) else title
            title_path = os.path.join(dir_path, title)
            if isinstance(content, dict):
                if not pathlib.Path(title_path).exists():
                    os.makedirs(title_path)
                json_to_dir(content, title_path)
            else:
                with open(title_path + '.txt', 'w', encoding='utf-8', newline='') as f:
                    f.write(content)

    for file_dir in os.listdir(source_dir):
        source_path = os.path.join(source_dir, file_dir)
        target_path = os.path.join(target_dir, file_dir)
        path_type = pathlib.Path(source_path)
        if path_type.is_dir():
            if not pathlib.Path(target_dir).exists():
                os.makedirs(target_path)
            to_dir(source_path, target_path)
        elif path_type.is_file():
            with open(source_path, 'r', encoding='utf-8') as f:
                law = json.load(f)
            target_path = target_path[:-4]
            if not pathlib.Path(target_path).exists():
                os.makedirs(target_path)
            json_to_dir(law, target_path)
        else:
            raise RuntimeError("%s 出错" % source_dir)


if __name__ == '__main__':
    # dxf_path = os.path.join('..', '..', 'data', '中国法律大全JSON_DXF')
    law_path = os.path.join('..', '..', 'data', '中国法律大全JSON')  # 格式化后的法律条文的保存路径
    dir_path = os.path.join('..', '..', 'data', '中国法律大全')
    # dxf_to_law(dxf_path, law_path)  # 格式化下载的法律条文
    to_dir(law_path, dir_path)
