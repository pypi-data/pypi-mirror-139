# -*- coding: utf-8 -*-
# @Time    : 2022/2/21 16:43
# @Author  : wyw


import pandas as pd
__all__ = ["pt_class_report"]

def get_metric(y_trues, y_preds):
    assert len(y_trues) == len(y_preds)
    length = len(y_preds)
    X, Y, Z = 1e-10, 1e-10, 1e-10
    count = 0
    for i in range(length):
        pred = y_preds[i]
        true = y_trues[i]

        R = set(pred)
        T = set(true)

        X += len(R & T)
        Y += len(R)
        Z += len(T)

        count += len(true)
    precision = X / Y if X != 1e-10 else 0.
    recall = X / Z if X != 1e-10 else 0.
    f1 = 2 * X / (Y + Z) if X != 1e-10 else 0.
    return (precision, recall, f1, count)


def get_class_report(y_trues, y_preds):
    metric_map = {}
    all_trues = []
    all_preds = []
    for k, v in y_trues.items():
        tmp_trues = v
        tmp_preds = y_preds[k]
        metric_map[k] = get_metric(tmp_trues, tmp_preds)

        all_trues.extend(tmp_trues)
        all_preds.extend(tmp_preds)

    avg_f1, avg_precision, avg_recall = 0., 0., 0.
    weight_f1, weight_precision, weight_recall = 0., 0., 0

    e_count = 0

    for k, v in metric_map.items():
        avg_precision += v[0]
        avg_recall += v[1]
        avg_f1 += v[2]
        e_count += v[3]

        weight_precision += v[0] * v[3]
        weight_recall += v[1] * v[3]
        weight_f1 += v[2] * v[3]

    avg_precision /= len(metric_map)
    avg_recall /= len(metric_map)
    avg_f1 /= len(metric_map)

    weight_precision /= e_count
    weight_recall /= e_count
    weight_f1 /= e_count

    metric_map[''] = ("", "", "", "")
    metric_map['micro avg'] = get_metric(all_trues, all_preds)
    metric_map['macro avg'] = (avg_precision, avg_recall, avg_f1, e_count)
    metric_map['weight avg'] = (weight_precision, weight_recall, weight_f1, e_count)
    metric_pd = pd.DataFrame(metric_map)
    metric_pd = metric_pd.transpose()

    metric_pd.columns = ["precision", "recall", "f1", "support"]
    metric_pd = metric_pd.rename(lambda x: "            " + x + "                ")

    f1 = avg_f1
    str_report = metric_pd.to_string(justify="left")
    return str_report, f1


def pt_class_report(y_trues,y_preds,label_list):
    id2label = {i: label for i, label in enumerate(label_list)}
    my_trues = {
        label: [] for i, label in id2label.items()
    }
    my_preds = {
        label: [] for i, label in id2label.items()
    }
    for t,p in zip(y_trues,y_preds):
        one_trues = {
            label: [] for i, label in id2label.items()
        }
        one_preds = {
            label: [] for i, label in id2label.items()
        }
        for (l,start,end) in t:
            str_label = id2label[l]
            one_trues[str_label].append((l, start, end))
        for (l,start,end) in p:
            str_label = id2label[l]
            one_preds[str_label].append((l, start, end))

        for k, v in my_trues.items():
            v.append(one_trues[k])
        for k, v in my_preds.items():
            v.append(one_preds[k])

    str_report, f1 = get_class_report(my_trues,my_preds)
    return str_report, f1
