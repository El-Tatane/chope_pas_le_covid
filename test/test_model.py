import numpy as np
import pandas as pd

from my_framework.modeles.SIRModel import SIRModel
from my_framework.etl import get_dataset
from my_framework.plot import plot_simple_sir, plot_triple_sir


def test_model_sir_1():

    # Result
    result_beta = 1
    result_gamma = 0.1

    pop_size = 55000000
    df = pd.read_csv("/home/covid/dataset/data_1.csv")
    model_sir = SIRModel()
    model_sir.fit(df["I"], pop_size)
    assert abs(model_sir.params["beta"] - result_beta) < 1
    assert abs(model_sir.params["gamma"] - result_gamma) < 1


def test_model_sir_2():

    # Result
    result_beta = 0.01
    result_gamma = 0.005

    pop_size = 670000
    df = pd.read_csv("/home/covid/dataset/data_2.csv")
    model_sir = SIRModel()
    model_sir.fit(df["I"], pop_size)
    assert abs(model_sir.params["beta"] - result_beta) < 1
    assert abs(model_sir.params["gamma"] - result_gamma) < 1


def test_model_sir_3():

    # Result
    result_beta = 0.5
    result_gamma = 0.2

    pop_size = 7700000000
    df = pd.read_csv("/home/covid/dataset/data_3.csv")
    model_sir = SIRModel()
    model_sir.fit(df["I"], pop_size)
    assert abs(model_sir.params["beta"] - result_beta) < 1
    assert abs(model_sir.params["gamma"] - result_gamma) < 1
