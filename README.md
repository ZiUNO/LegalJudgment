# LegalJudgment
## Dir
```
.
|-- data
|-- utils
|   |-- data
|   |   |-- cail2tsv.py                        -- cail-2018转tsv
|   |   |-- crawler.py                         -- 度小法爬虫
|   |   |-- transform.py                       -- 度小法格式转换
|   |-- display                                -- [废弃]测试用
|   |-- engine
|   |   |-- neo4j_engine.py                    -- 使用neo4j进行检索
|   |   |-- whoosh_engine.py                   -- [废弃]whoosh全文搜索框架
|   |   |-- 中文停用词表.txt
|   |-- model
|   |   |-- bert                               -- google-research/bert[单标签]改写
|   |   |-- svm_classifier                     -- svm多标签分类器
|   |   |-- torch_pretrained_bert              -- pytorch-pretrained-bert[单标签]改写
|   |   |-- torch_pretrained_bert_multi_label  -- pytorch-pretrained-bert[多标签]改写
|   |   |-- transformers_bert                  -- transformers[单标签]改写
|   |   |-- predict.py                         -- 预测标签、高亮后文字
|-- main.py
```
## P.S.
