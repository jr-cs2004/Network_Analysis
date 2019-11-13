import networkx as nx
import matplotlib.pyplot as plt
import operator

file_name = "test.txt"
G = nx.read_edgelist(file_name, nodetype=str, data=(('weight', int),)) #reading a graph as edge listed
# G.degree()  ----  List of nodes and their degrees
i = 0
print (G.number_of_nodes())
while i < (G.number_of_nodes() / 10):
  degree_sequence = sorted(G.degree().items(), key=operator.itemgetter(1), reverse = True)
  print(degree_sequence[0][1])
  G.remove_node(degree_sequence[0][0])
  i = i + 1
print (G.number_of_nodes())