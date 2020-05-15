import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp, odeint
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

class SEIRModel():
    """
    Info SEIR model

    S = those susceptible but not yet infected with the disease
    E = individuals that have contracted the disease but are not yet infectious
    I = the number of infectious individuals
    R = those individuals who have recovered from the disease and now have immunity to it

    """

    def __init__(self, beta=0.3, gamma=0.1, delta=0.3):
        self.params = {}
        self.params["beta"] = beta
        self.params["gamma"] = gamma
        self.params["delta"] = delta

    def get_SEIR_0(self, N, I_0, E_0, R_0=0):
        S_0 = N - E_0 - I_0 - R_0
        SEIR_0 = S_0, E_0, I_0, R_0
        return SEIR_0

    def fit(self, N, I, R=None, E_0=1):
            if R is None:
                return self.fit_I(I, N, E_0)
            else:
                return self.fit_IR(I, R, N, E_0)

    def fit_I(self, y, N, E_0):
        if y[0] == 0 : raise ValueError("Need an infected at the beginning")
        t = np.linspace(0, len(y), len(y))

        SEIR_0 = self.get_SEIR_0(N, y[0], E_0)

        f = lambda t, beta, gamma, delta : (odeint(self.deriv, SEIR_0, t, args=(N, beta, gamma, delta)).T)[2]

        params, covariance = curve_fit(f, t, y)
        self.params["beta"] = params[0]
        self.params["gamma"] = params[1]
        self.params["delta"] = params[2]
        return params, covariance

    def fit_IR(self, I, R, N, E_0):
        if I[0] == 0 : raise ValueError("Need an infected at the beginning")
        t = np.linspace(0, len(I)*2, len(I)* 2)
        y = np.hstack((I, R))

        SIER_0 = self.get_SEIR_0(N, I[0], E_0)

        f = lambda t, beta, gamma, delta : np.hstack((odeint(self.deriv, SIER_0, t, args=(N, beta, gamma, delta)).T)[1:2])

        params, covariance = curve_fit(f, t, y)
        self.params["beta"] = params[0]
        self.params["gamma"] = params[1]
        self.params["delta"] = params[2]
        return params, covariance

    def deriv(self, y, t, N, beta, gamma, delta):
        S, E, I, R = y
        dSdt = -beta * S * I / N
        dEdt = beta * S * I / N - delta * E
        dIdt = delta * E - gamma * I
        dRdt = gamma * I
        return dSdt, dEdt, dIdt, dRdt

    def predict(self, t, N, I_0=1, E_0=1):
        SEIR_0 = self.get_SEIR_0(N, I_0, E_0)
        res = odeint(self.deriv, SEIR_0, t, args=(N, self.params["beta"], self.params["gamma"], self.params["delta"]))
        return res.T
