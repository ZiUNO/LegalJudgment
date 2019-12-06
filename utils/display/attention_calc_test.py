import json

if __name__ == '__main__':

    with open("attention.json", "r") as f:
        attention_data = json.load(f)
    attention = {}
    for lay in attention_data:
        attention[int(lay)] = {}
        for head in attention_data[lay]:
            matrix = attention_data[lay][head]
            matrix = [[float(i) for i in vec] for vec in matrix]
            attention[int(lay)][int(head)] = matrix
    with open("result.txt", 'r', newline="\n") as f:
        result_data = f.readlines()
    result = [float(data.strip()) for data in result_data]
    # TODO 根据attention计算result，得到计算过程，用于计算词汇权重
