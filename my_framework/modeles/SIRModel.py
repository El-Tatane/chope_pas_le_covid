import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp, odeint
from scipy.optimize import curve_fit


class SIRModel():
    """
    Info SIR model

    S = those susceptible but not yet infected with the disease
    I = the number of infectious individuals
    R = those individuals who have recovered from the disease and now have immunity to it

    """

    def __init__(self, beta=0.3, gamma=0.1):
        self.params = {}
        self.params["beta"] = beta
        self.params["gamma"] = gamma

    def get_SIR_0(self, N, I_0):
        R_0 = 0
        S_0 = N - I_0 - R_0
        SIR_0 = S_0, I_0, R_0
        return SIR_0

    def fit(self, N, I, R=None):
        if R is None:
            return self.fit_I(I, N)
        else:
            return self.fit_IR(I, R, N)

    def fit_I(self, y, N):
        if y[0] == 0 : raise ValueError("Need an infected at the beginning")
        t = np.linspace(0, len(y), len(y))
        SIR_0 = self.get_SIR_0(N, y[0])

        f = lambda t, beta, gamma : (odeint(self.deriv, SIR_0, t, args=(N, beta, gamma)).T)[1]

        params, covariance = curve_fit(f, t, y)
        self.params["beta"] = params[0]
        self.params["gamma"] = params[1]
        return params, covariance

    def fit_IR(self, I, R, N):
        if I[0] == 0 : raise ValueError("Need an infected at the beginning")
        t = np.linspace(0, len(I)*2, len(I)* 2)
        y = np.hstack((I, R))

        SIR_0 = self.get_SIR_0(N, I[0])

        f = lambda t, beta, gamma : np.hstack((odeint(self.deriv, SIR_0, t, args=(N, beta, gamma)).T)[1:2])

        params, covariance = curve_fit(f, t, y)
        self.params["beta"] = params[0]
        self.params["gamma"] = params[1]
        return params, covariance

    def deriv(self, y, t, N, beta, gamma):
        S, I, R = y
        dSdt = -beta * S * I / N
        dIdt = beta * S * I / N - gamma * I
        dRdt = gamma * I
        return dSdt, dIdt, dRdt

    def predict(self, t, N, I_0=1):
        # t_inter = (min(t), max(t))
        SIR_0 = self.get_SIR_0(N, I_0)
        res = odeint(self.deriv, SIR_0, t, args=(N, self.params["beta"], self.params["gamma"]))
        return res.T
