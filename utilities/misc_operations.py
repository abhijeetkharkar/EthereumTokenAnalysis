import pickle
from matplotlib import pyplot as plt
from datetime import datetime
import random
import numpy as np
import sys


def dump_load_pickle_object(action="", filename="", data=""):
    if action == "dump":
        dump = open(filename, 'wb')
        pickle.dump(data, dump)
        dump.close()
        return None
    else:
        dump = open(filename, 'rb')
        data = pickle.load(dump)
        dump.close()
        return data


# Plotting Function
def plot_basic_line_chart(x_data, y_data, title, x_label, y_label, save="Y", show="N", date=False):
    colors = ['b', 'g', 'r', 'c', 'm', 'y']
    plt.figure(figsize=(20, 9), dpi=100)
    plt.style.use("ggplot")
    plt.tight_layout()
    color = colors[random.randint(0, len(colors)-1)] + "-"
    if date:
        plt.plot_date(x_data, y_data, color)
    else:
        plt.plot(x_data, y_data, color)
    plt.title(title, fontsize=20)
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.axis([min(x_data), max(x_data), min(y_data), max(y_data)])
    plt.xticks(rotation=90, fontsize=8)
    if save == "Y":
        plt.savefig("output/plots/" + title.replace('/', '') + ".png", dpi=500, bbox_inches='tight')
    if show == "Y":
        plt.show()


def plot_multiple_lines_chart(data_map, title, x_label, y_label, save="Y", show="N", date=False):
    colors = ['b', 'g', 'r', 'c', 'm', 'y']
    plt.figure(figsize=(20, 9), dpi=100)
    plt.style.use("ggplot")
    plt.tight_layout()
    x_min = sys.maxsize
    x_max = 0
    y_min = sys.maxsize
    y_max = 0
    for key in data_map:
        color = colors.pop() + "-"
        if date:
            # print(set([type(entity) for entity in data_map.get(key)[0]]))
            plt.plot_date(data_map.get(key)[0], data_map.get(key)[1], color, label=key)
        else:
            # print("X: ", data_map.get(key)[0])
            # print("Y: ", data_map.get(key)[1])
            plt.plot(data_map.get(key)[0], data_map.get(key)[1], color, label=key)
        # print(max(data_map.get(key)[0]))
        if date:
            if x_max < max(data_map.get(key)[0]):
                x_max = max(data_map.get(key)[0])
            if y_max < max(data_map.get(key)[1]):
                y_max = max(data_map.get(key)[1])
            if x_min > min(data_map.get(key)[0]):
                x_min = min(data_map.get(key)[0])
            if y_min > min(data_map.get(key)[1]):
                y_min = min(data_map.get(key)[1])

    # print(x_min, "|", x_max, "|", y_min, "|", y_max)
    plt.title(title, fontsize=20)
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    if date:
        plt.axis([x_min, x_max, y_min, y_max])
    plt.xticks(rotation=90, fontsize=8)
    plt.legend()
    if save == "Y":
        plt.savefig("output/plots/" + title.replace('/', '') + ".png", dpi=500, bbox_inches='tight')
    if show == "Y":
        plt.show()


def plot_basic_bar_chart(x_axis, y_axis, title, x_label, y_label, x_label_font_size=8, save="Y", show="N"):
    plt.figure(figsize=(20, 9), dpi=100)
    plt.style.use("ggplot")
    plt.bar(np.arange(len(x_axis)), y_axis, align='center', alpha=0.5)
    plt.xticks(np.arange(len(x_axis)), x_axis, fontsize=10)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.xticks(rotation=90, fontsize=x_label_font_size)
    if save == 'Y':
        plt.savefig("output/plots/" + title.replace('/', '') + ".png", dpi=500)
    if show == 'Y':
        plt.show()
