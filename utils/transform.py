import json
import os
import pathlib
import re

"""
用于转换原始法律条文（度小法）
若更换爬虫需重写转换函数（重写__trans_main_body函数即可）
"""


def __trans_main_body(raw_main_body):
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
        return re.sub('\s*', '', content)

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


def __trans_json(source_file, target_file):
    """
    json文件转换
    :param source_file: 需转换的源文件路径
    :param target_file: 转换后需保存的目标路径
    """
    with open(source_file, 'r', encoding='utf-8') as f:
        raw_laws = json.load(f)
    raw_main_body = raw_laws['data']["mainBody"]
    main_body = __trans_main_body(raw_main_body)
    with open(target_file, 'w', encoding='utf-8') as f:
        json.dump(main_body, f, ensure_ascii=False)


def __trans_dir(source_dir, target_dir):
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
            __trans_dir(s_item, t_item)
        else:
            __trans_json(s_item, t_item)


def to_law(source_dir, target_dir):
    """
    转换为法律条文格式
    :param source_dir: 源文件夹
    :param target_dir: 存储目标文件夹
    """
    print('TRANSFORMING...')
    if not pathlib.Path(source_dir).exists():
        raise RuntimeError("源文件夹不存在")
    __trans_dir(source_dir, target_dir)
    print('DONE')
