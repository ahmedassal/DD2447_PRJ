import networkx as nx
from networkx.utils import uniform_sequence
# import matplotlib as mpl
import matplotlib
matplotlib.rcParams['backend'] = 'TkAgg'
# matplotlib.rcParams['backend'] = 'WXAgg'
# matplotlib.rcParams['backend'] = 'QTAgg'
# matplotlib.rcParams['backend'] = 'Qt4Agg'
# matplotlib.rcParams['backend'] = 'Qt5Agg'
import matplotlib.pyplot as plt
# plt.switch_backend('Qt5Agg')
from faker import Factory
import random
import logging
import logging.handlers
import numpy as np
import pandas as pd
import os, time, pickle


# mpl.use('Qt5Agg')
"""
I think here is what we need to do for synthetic data:

1- Generate a number of random graphs, a graph should be generated as follows:
  A-(Sizing) Pick a random n number for the number of vertices.
  B-(Connecting) create n vertices and connect every one of them to two other vertices randomly.
  C- (Labeling) Label the resulting edges randomly either as L, R, or O.
  D- (Programming Switches) Set every switch to L or R randomly.

2- Per each graph G simulate a number of train runs:
  A-Choose a random vertex as a start position.
  B- Let the train starts moving based on the start vertex switch programming.
      As the train travels and passed different vertices the switches will tell it where to go.
  C- Accumulate the labels of edges as the train arrives at each segment.
  D- if when leaving the current segment emit the last two(or one) labels accumulated.
  E- Log all data to another file including, timings, names and labels of vertices and edges, and the switches settings.

It is recommended that all data generated and all output is saved in files so if we need to interface with other tools
for graphing or solving HMM or MCMC it becomes easier to work with.

"""

"""
CONSTATS
"""

MAX_EDGES_PER_VERTEX = 3
GRAPH_DIM = 3
MIN_GRAPH_DIM = 3
MAX_GRAPH_DIM = 10
TARGET_VERTICES_COUNT = pow(GRAPH_DIM, 2)
LABELS = ['L', 'O', 'R' ]
SWITCHES_VALUES = ['R', 'L']
EXPERIMENTS_COUNT = 3
vertex1Key = 'V1'
vertex2Key = 'V2'
vertex1LabelKey = 'L1'
vertex2LabelKey = 'L2'

def stringizer(item):
  return str(item)

def makelog(filepath):
  logger = logging.getLogger(filepath)
  dir = os.path.split(filepath)
  dir = dir[0]
  if (not os.path.exists(dir)) and (dir != ''):
    os.makedirs( dir )
  #hdl = logging.handlers.RotatingFileHandler(filepath, maxBytes=2097152, backupCount=5, mode='w')
  hdl = logging.FileHandler(filepath, mode='w')
  formatter = logging.Formatter('%(asctime)s %(module)s, line %(lineno)d %(levelname)s %(message)s')
  hdl.setFormatter(formatter)

  logger.addHandler(hdl)
  logger.setLevel(logging.DEBUG)
  return logger

def create_fake_cities(fake, count):
  """"""
  cities = []
  # for i in range(count):
  #   cities.append(fake.city())

  cities = [fake.city() for i in range(count)]

  return cities

def compute_histogram(graph, logger):
  degree_sequence = list(nx.degree(graph).values())  # degree sequence
  logger.info("Degree sequence %s" % degree_sequence)
  logger.info("Degree histogram")
  hist = {}
  for d in degree_sequence:
    if d in hist:
      hist[d] += 1
    else:
      hist[d] = 1
  logger.info("degree #nodes")
  for d in hist:
    logger.info('%d %d' % (d, hist[d]))

def visualize_graph(graph, graphsFolder, experimentName, logger):
  try:
    logger.info("### Graph plotting started ==>")
    # nx.draw(graph, with_labels = True)
    # graph_pos = nx.shell_layout(graph)
    graph_pos = nx.spring_layout(graph)
    # graph_pos = nx.spectral_layout(graph)
    # nx.draw(graph, pos=nx.spring_layout(graph))
    # nx.draw_networkx_labels(graph, pos=nx.spring_layout(graph))

    nx.draw_networkx_nodes(graph, graph_pos, node_size=1000, node_color='blue', alpha=0.3)
    # nx.draw_networkx_node_labels(graph, graph_pos)
    nx.draw_networkx_edges(graph, graph_pos)
    nx.draw_networkx_edge_labels(graph, graph_pos)
    nx.draw_networkx_labels(graph, graph_pos, font_size=12, font_family='sans-serif')
    plt.title(experimentName)
    plt.show()
    plt.savefig("{0}/{1}.png".format(graphsFolder, experimentName))
    logger.info("### Graph plotting ended ==<")
  except:
    logger.error("### Graph is empty !!!!")


def create_graph(labels, dim, logger):
  logger.info("### Graph generation started ==>")
  # G = nx.grid_graph([GRAPH_DIM, GRAPH_DIM])
  G = nx.grid_2d_graph(dim, dim)
  n_target_vertices = pow(dim, 2)
  nodeToAdd_idx = TARGET_VERTICES_COUNT + 1
  nodeToAdd = len(G.nodes())
  nodesToRemove = [];
  nodesToModify = [];
  nodesToDuplicateN = 0;
  for node in G.nodes():
    if (G.degree(node) == 1):
      nodesToRemove.append(node);
    elif (G.degree(node) == 2):
      nodesToRemove.append(node);
    elif (G.degree(node) >= 4):
      neighbors = G.neighbors(node)

      # G.add_node(cities[nodeToAdd_idx])
      # G.add_edge(node, cities[nodeToAdd_idx])
      # G.add_edge(cities[nodeToAdd_idx], neighbors[2])
      # G.add_edge(cities[nodeToAdd_idx], neighbors[3])

      G.add_node(nodeToAdd)
      G.add_edge(node, nodeToAdd)
      G.add_edge(nodeToAdd, neighbors[2])
      G.add_edge(nodeToAdd, neighbors[3])

      G.remove_edge(node, neighbors[2])
      G.remove_edge(node, neighbors[3])
      # nodeToAdd_idx = nodeToAdd_idx + 1
      nodeToAdd = nodeToAdd + 1
      nodesToDuplicateN = nodesToDuplicateN + 1
      # G.add_edge(neighbors[2], neighbors[3])
    elif (G.degree(node) > 4):
      print("Warning greater than deg 4 ", node)
  for node in nodesToRemove:
    neighbors = G.neighbors(node)
    G.add_edge(neighbors[0], neighbors[1])
  # for node in nodesToModify:
  # print('number of nodes to remove', len(nodesToRemove))
  # print('number of nodes to duplicate ', nodesToDuplicateN)
  # print('number of nodes untouched', TARGET_VERTICES_COUNT - len(nodesToRemove) - nodesToDuplicateN)
  # print('number of resulting nodes in new graph ',
  #       TARGET_VERTICES_COUNT - len(nodesToRemove) - nodesToDuplicateN + 2 * nodesToDuplicateN)
  G.remove_nodes_from(nodesToRemove)
  mapping = {G.nodes()[i]: labels[i] for i in range(len(G.nodes())) for label in labels}
  graph = nx.relabel_nodes(G, mapping, copy=True)
  logger.info("### Graph generation ended ==<")
  return graph

def label_nodes(graph, labels):
  mapping = {graph.nodes()[i]: labels[i] for i in range(len(graph.nodes())) for label in labels}
  # graph = nx.relabel_nodes(graph, mapping, copy=False)
  # print(dic)
  # nx.set_node_attributes(graph, 'label', dic)

def label_graph(graph, labels, logger):
  logger.info("### Labels setting started ==>")
  if(any(x != 3 for x in list(nx.degree(graph).values()))):
    logger.error("### some graph's nodes do not have a degree of 3 !!!!")
  else:
    # # Row
    nodes = graph.nodes();
    potentialLabels = LABELS
    for node in graph.nodes():
      mappingVertices1 = {}
      mappingVertices1Label = {}

      mappingVertices2 = {}
      mappingVertices2Label = {}
      idx1 = np.arange(3)
      np.random.shuffle(idx1)
      # vertex2labels = [x for x in tmpX if x in ['O', 'R', 'L']]
      # idx1 = np.arange(3)
      # np.random.shuffle(idx2)
      idx_idx = 0
      for neighbor in nx.neighbors(graph, node):
        if vertex1Key not in graph[node][neighbor] and vertex1LabelKey not in graph[node][neighbor]:
          # graph[node][neighbor][vertex1Key] = node
          # graph[node][neighbor][vertex1LabelKey] = potentialLabels[idx1[idx_idx]]
          mappingVertices1[(node, neighbor)] = node
          mappingVertices1Label[(node, neighbor)] = potentialLabels[idx1[idx_idx]]  # labels[idx1[idx]]
        elif vertex2Key not in graph[node][neighbor] and vertex2LabelKey not in graph[node][neighbor]:
          # usedLabels = []
          # for neighborNeighbor in range(len(graph.nodes())):
          #   usedLabels.append(graph[neighborNeighbor][neighbor][vertex2LabelKey])
          #   potentialLabels2 = [x for x in potentialLabels if x not in usedLabels]
          # idx2 = np.arange(3)
          # np.random.shuffle(idx2)
          # graph[node][neighbor][vertex2Key] = node
          # graph[node][neighbor][vertex2LabelKey] = potentialLabels[idx1[idx_idx]]
          mappingVertices2[(node, neighbor)] = node
          mappingVertices2Label[(node, neighbor)] = potentialLabels[idx1[idx_idx]]  # labels[idx1[idx]]
        idx_idx = idx_idx + 1
      # nx.set_edge_attributes(graph, vertex1Key, mappingVertices1)
      # nx.set_edge_attributes(graph, vertex1LabelKey, mappingVertices1Label)
      # nx.set_edge_attributes(graph, vertex2Key, mappingVertices2)
      # nx.set_edge_attributes(graph, vertex2LabelKey, mappingVertices2Label)

      # nx.set_edge_attributes(graph, vertex1Key, mappingVertices1)
      nx.set_edge_attributes(graph, node, mappingVertices1Label)
      # nx.set_edge_attributes(graph, vertex2Key, mappingVertices2)
      nx.set_edge_attributes(graph, node, mappingVertices2Label)
      logger.info(mappingVertices1Label)
      logger.info(mappingVertices2Label)

        # mapping1[(nodes[i], nodes[j])] = lbl





    # for i in range(len(graph.nodes())):
    #   idx1 = np.arange(len(potentialLabels))
    #   np.random.shuffle(idx1)
    #   idx_idx = 0
    #   for j in range(i+1, len(graph.nodes())):
    #     if (df.ix[i, j] == 1):
    #       # lbl = np.random.choice(lbls, replace= False)
    #       df.ix[i, j] = potentialLabels[idx1[idx_idx]] #lbl #lbls[idx1[idx]]
    #       mappingVertices1[(list(df.index)[i], list(df.index)[j])] = list(df.index)[i]
    #       mappingVertices1Label[(list(df.index)[i], list(df.index)[j])] = potentialLabels[idx1[idx_idx]]  # labels[idx1[idx]]
    #
    #       # mapping1[(nodes[i], nodes[j])] = potentialLabels[idx1[idx_idx]]  #labels[idx1[idx]]
    #       idx_idx = idx_idx + 1
    #
    # print(mappingVertices1)
    # print(mappingVertices1Label)
    # nx.set_edge_attributes(graph, vertex1Key, mappingVertices1)
    # nx.set_edge_attributes(graph, vertex1LabelKey, mappingVertices1Label)
    #
    # # Columns
    # nodes = graph.nodes();
    # potentialLabels = ['L', 'O', 'R']
    # # for node in graph.nodes():
    # #   idx1 = np.arange(3)
    # #   np.random.shuffle(idx1)
    # #   vertex2labels = [x for x in tmpX if x in ['O', 'R', 'L']]
    # #   idx1 = np.arange(3)
    # #   np.random.shuffle(idx2)
    # #   idx_idx = 0
    # #   for neighbor in nx.neighbors(graph, node):
    # #     if vertex1Key not in graph[node][neighbor] and vertex1LabelKey not in graph[node][neighbor]:
    # #       graph[node][neighbor][vertex1Key] = node
    # #       graph[node][neighbor][vertex1LabelKey] = potentialLabels[idx1[idx_idx]]
    # #     elif vertex2Key not in graph[node][neighbor] and vertex2LabelKey not in graph[node][neighbor]:
    # #       # usedLabels = []
    # #       # for neighborNeighbor in range(len(graph.nodes())):
    # #       #   usedLabels.append(graph[neighborNeighbor][neighbor][vertex2LabelKey])
    # #       #   potentialLabels2 = [x for x in potentialLabels if x not in usedLabels]
    # #       # idx2 = np.arange(3)
    # #       # np.random.shuffle(idx2)
    # #       graph[node][neighbor][vertex2Key] = node
    # #       graph[node][neighbor][vertex2LabelKey] = potentialLabels[idx1[idx_idx]]
    # #
    # #     mapping1[(nodes[i], nodes[j])] = lbl
    # for i in range(len(graph.nodes())) :
    #   idx1 = np.arange(len(potentialLabels))
    #   np.random.shuffle(idx1)
    #   idx_idx = 0
    #   for j in range(i+1, len(graph.nodes())):
    #     print("by column ", i, j)
    #     if (df.ix[j, i] == 1):
    #       # lbl = np.random.choice(lbls, replace= False)
    #       df.ix[j, i] = potentialLabels[idx1[idx_idx]]  # lbl #lbls[idx1[idx]]
    #       mappingVertices2[(list(df.index)[j], list(df.index)[i])] = list(df.index)[j]
    #       mappingVertices2Label[(list(df.index)[j], list(df.index)[i])] = potentialLabels[idx1[idx_idx]]  # labels[idx1[idx]]
    #       # mapping1[(nodes[i], nodes[j])] = potentialLabels[idx1[idx_idx]]  #labels[idx1[idx]]
    #       idx_idx = idx_idx + 1

    # print(mappingVertices2)
    # print(mappingVertices2Label)
    # nx.set_edge_attributes(graph, vertex2Key, mappingVertices2)
    # nx.set_edge_attributes(graph, vertex2LabelKey, mappingVertices2Label)

    # print(df)
    # # Columns
    # nodes = graph.nodes();
    # for j in range(len(graph.nodes())):
    #   # fltr = lambda x: (x != node);
    #   # potentialNeighbors = list(filter(fltr, graph.nodes()));
    #   # idx1 = np.arange(3)
    #   # np.random.shuffle(idx1)
    #   # idx = 0
    #   # for neighbor in potentialNeighbors:
    #   for i in range(j + 1, len(graph.nodes())):
    #     # print(node, ' ', neighbor)
    #     # print(df.head())
    #     # print(idx)
    #     # print(idx1[idx])
    #     # print(labels[idx1[idx]])
    #     # if(df.ix[node, neighbor]==1):
    #     #   df.ix[node, neighbor] = labels[idx1[idx]]
    #     # print(i, ',', j)
    #     tmpX = list(df.ix[i, :])
    #     tmpY = list(df.ix[:, j])
    #     print(tmpX)
    #     print(tmpY)
    #     labelsX = [x for x in tmpX if x in ['O', 'R', 'L']]
    #     print(labelsX)
    #     labelsY = [y for y in tmpY if y in ['O', 'R', 'L']]
    #     print(labelsY)
    #     lbls = [item for item in labels if item not in labelsY and item not in labelsX]
    #     print(lbls)
    #     # idx1 = np.arange(len(lbls))
    #     # np.random.shuffle(idx1)
    #     idx = 0
    #     if (df.ix[i, j] == 1):
    #       if (len(lbls) > 0):
    #         lbl = np.random.choice(lbls)
    #         df.ix[i, j] = lbl  # lbls[idx1[idx]]
    #         mapping2[(nodes[j], nodes[i])] = lbl  # labels[idx1[idx]]
    #         idx = idx + 1
    #       else:
    #         df.ix[i, j] = '?'
    #         mapping2[( nodes[j], nodes[i])] = '?'
    #         # print(df.ix[node, :])
    #         # print(df.ix[i, :])
    # # print(df.ix[:, :])
    # print(mapping2)
    # nx.set_edge_attributes(graph, 'label2', mapping2)
    # df = nx.to_pandas_dataframe(graph)
    # print(df.ix[:,:])
    # print(df.to_string())
    return nx.Graph(graph)

    # print(df[1,:])
    # for node in graph.nodes():
    #   edges = graph.edges(node, keys=True)
    #   idx1 = np.arange(3)
    #   np.random.shuffle(idx1)
    #   idx2 = np.arange(3)
    #   np.random.shuffle(idx2)
    #   # print(idx2)
    #   mapping1 = {}
    #   mapping2 = {}
    #   for i in range(len(edges)):
    #     lbls = np.random.choice(labels, 2, replace=False)
    #     mapping1[edges[i]] = labels[idx1[i]]
    #     mapping2[edges[i]] = labels[idx2[i]]
    #   # print(mapping1)
    #   # print(mapping2)
    #   nx.set_edge_attributes(graph, 'label1', mapping1)
    #   nx.set_edge_attributes(graph, 'label2', mapping2)
    # # mapping1 = {edge: lbls for lbls = random.choice(labels, 2, replacement= False) for edge in graph.edges(keys=True)}
    # # mapping2 = {edge: random.choice(labels) for edge in graph.edges(keys=True)}
    # # print(mapping1)
    # # print(mapping2)
    #
    # # for node in graph.nodes():
    # #   neighbors = graph.neighbors(node)
    # #   for neighbor in graph.neighbors(node):
    # #     neighborLabel = random.choice(LABELS)
  logger.info("### Labels setting ended ==<")

def set_switches(graph, switches_values, logger):
  try:
  # if(type(graph)!="NoneType"):
    logger.info("### Switches setting started ==>")
    mapping = {node: np.random.choice(switches_values)for node in graph.nodes()}
    logger.info(mapping)
    nx.set_node_attributes(graph, 'sw', mapping)
    logger.info("### Switches setting ended ==<")
    return graph
  except:
    logger.error("### Graph is empty !!!!")

def simulate(graph, timesteps, observationsFolder, observationsFilename, logger):
  try:
    logger.info("### Simulation started ==>")
    observations = []
    theWalk = []
    startNode = np.random.choice(graph.nodes())
    node = startNode

    logger.info('timestep: {}'.format(str(0)))
    # observations.append(0)
    theWalk.append(0)

    logger.info('visited node: {}'.format(str(node)))
    theWalk.append(node)
    # observations.append(node)


    for timestep in range(1, timesteps):
      logger.info('timestep: {}'.format(str(timestep)))
      # observations.append(timestep)
      theWalk.append(timestep)

      switchVal = nx.get_node_attributes(graph, 'sw')[node]
      logger.info('switch setting: {}'.format(str(switchVal)))
      theWalk.append('switch: {}'.format(str(switchVal)))

      for neighbor in nx.neighbors(graph, node):
        logger.info('considered node: {}'.format(str(neighbor)))
        theWalk.append('neighbor: {}'.format(str(neighbor)))

        # print(switchVal)

        labelVal = graph[node][neighbor][node]

        # labelVal = nx.get_edge_attributes(graph, node)
        # # print(labelVal)
        # if labelVal.__contains__((node, neighbor)) :
        #   labelVal = labelVal[(node, neighbor)]
        # elif labelVal.__contains__((neighbor, node)):
        #   labelVal = labelVal[(neighbor, node)]
        # print(labelVal)
        # if graph[node][neighbor]['label1'] == graph[node]['switch']:
        if labelVal == switchVal:

          logger.info('edge label: {}'.format(str(labelVal)))
          theWalk.append('label: {}'.format(str(labelVal)))
          observations.append(labelVal)

          node = neighbor
          logger.info('visited node: {}'.format(str(node)))
          theWalk.append(node)
          # observations.append(node)
          break
    logger.info('observations: {}'.format(str(observations)))
    # print('{0}/{1}.txt'.format(observationsFolder, observationsFilename))
    with open('{0}/{1}.txt'.format(observationsFolder, observationsFilename), "w") as text_file:
      text_file.writelines('{0} '.format(str(observationsFilename)))
      text_file.writelines('{0} '.format(observations.__len__()))
      text_file.writelines('{0} '.format(observations))

    with open('{0}/{1}.pickle'.format(observationsFolder, observationsFilename), 'wb') as f:
      # Pickle the 'data' dictionary using the highest protocol available.
      pickle.dump(observations, f, pickle.HIGHEST_PROTOCOL)
    logger.info("### Simulation ended ==<")
    return observations
  except:
    logger.error("### Graph is empty !!!!")




if __name__ == "__main__":
  # np.random.seed(1234)
  fake = Factory.create()
  logsFolder='logs'
  networksFolder = 'networks'
  observationsFolder = 'observations'
  graphsFolder  = 'graphs'

  n_run = np.random.choice(range(1000000))
  timestr = time.strftime("%y%m%d-%H%M%S")
  for experiment_idx in range(EXPERIMENTS_COUNT):
    simultionName = "-".join(['sim',str(n_run), str(timestr),'exp',str(experiment_idx)])
    log = makelog('{}/{}.log'.format(logsFolder, simultionName))
    # logging.basicConfig(filename='{}.log'.format(simultionName), filemode='w', level=logging.DEBUG)
    log.info("Experiment# {}".format(experiment_idx))
    current_dim = np.random.choice(range(MIN_GRAPH_DIM, MAX_GRAPH_DIM))
    log.info("dim {}".format(current_dim))
    current_n_target_vertices = pow(current_dim, 2)
    current_timesteps_count = current_n_target_vertices
    cities = create_fake_cities(fake, 2 * current_n_target_vertices)
    graph = create_graph(cities, current_dim, log)
    compute_histogram(graph,log)
    graph = label_graph(graph, LABELS, log)
    graph = set_switches(graph, SWITCHES_VALUES, log)

    try:
      nx.write_gml(graph, '{}\{}.gml'.format(networksFolder, simultionName), stringizer=stringizer)
    except:
      print('Unable to write file {}.gml'.format(simultionName))
      log.error('Unable to write file {}.gml'.format(simultionName))

    observations = simulate(graph, current_timesteps_count, \
                            observationsFolder=observationsFolder, observationsFilename=simultionName, logger=log)
    # print(observations)
    visualize_graph(graph, graphsFolder, simultionName, log)


    # close logger
    x = logging._handlers.copy()
    for i in x:
      log.removeHandler(i)
      i.flush()
      i.close()
    logging.shutdown()






  # label_nodes(graph, cities)



  # df = nx.to_pandas_dataframe(graph)
  # print('########################## Daniel')
  # print(df)
  # pd.DataFrame.to_csv("graph.csv", sep=',')


  # print(observations)

  # mygraph = nx.read_gml("path.to.file")













