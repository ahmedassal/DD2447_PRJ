import mcmc as mc
import numpy as np
import matplotlib
matplotlib.rcParams['backend'] = 'TkAgg'
# matplotlib.rcParams['backend'] = 'WXAgg'
# matplotlib.rcParams['backend'] = 'QTAgg'
# matplotlib.rcParams['backend'] = 'Qt4Agg'
# matplotlib.rcParams['backend'] = 'Qt5Agg'
import matplotlib.pyplot as plt
# plt.switch_backend('Qt5Agg')
import generategraphs as gg
import networkx as nx
import pickle


def main():
  logsFolder = 'logs'
  networksFolder = 'networks'
  observationsFolder = 'observations'
  graphsFolder = 'graphs'
  simulationsNamesFile = "simulations"
  gg.generate_and_simulate()
  simulationsNamesFile = "simulations"

  simulations = []
  simulation = {}
  with open('{0}.txt'.format(simulationsNamesFile), "r") as text_file:
    content=text_file.readlines()
  # simulationsRaw = [x.strip() for x in content]
  for simName in content:
    simName = simName.strip()
    simulation['name'] = simName
    file = open("{0}/{1}.pickle".format(observationsFolder, simName), 'rb')
    observations = pickle.load(file)
    file.close()
    simulation['observations'] = observations
    simulations.append(simulation)
    # print(observations)

  # print(simulations)
  for sim_idx in range(len(simulations)):
    print(simulations[sim_idx]['observations'])
    convertedObs = convertObservations(simulations[sim_idx]['observations'])
    print(convertedObs)
    # simulations[sim_idx]['sigma'] = getSigma(simulations[sim_idx]['observations'])
    # simulations[sim_idx]['emissionsMat'] = getEmission(simulations[sim_idx]['sigma'])
  #   simulations[sim_idx]['transMat'] = getTransitionMat(simulations[sim_idx]['sigma'], n_vertices, graph)


    # simulationRaw[name]
    # for experiment_idx in range(EXPERIMENTS_COUNT):
    #   simultionName = "-".join(['sim', str(n_run), str(timestr), 'exp', str(experiment_idx)])

    # obs = getObservations()
    # sigma = getSigma(obs)
    # emissionMat = getEmission(sigma)
    # #G= []# graph dunno how it should be
    # transMat = getTransitionMat( sigma, len(sigma))
    # print(transMat)

def convertObservations(observations):
  convertedObs = []
  print(type(observations))
  print(len(observations))
  for obs in observations:
    if obs == 'L':
      convertedObs.append(-1)
    elif obs == 'O':
      convertedObs.append(0)
    elif obs == 'R':
      convertedObs.append(1)
    else:
      print("Observations conversion error!!!")
  return convertedObs

def getObservations(observations):
    # L, O ,R translates to -1,0,1
    convertedObs = convertObservations(observations)
    print(convertedObs)
    # obs = [-1,1,0,1]
    return convertedObs

def getSigma(obs):
    ## Setting up my prior beliefs and how many samples i want
    mcmcSamples = mc.MCMC_MH(obs, samples =100, mu_prior_mu=[0,0,0,0], mu_prior_sd=[1.,1.,1.,1.])
    return mc.get_sigma(mcmcSamples[-1]) # returns last switchsetting,for example ['L','R']

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
            lbl = getLabelForEdge(G, i,j)
            if lbl == sigma[i]:
                transMat[i][j] = 1
    return transMat

def getLabelForEdge(node1, node2):
    #TODO: S
    return 'L'

if __name__ == "__main__":
  main()