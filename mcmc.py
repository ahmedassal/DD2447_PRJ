import numpy as np
import scipy as sp
import pandas as pd
import matplotlib
matplotlib.rcParams['backend'] = 'TkAgg'
# matplotlib.rcParams['backend'] = 'WXAgg'
# matplotlib.rcParams['backend'] = 'QTAgg'
# matplotlib.rcParams['backend'] = 'Qt4Agg'
# matplotlib.rcParams['backend'] = 'Qt5Agg'
import matplotlib.pyplot as plt
# plt.switch_backend('Qt5Agg')
import seaborn as sns
from scipy.stats import norm
from random import randint
from scipy.stats import mvn

#sigma = switchSettings = [ 1,-1, ...., N]
#postmeans = [0.32, ...., N]
def calc_q_probability(sigma, postMeans):
    low = []
    upp = []
    inf = 999

    for s in sigma:
        if np.sign(s)== -1:
            upp.append(0)
            low.append(-inf)
        else:
            upp.append(inf)
            low.append(0)
    p,i = mvn.mvnun(low,upp,postMeans,   np.identity(len(postMeans))*1 )
    #print('it work :D:D',p)
    return p

def test():
    return calc_q_probability([1,-1],  [0.3,0.1])

def example():
    #obs = [-1,-1,1,1]
    obs = [[-1,-1,1,1],[-1,-1,1,1]]
    # 0:s and 1:s for these is good
    mu_prior_mu = [0,0,0,0]
    mu_prior_sd=[1.,1.,1.,1.]
    t = MCMC_MH(obs, samples =100, mu_prior_mu=[0,0,0,0], mu_prior_sd=[1.,1.,1.,1.])
    print(t[-1])
    print(get_sigma(t[-1]))

# Argument should be the output of MCMC_MH
# Returns a list of switch settings
def get_sigma(t):
    settings = np.array(['L','R'])
    a = np.sign(t)
    low_values_indices = a == -1
    a[low_values_indices] = 0
    a =  list(map(int, a))
    return settings[a]


def MCMC_MH(obs, samples=4, mu_init=.5, proposal_width=.5, plot=False, mu_prior_mu=0, mu_prior_sd=1.):
    # Observations and switch need to be sequential
    mu_init= [0] *len(mu_prior_mu)
    proposal_width = [0.5]*len(mu_prior_mu)
    mu_prior_sd=[1.] *len(mu_prior_mu)
    # Alg starts
    mu_current = mu_init
    posterior = [mu_current]
    for i in range(samples):
        # suggest new position
        mu_proposal= []
        for m in range(len(mu_current)):
            mu_proposal.append(norm(mu_current[m], proposal_width[m]).rvs())
        #mu_proposal = norm(mu_current, proposal_width).rvs()

        # Compute likelihood by multiplying probabilities of each data point
        ## No need for product as we assume we know which observation comes from where
        likelihood_current = np.prod(norm(mu_current, np.ones(len(mu_current))).pdf(obs))
        likelihood_proposal = np.prod(norm(mu_proposal, np.ones(len(mu_current))).pdf(obs))
        #likelihood_current = norm(mu_current, np.ones(len(mu_current))).pdf(obs).prod()
        #likelihood_proposal = norm(mu_proposal, np.ones(len(mu_current))).pdf(obs).prod()

        # Compute prior probability of current and proposed mu
        prior_current_var = sp.stats.multivariate_normal(mu_prior_mu,np.identity(len(mu_prior_mu))* mu_prior_sd[0])
        prior_proposal_var = sp.stats.multivariate_normal(mu_prior_mu, np.identity(len(mu_prior_mu))*mu_prior_sd[0])
        prior_current = prior_current_var.pdf(mu_current)
        prior_proposal = prior_proposal_var.pdf(mu_proposal)
        #prior_current = norm(mu_prior_mu, mu_prior_sd).pdf(mu_current)
        #prior_proposal = norm(mu_prior_mu, mu_prior_sd).pdf(mu_proposal)


        p_current = likelihood_current * prior_current
        p_proposal = likelihood_proposal * prior_proposal
        print('he',p_current)
        print(p_proposal)

        # Accept proposal?
        p_accept = p_proposal / p_current

        # Usually would include prior probability, which we neglect here for simplicity
        accept = np.random.rand() < p_accept
        if plot:
            sns.plot_proposal(mu_current, mu_proposal, mu_prior_mu, mu_prior_sd, obs, accept, posterior, i)

        if accept:
            # Update position
            mu_current = mu_proposal

        posterior.append(mu_current)

    return posterior
