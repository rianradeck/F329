import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
import sys

def get_ups_and_downs(Y):
    ups = []
    downs = []
    for i in range(10, len(Y)):
        if (np.sign(Y[i-10:i].max()) < 0) and (np.sign(Y[i]) >= 0):
            ups.append(i)
        if (np.sign(Y[i-10:i].min()) > 0) and (np.sign(Y[i]) <= 0):
            downs.append(i)
    return np.array(ups), np.array(downs)

def get_data_from_csv(path):
    df = pd.read_csv(path, header=None, names = ["1", "2", "3", "4", "5"])
    
    X = np.array(df["3"])
    Y = np.array(df["4"])
    return X, Y

def get_info(path, filter_size=5, name="", line=None, wave="sine", other_function=None):
    X, Y = get_data_from_csv(path)
    other_function = {"X": other_function[0], "Y": other_function[1]} if other_function else None
    filtered_Y = np.convolve(Y, np.ones(filter_size) / filter_size)

    plot = go.Scatter(
        x = X,
        y = filtered_Y,
        name = name,
        line=line
    )

    ups, downs = get_ups_and_downs(Y)

    if len(ups) > 1:
        freq = np.diff(X[ups]).mean()
    elif len(downs) > 1:
        freq = np.diff(X[downs]).mean()
    else:
        freq = -1
    Vpp = Y.max() - Y.min()

    print("#" * 10 + f" {name} " + "#" * 10)
    print("Amplitude", Vpp)
    print("Frequência", freq)
    print("Vrms", Vpp / (2 * (np.sqrt(2) if wave == "sine" else 1)))

    if other_function:
        ups_, downs_ = get_ups_and_downs(other_function["Y"])

        other_ups_times = other_function["X"][ups_]
        ups_times = X[ups]
        other_closer_to_origin = other_ups_times[np.abs(other_ups_times).argmin()]
        closer_to_origin = ups_times[np.abs(ups_times).argmin()] 

        print("Fase", np.abs(abs(closer_to_origin) - abs(other_closer_to_origin)))

    return X, Y, plot

if __name__ == "__main__":
    _, _, c1_ch1 = get_info("./ALL0000/F0000CH1.CSV", name="A", other_function=get_data_from_csv("./ALL0000/F0000CH2.CSV"))
    _, _, c1_ch2 = get_info("./ALL0000/F0000CH2.CSV", name="B")

    _, _, c2_ch1 = get_info("./ALL0002/F0002CH1.CSV", name="C")
    _, _, c2_ch2 = get_info("./ALL0002/F0002CH2.CSV", name="D", filter_size=1)

    _, _, c3_ch1 = get_info("./ALL0006/F0006CH1.CSV", name="E 20Hz Onda quadrada", wave="square")
    _, _, c3_ch2 = get_info("./ALL0006/F0006CH2.CSV", name="F 20Hz Onda quadrada", wave="square")

    fig = make_subplots(rows=3, cols=1)#, specs=[[{}, {}],
                                        #      [{"colspan": 2}, None]])

    fig.add_trace(c1_ch1, row=1, col=1)
    fig.add_trace(c1_ch2, row=1, col=1)

    fig.add_trace(c2_ch1, row=2, col=1)
    fig.add_trace(c2_ch2, row=2, col=1)

    fig.add_trace(c3_ch1, row=3, col=1)
    fig.add_trace(c3_ch2, row=3, col=1)

    fig_c3 = make_subplots(rows=3, cols=1)


    _, _, c3A_ch1 = get_info("./ALL0008/F0008CH1.CSV", name="E 21.1638 hz", other_function=get_data_from_csv("./ALL0008/F0008CH2.CSV"))
    _, _, c3A_ch2 = get_info("./ALL0008/F0008CH2.CSV", name="F 21.1638 hz")

    _, _, c3B_ch1 = get_info("./ALL0007/F0007CH1.CSV", name="E 211.638 hz")
    _, _, c3B_ch2 = get_info("./ALL0007/F0007CH2.CSV", name="F 211.638 hz")

    _, _, c3C_ch1 = get_info("./ALL0009/F0009CH1.CSV", name="E 2116.38 hz")
    _, _, c3C_ch2 = get_info("./ALL0009/F0009CH2.CSV", name="F 2116.38 hz")

    fig_c3.add_trace(c3A_ch1, row=1, col=1)
    fig_c3.add_trace(c3A_ch2, row=1, col=1)

    fig_c3.add_trace(c3B_ch1, row=2, col=1)
    fig_c3.add_trace(c3B_ch2, row=2, col=1)

    fig_c3.add_trace(c3C_ch1, row=3, col=1)
    fig_c3.add_trace(c3C_ch2, row=3, col=1)

    fig.show()
    fig_c3.show()