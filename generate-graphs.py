import networkx as nx
from networkx.utils import uniform_sequence
import matplotlib.pyplot as plt
from faker import Factory
import random
import logging
import numpy as np
import pandas as pd

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
TARGET_VERTICES_COUNT = pow(GRAPH_DIM, 2)
LABELS = ['L', 'O', 'R' ]
SWITCHES_VALUES = ['R', 'L']


def create_fake_cities(fake, count):
  """"""
  cities = []
  # for i in range(count):
  #   cities.append(fake.city())

  cities = [fake.city() for i in range(count)]

  return cities

def compute_histogram(graph):
  degree_sequence = list(nx.degree(graph).values())  # degree sequence
  print("Degree sequence %s" % degree_sequence)
  print("Degree histogram")
  hist = {}
  for d in degree_sequence:
    if d in hist:
      hist[d] += 1
    else:
      hist[d] = 1
  print("degree #nodes")
  for d in hist:
    print('%d %d' % (d, hist[d]))

def visualize_graph(graph):
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
  plt.show()

def generate_graph(labels):
  G = nx.grid_graph([GRAPH_DIM, GRAPH_DIM])

  # G = nx.Graph()
  # print(cities)
  # print(cities[:targetVerticesCount])
  # G.add_nodes_from(cities[:targetVerticesCount])
  # graphNodes = G.nodes();
  # print(graphNodes)
  # for node in G.nodes():
  #   fltr = lambda x: (x != node) ;
  #   potentialNeighbors = list(filter(fltr, G.nodes()));
  #   for neighbor in potentialNeighbors:
  #     G.add_edge(node, neighbor)

  nodeToAdd_idx = TARGET_VERTICES_COUNT + 1
  nodeToAdd = len(G.nodes())
  nodesToRemove = [];
  nodesToModify = [];
  nodesToDuplicateN = 0;
  for node in G.nodes():
    if (G.degree(node) == 2):
      nodesToRemove.append(node);
    elif (G.degree(node) == 4):
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
  print('number of nodes to remove', len(nodesToRemove))
  print('number of nodes to duplicate ', nodesToDuplicateN)
  print('number of nodes untouched', TARGET_VERTICES_COUNT - len(nodesToRemove) - nodesToDuplicateN)
  print('number of resulting nodes in new graph ',
        TARGET_VERTICES_COUNT - len(nodesToRemove) - nodesToDuplicateN + 2 * nodesToDuplicateN)
  G.remove_nodes_from(nodesToRemove)
  mapping = {G.nodes()[i]: labels[i] for i in range(len(G.nodes())) for label in labels}
  graph = nx.relabel_nodes(G, mapping, copy=True)
  return graph

def label_nodes(graph, labels):
  mapping = {graph.nodes()[i]: labels[i] for i in range(len(graph.nodes())) for label in labels}
  # graph = nx.relabel_nodes(graph, mapping, copy=False)
  # print(dic)
  # nx.set_node_attributes(graph, 'label', dic)

def label_graph(graph, labels):
  assert all(x == 3 for x in list(nx.degree(graph).values()))
  # mapping = {(edge[0], edge[1], edge): random.choice(labels) for edge in graph.edges(keys=True)}
  df = nx.to_pandas_dataframe(graph)
  print(type(df))
  mapping1 = {}
  mapping2 = {}
  # for node in graph.nodes():

  # Row
  nodes = graph.nodes();
  for i in range(len(graph.nodes())):
    # fltr = lambda x: (x != node);
    # potentialNeighbors = list(filter(fltr, graph.nodes()));
    # idx1 = np.arange(3)
    # np.random.shuffle(idx1)
    # idx = 0
    # for neighbor in potentialNeighbors:
    for j in range(i+1, len(graph.nodes())):
      # print(node, ' ', neighbor)
      # print(df.head())
      # print(idx)
      # print(idx1[idx])
      # print(labels[idx1[idx]])
      # if(df.ix[node, neighbor]==1):
      #   df.ix[node, neighbor] = labels[idx1[idx]]
      # print(i, ',', j)
      tmpX = list(df.ix[i,:])
      tmpY = list(df.ix[:,j])
      print(tmpX)
      print(tmpY)
      labelsX = [x for x in tmpX if x in ['O', 'R', 'L']]
      print(labelsX)
      labelsY = [y for y in tmpY if y in ['O', 'R', 'L']]
      print(labelsY)
      lbls = [item for item in labels if item not in labelsY and item not in labelsX]
      print(lbls)
      # idx1 = np.arange(len(lbls))
      # np.random.shuffle(idx1)
      idx = 0
      if (df.ix[i, j] == 1):
        if(len(lbls)>0):
          lbl = np.random.choice(lbls)
          df.ix[i, j] = lbl #lbls[idx1[idx]]
          mapping1[(nodes[i], nodes[j])] = lbl  #labels[idx1[idx]]
          idx = idx + 1
        else:
          df.ix[i, j] = '?'
          mapping1[(nodes[i], nodes[j])] = '?'
    # print(df.ix[node, :])
    # print(df.ix[i, :])
  # print(df.ix[:, :])
  print(mapping1)
  nx.set_edge_attributes(graph, 'label1', mapping1)

  # Columns
  nodes = graph.nodes();
  for j in range(len(graph.nodes())):
    # fltr = lambda x: (x != node);
    # potentialNeighbors = list(filter(fltr, graph.nodes()));
    # idx1 = np.arange(3)
    # np.random.shuffle(idx1)
    # idx = 0
    # for neighbor in potentialNeighbors:
    for i in range(j + 1, len(graph.nodes())):
      # print(node, ' ', neighbor)
      # print(df.head())
      # print(idx)
      # print(idx1[idx])
      # print(labels[idx1[idx]])
      # if(df.ix[node, neighbor]==1):
      #   df.ix[node, neighbor] = labels[idx1[idx]]
      # print(i, ',', j)
      tmpX = list(df.ix[i, :])
      tmpY = list(df.ix[:, j])
      print(tmpX)
      print(tmpY)
      labelsX = [x for x in tmpX if x in ['O', 'R', 'L']]
      print(labelsX)
      labelsY = [y for y in tmpY if y in ['O', 'R', 'L']]
      print(labelsY)
      lbls = [item for item in labels if item not in labelsY and item not in labelsX]
      print(lbls)
      # idx1 = np.arange(len(lbls))
      # np.random.shuffle(idx1)
      idx = 0
      if (df.ix[i, j] == 1):
        if (len(lbls) > 0):
          lbl = np.random.choice(lbls)
          df.ix[i, j] = lbl  # lbls[idx1[idx]]
          mapping2[(nodes[j], nodes[i])] = lbl  # labels[idx1[idx]]
          idx = idx + 1
        else:
          df.ix[i, j] = '?'
          mapping2[( nodes[j], nodes[i])] = '?'
          # print(df.ix[node, :])
          # print(df.ix[i, :])
  # print(df.ix[:, :])
  print(mapping2)
  nx.set_edge_attributes(graph, 'label2', mapping2)

  print(df.ix[:,:])
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

def set_switches(graph, switches_values):
  mapping = {node: np.random.choice(switches_values)for node in graph.nodes()}
  print(mapping)
  nx.set_node_attributes(graph, 'switch', mapping)
  return graph

def simulate(graph, timesteps):
  observations = []
  startNode = np.random.choice(graph.nodes())
  node = startNode
  observations.append(node)
  for timestep in range(timesteps):
    print('timestep: ', timestep)
    observations.append(timestep)
    for neighbor in nx.neighbors(graph, node):
      switchVal = nx.get_node_attributes(graph, 'switch')[node]
      # print(switchVal)
      labelVal = nx.get_edge_attributes(graph, 'label1')
      # print(labelVal)
      if labelVal.__contains__((node, neighbor)) :
        labelVal = labelVal[(node, neighbor)]
      else:
        labelVal = labelVal[(neighbor, node)]
      print(labelVal)
      # if graph[node][neighbor]['label1'] == graph[node]['switch']:
      if labelVal == switchVal:
        observations.append(labelVal)
        node = neighbor
        print(node)
        observations.append(node)
        break
  return observations



if __name__ == "__main__":
  logging.basicConfig(filename='run.log', filemode='w', level=logging.DEBUG)
  fake = Factory.create()
  cities = create_fake_cities(fake, 2 * TARGET_VERTICES_COUNT)

  graph = generate_graph(cities)
  multiGraph = graph
  # multiGraph = nx.MultiGraph(graph)
  # compute_histogram(multiGraph)
  # print(graph.nodes())
  # label_nodes(multiGraph, cities)
  multiGraph = label_graph(multiGraph, LABELS)
  multiGraph = set_switches(multiGraph, SWITCHES_VALUES)

  nx.write_gml(multiGraph, "graph.gml")
  df = nx.to_pandas_dataframe(multiGraph)
  print('########################## Daniel')
  print(df)
  # pd.DataFrame.to_csv("graph.csv", sep=',')

  observations = simulate(multiGraph, 10)
  print(observations)
  visualize_graph(multiGraph)
  # am = nx.adjacency_matrix(multiGraph)
  # print("am")
  # print(am)
  # sm = nx.to_scipy_sparse_matrix(multiGraph)
  # print("sm")
  # print(sm)





  nx.write_gml(multiGraph, "graph.gml")
  # mygraph = nx.read_gml("path.to.file")













  # for node in G.nodes():
  #   logging.info(" node: {0}, deg: {1}".format(node, G.degree(node)));
  #   for edge_idx in range(maxEdgesPerVertex - len(G.neighbors(node))):
  #     # print(G.degree(node))
  #     fltr = lambda x: (x != node) and (x not in G.neighbors(node)) and (G.degree(x) < maxEdgesPerVertex);
  #     potentialNeighbors = list(filter(  fltr ,G.nodes()));
  #     neighbor = random.choice(potentialNeighbors);
  #     logging.info(" deg: {0}, pneighbors: {1}, neightbor: {2}. Added e# {3}".format(G.degree(node), potentialNeighbors, neighbor, edge_idx));
  #     G.add_edge(node, neighbor)
  #     # logging.info(" added e# {3}".format(edge_idx, node, neighbor));
  #
  #     # if len(G.neighbors(node))<4 :
  #   logging.info(G.degree());
  #   logging.info(" ");
  # visualize_graph(G)







# degree = 3
# n = 100
# print(uniform_sequence(5))
# seq=nx.utils.create_degree_sequence(10,uniform_sequence, max_tries=100, 3)
# # z=nx.utils.create_degree_sequence([3, 3, 3, 3, 3])
# G=nx.configuration_model(seq)
# G=nx.Graph(G)

# z=[3,3, 3, 3]
# print(nx.is_valid_degree_sequence(z))
#
# print("Configuration model")
# G=nx.configuration_model(z)  # configuration model