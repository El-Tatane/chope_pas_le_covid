import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp, odeint
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

class SEIRDModel():
    """
    Info SEIR model

    S = those susceptible but not yet infected with the disease
    E = individuals that have contracted the disease but are not yet infectious
    I = the number of infectious individuals
    R = those individuals who have recovered from the disease and now have immunity to it

    """

    def __init__(self, beta=0.3, gamma=0.1, delta=0.3, alpha=0.2, rho=0.1):
        self.params = {}
        self.params["beta"] = beta
        self.params["gamma"] = gamma
        self.params["delta"] = delta
        self.params["alpha"] = alpha
        self.params["rho"] = rho

    def get_SEIRD_0(self, N, I_0, E_0, R_0=0, D_0=0):
        S_0 = N - E_0 - I_0 - R_0
        SEIRD_0 = S_0, E_0, I_0, R_0, D_0
        return SEIRD_0

    def fit(self, y, N, E_0=1):
        t = np.linspace(0, len(y), len(y))

        SEIRD_0 = self.get_SEIRD_0(N, y[0], E_0)

        f = lambda t, beta, gamma, delta, alpha, rho : (odeint(self.deriv, SEIRD_0, t, args=(N, beta, gamma, delta, alpha, rho)).T)[2]

        params, covariance = curve_fit(f, t, y)
        self.params["beta"] = params[0]
        self.params["gamma"] = params[1]
        self.params["delta"] = params[2]
        self.params["alpha"] = params[3]
        self.params["rho"] = params[4]
        return params, covariance

    def deriv(self, y, t, N, beta, gamma, delta, alpha, rho):
        S, E, I, R, D = y
        dSdt = -beta * S * I / N
        dEdt = beta * S * I / N - delta * E
        dIdt = delta * E - (1 - alpha) * gamma * I - alpha * rho * I
        dRdt = (1 - alpha) * gamma * I
        dDdt = alpha * rho * I
        return dSdt, dEdt, dIdt, dRdt, dDdt

    def predict(self, t, N, I_0=1, E_0=1):
        SEIRD_0 = self.get_SEIRD_0(N, I_0, E_0)
        res = odeint(self.deriv, SEIRD_0, t, args=(N, self.params["beta"], self.params["gamma"], self.params["delta"],
                                                   self.params["alpha"], self.params["rho"]))
        return res.T
