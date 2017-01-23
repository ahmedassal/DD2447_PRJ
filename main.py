import mcmc as mc
import numpy as np


def main():
    obs = getObservations()
    sigma = getSigma(obs)
    emissionMat = getEmission(sigma)
    #G= []# graph dunno how it should be
    transMat = getTransitionMat( sigma, len(sigma))
    print(transMat)


def getObservations():
    # L, O ,R translates to -1,0,1
    obs = [-1,1,0,1]
    return obs

def getSigma(obs):
    ## Setting up my prior beliefs and how many samples i want
    mcmcSamples = MCMC_MH(obs, samples =100, mu_prior_mu=[0,0,0,0], mu_prior_sd=[1.,1.,1.,1.])
    return get_sigma(mcmcSamples[-1]) # returns last switchsetting,for example ['L','R']

def getEmission(sigma):
    p = 0.05
    #Sigma only contains L or R
    settings =['L','O','R']
    emMat = np.ones((len(sigma), 3)) * (p/2)
    for i in range (len(sigma)):
        emMat[i][settings.index(sigma[i])]  = (1-p)
    return emMat

def getTransitionMat(sigma,N, G= None): # The sigma is the same sequence for how the train passed the switches
    transMat = np.zeros((N,N))
    for i in range(N):
        start = i
        for j in range(N):
            dst = j
            lbl = getLabelForEdge(i,j)
            if lbl == sigma[i]:
                transMat[i][j] = 1
    return transMat

def getLabelForEdge(node1, node2):
    #TODO: S
    return 'L'
