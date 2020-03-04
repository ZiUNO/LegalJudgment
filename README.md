# LegalJudgment
## Dir
```
.
|-- data/
|   |-- 中国法律大全JSON/                 -- 处理后的度小法的法律文献
|   |-- 中国法律大全JSON_DXF/             -- 爬自度小法的法律文献
|   |-- 案例/                            -- 案例数据
|   |   |-- cases/                             -- 原始案例文件
|   |   |-- handled/                           -- 人工处理后的案情文本
|   |   |-- multi_data_dir/                    -- 用于案情多标签分类的数据集
|   |   |-- raw/                               -- 原始案例文件（json）
|   |   |-- raw_/                              -- 经ipynb初步处理的案例文件
|   |   |-- invalid_uniqid.json                -- 下载失败的uniqid列表
|   |   |-- kinds.txt                          -- 案情种类
|   |   |-- to_consider.json                   -- 案例中的需考虑部分
|   |   |-- uniqid.json                        -- uniqid文件（觅律搜索标识）
|   |-- synonyms.json                          -- 同义词文件
|-- sofa/                                      -- 小程序
|   |-- images/                                -- 小程序图片
|   |   |-- logo.png                           -- logo图片
|   |-- pages/                                 -- 小程序界面
|   |   |-- about/                             -- 关于界面
|   |   |-- case/                              -- 案例界面
|   |   |-- index/                             -- 主页界面
|   |   |-- search/                            -- 检索界面
|   |-- styles/
|   |   |-- weui.wxss                          -- weui
|   |-- app.js
|   |-- app.json
|   |-- app.wxss
|   |-- project.config.json
|   |-- sitemap.json
|-- utils/
|   |-- __init__.py
|   |-- data/
|   |   |-- cail2tsv.py                        -- cail-2018转tsv
|   |   |-- crawler.py                         -- 度小法爬虫
|   |   |-- handle_case.ipynb                  -- 结合人工进行案例处理
|   |   |-- handleq.py                         -- 处理问题q
|   |   |-- transform.py                       -- 度小法格式转换
|   |-- display/                               -- [废弃]测试用
|   |-- engine/
|   |   |-- db.py                              -- 数据库操作
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
> 执行步骤：crawler.py->transform.py->main.py->flask run.py