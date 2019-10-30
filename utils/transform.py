import json
import os
import pathlib

KEY_LABEL = ["pieceNum", "title"]


def __trans_main_body(raw_main_body):
    # TODO 将原始mainBody转换为树结构
    main_body = {}
    return main_body


def __trans_json(source_file, target_file):
    with open(source_file, 'r', encoding='utf-8') as f:
        raw_laws = json.load(f)
    raw_main_body = raw_laws['data']['mainBody']
    main_body = __trans_main_body(raw_main_body)
    with open(target_file, 'w', encoding='uf-8') as f:
        json.dump(main_body, f, ensure_ascii=False)


def __trans_dir(source_dir, target_dir):
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
    if not pathlib.Path(source_dir).exists():
        raise RuntimeError("源文件夹不存在")
    __trans_dir(source_dir, target_dir)
