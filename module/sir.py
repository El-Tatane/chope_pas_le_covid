import numpy as np
from scipy.integrate import solve_ivp, odeint
import matplotlib.pyplot as plt

class SIRModel():

    def __init__(self, beta=0.2, gamma=0.1, run_default=False):
        # self.beta_0 = beta_init
        # self.gamma_0 = gamma_init
        self.beta_ = None
        self.gamma_ = None
        if run_default:
            self.beta_ = beta
            self.gamma_ = gamma

    def fit(self, X, y):
        return self

    """
        S = those susceptible but not yet infected with the disease
        I = the number of infectious individuals
        R = those individuals who have recovered from the disease and now have immunity to it
    """

    def predict(self, init_population, init_infected, day_number, init_recovered=0):
        t = np.linspace(0, day_number, day_number)
        SIR = (init_population - init_infected - init_recovered, init_infected, init_recovered)
        res = odeint(self.deriv, SIR, t, args=(init_population, self.beta_, self.gamma_))
        return res.T

    def deriv(self, SIR, t, N, beta, gamma):
        S, I, R = SIR
        dSdt = -beta * S * I / N
        dIdt = beta * S * I / N - gamma * I
        dRdt = gamma * I
        return dSdt, dIdt, dRdt
