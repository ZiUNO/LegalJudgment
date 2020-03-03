import json
import numpy as np

if __name__ == '__main__':

    with open("attention.json", "r") as f:
        attention_data = json.load(f)
    attention = []
    for i in range(12):
        lay = str(i)
        attention.append([])
        for j in range(12):
            head = str(j)
            matrix = attention_data[lay][head]
            matrix = [[float(i) for i in vec] for vec in matrix]
            attention[int(lay)].append([])
            attention[int(lay)][int(head)] = matrix
    with open("result.txt", 'r', newline="\n") as f:
        result_data = f.readlines()
    result = [float(data.strip()) for data in result_data]
    consider_layers_ids = [10]
    consider_layers = []
    for layer_id in consider_layers_ids:
        layer = attention[layer_id]
        head = np.average(layer, axis=0)
        to_consider_head = head[0:-1, 0:-1]
        consider_layers.append(to_consider_head)
    consider_layers = np.average(consider_layers, axis=0)
    cls2others = consider_layers[0, 1:]
    threshold = 0.5
    max_rate = cls2others.max()
    rate_threshold = max_rate * threshold
    huge_w_ids = list(np.where(cls2others >= rate_threshold)[0])
    print(huge_w_ids)
