# LegalJudgment
## Dir
```
.
|-- data/
|-- utils/
|   |-- __init__.py
|   |-- data/
|   |   |-- cail2tsv.py                        -- cail-2018转tsv
|   |   |-- crawler.py                         -- 度小法爬虫
|   |   |-- transform.py                       -- 度小法格式转换
|   |-- display/                               -- [废弃]测试用
|   |-- engine/
|   |   |-- neo4j_engine.py                    -- 使用neo4j进行检索
|   |   |-- whoosh_engine.py                   -- [废弃]whoosh全文搜索框架
|   |   |-- 中文停用词表.txt
|   |-- model/
|   |   |-- bert/                              -- google-research/bert[单标签]改写
|   |   |-- svm_classifier/                    -- svm多标签分类器
|   |   |-- torch_pretrained_bert/             -- pytorch-pretrained-bert[单标签]改写
|   |   |-- torch_pretrained_bert_multi_label/ -- pytorch-pretrained-bert[多标签]改写
|   |   |-- transformers_bert/                 -- transformers[单标签]改写
|   |   |-- predict.py                         -- 预测标签、高亮后文字
|   |-- web/
|       |-- flaskr/
|           |-- models/
|           |-- static/
|           |   |-- img/
|           |   |   |-- logo.png               -- 程序图标
|           |   |   |-- qrcode.png             -- 小程序码（待更换）
|           |-- templates/
|           |   |-- about.html                 -- 关于界面
|           |   |-- case.html                  -- 案例界面
|           |   |-- exception.html             -- 异常界面
|           |   |-- index.html                 -- 主页界面
|           |   |-- search.html                -- 检索界面
|           |-- views/
|           |-- config.json                    -- 程序配置文件
|           |-- run.py                         -- 服务器运行文件
|           |-- setting.py
|-- config.json
|-- requirements.txt
|-- main.py
```
## P.S.
