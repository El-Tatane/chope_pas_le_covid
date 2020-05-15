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


def test_random_modele_sir():
    # Code juste, mais resultat des modèles pas exceptionnel.
    success, bad, error = 0, 0, 0

    for i in range(10):
        try:
            b_g = np.random.rand(2) * 5
            beta, gamma = max(b_g), min(b_g)
            pop_size = np.random.randint(100000, 1000000)
            day_number = np.random.randint(50, 200)
            t = np.linspace(0, day_number, day_number)
            I_0 = 1

            model_data_sir = SIRModel(beta=beta, gamma=gamma)
            S, I, R = model_data_sir.predict(t, pop_size, I_0)

            model_pred_sir = SIRModel()
            model_pred_sir.fit(I, pop_size)

            if  abs(model_data_sir.params["beta"] - model_pred_sir.params["beta"] ) < 1.5 and abs(model_data_sir.params["gamma"] - model_pred_sir.params["gamma"]) < 1.5:
                success += 1
            else:
                bad += 1
        except:
            error += 1
    assert bad + error != 10
