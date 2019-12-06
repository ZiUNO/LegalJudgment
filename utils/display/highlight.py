from bertviz import model_view
from transformers import BertTokenizer, BertForSequenceClassification

model_version = r"E:/PyCharmWorkspace/LegalJudgment/utils/model/transformers_bert/tmp/self"
do_lower_case = True
model = BertForSequenceClassification.from_pretrained(model_version, output_attentions=True)
tokenizer = BertTokenizer.from_pretrained(model_version, do_lower_case=do_lower_case)

sentence_a = "周某打伤刘某"
sentence_b = "马某被孙某打伤"

hide_delimiter_attn = False

inputs = tokenizer.encode_plus(sentence_a, sentence_b, return_tensors='pt', add_special_tokens=True)
token_type_ids = inputs['token_type_ids']
input_ids = inputs['input_ids']

logits = model(input_ids, token_type_ids=token_type_ids)
attention = logits[-1]

input_id_list = input_ids[0].tolist()  # Batch index 0
tokens = tokenizer.convert_ids_to_tokens(input_id_list)

if sentence_b:
    sentence_b_start = token_type_ids[0].tolist().index(1)
else:
    sentence_b_start = None
if hide_delimiter_attn:
    for i, t in enumerate(tokens):
        if t in ("[SEP]", "[CLS]"):
            for layer_attn in attention:
                layer_attn[0, :, i, :] = 0
                layer_attn[0, :, :, i] = 0

model_view(attention, tokens, sentence_b_start)

for lay in attention:
    for i in lay:
        print(" ".join(i.values))
