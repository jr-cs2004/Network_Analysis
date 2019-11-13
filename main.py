import networkx as nx
import matplotlib.pyplot as plt
import operator

file_name = "test.txt"
G = nx.read_edgelist(file_name, nodetype=str, data=(('weight', int),)) #reading a graph as edge listed
# G.degree()  ----  List of nodes and their degrees
degree_sequence = sorted(G.degree().items(), key=operator.itemgetter(1), reverse = True)

## draw graph in inset
plt.title("Degree rank plot")
plt.ylabel("degree")
plt.xlabel("rank")
plt.axes([0.45, 0.45, 0.45, 0.45])
Gcc = G.subgraph(sorted(nx.connected_components(G), key=len, reverse=True)[0])
pos = nx.spring_layout(Gcc)
plt.axis('off')
nx.draw_networkx_nodes(Gcc, pos, node_size=20)
nx.draw_networkx_edges(Gcc, pos, alpha=0.4)
plt.show()

#sort nodes based on their degrees and removed the top one
i = 0
print (G.number_of_nodes())
while i < (G.number_of_nodes() / 10):
  degree_sequence = sorted(G.degree().items(), key=operator.itemgetter(1), reverse = True)
  print(degree_sequence[0][1])
  G.remove_node(degree_sequence[0][0])
  i = i + 1
print (G.number_of_nodes())

