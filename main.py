import networkx as nx
import matplotlib.pyplot as plt
import operator
# import collections

# ########################################################################
# ########################################################################
#      Functions   START
# ########################################################################
# ########################################################################

# def get_degree_frequencies(degree_sequence):
#   print(len(degree_sequence))
#   degree_freq = {}
#   n = len(degree_sequence)
#   for i in range(0, n):
#     degree_freq[i] = 0
  
#   for d in degree_sequence:
#     degree_freq[d[1]] += 1
#   return degree_freq


def get_LCC_size(G):
  LCC = sorted(nx.connected_components(G), key=len, reverse=True)[0]
  return len(LCC)

def get_number_of_connected_component(G):
  return nx.number_connected_components(G)

def get_pairwise_connectivity(G):
  connected_components = nx.connected_components(G)
  _list = [len(c) for c in connected_components]
  pairwise_connectivity = 0
  for n in _list:
    pairwise_connectivity += n * (n - 1) / 2
  return pairwise_connectivity

def doit(G, budget, func): 
  temp_G = G.copy()
  i = 0
  _list = []  
  while i <= (budget):
    _list.append(func(temp_G))
    eigenvector_centrality = nx.eigenvector_centrality(temp_G, max_iter=1000)
    eigenvector_sequence = [(k, v) for k, v in eigenvector_centrality.items()] 
    eigenvector_sequence = sorted(eigenvector_sequence, key=lambda item: item[1], reverse=True)
    temp_G.remove_node(eigenvector_sequence[0][0])
    i = i + 1
    # print("%.0f%%" % (i / budget * 100) , end='\r', flush=True)
  return _list

def eigenvector_analysis(G, budget):
  print('          1')
  print(G.number_of_nodes())
  print(G.number_of_edges())
  LCC_Sizes = doit(G, budget, get_LCC_size)
  print('          2')
  print(G.number_of_nodes())
  print(G.number_of_edges())
  number_connected_components = doit(G, budget, get_number_of_connected_component)
  print('          3')
  print(G.number_of_nodes())
  print(G.number_of_edges())
  pairwise_connectivity = doit(G, budget, get_pairwise_connectivity)  
  print('          4')
  print(G.number_of_nodes())
  print(G.number_of_edges())
  return [LCC_Sizes, number_connected_components, pairwise_connectivity]

  # x_values = [*range(0, len(LCC_Sizes))]
  # plt.plot(x_values, LCC_Sizes, label = "degree distribution")
  # plt.xlabel('degree')
  # # Set the y axis label of the current axis.
  # plt.ylabel('frequecy')
  # # Set a title of the current axes.
  # plt.title('Two or more lines on same plot with suitable legends ')
  # # show a legend on the plot
  # plt.legend()
  # # Display a figure.
  # plt.show()
  




# ########################################################################
# ########################################################################
#      Functions   END
# ########################################################################
# ########################################################################

# file_name = ".\\Drosophila Melanogaster\\DroID\\DroID.GGIs.txt"
# file_name = "test.txt"
# G = nx.read_edgelist(file_name, nodetype=str, data=(('weight', int),)) #reading a graph as edge listed
# G.degree()  ----  List of nodes and their degrees

G = nx.Graph()
G.add_node('1')
G.add_node('2')
G.add_node('3')
G.add_node('4')
G.add_node('5')
G.add_node('6')
G.add_node('7')
G.add_node('8')
G.add_node('9')
G.add_node('10')
G.add_node('11')
G.add_node('12')
G.add_node('13')
G.add_node('14')
G.add_node('15')

G.add_edge('1', '2')
G.add_edge('1', '3')
G.add_edge('1', '4')
G.add_edge('1', '5')
G.add_edge('1', '6')

G.add_edge('7', '8')
G.add_edge('7', '9')
G.add_edge('7', '10')
G.add_edge('7', '11')

G.add_edge('12', '13')
G.add_edge('12', '14')
G.add_edge('12', '15')


print(G.number_of_nodes())
print(G.number_of_edges())

_list = eigenvector_analysis(G, 5)
print(_list)
exit()


# ########################################################################
# ########################################################################
#### Degree distribution plot

# degree_freq = nx.degree_histogram(G)
# degree_freq = degree_freq[1:]
# x_values = [*range(1, len(degree_freq) + 1)]

# print(len(degree_freq), len(x_values))

# plt.plot(x_values, degree_freq, label = "degree distribution")
# plt.xlabel('degree')
# # Set the y axis label of the current axis.
# plt.ylabel('frequecy')
# # Set a title of the current axes.
# plt.title('Two or more lines on same plot with suitable legends ')
# # show a legend on the plot
# plt.legend()
# # Display a figure.
# plt.show()



#sort nodes based on their degrees and removed the top one
i = 0

LCC_Sizes = []
LCC = sorted(nx.connected_components(G), key=len, reverse=True)[0]
LCC_Sizes.append(len(LCC))

while i < (G.number_of_nodes() / 10):
  degree_sequence = sorted(G.degree, key=lambda x: x[1], reverse=True)
  LCC = sorted(nx.connected_components(G), key=len, reverse=True)[0]
  LCC_Sizes.append(len(LCC))
  G.remove_node(degree_sequence[0][0])
  i = i + 1
print (G.number_of_nodes())

x_values = [*range(0, len(LCC_Sizes))]
plt.plot(x_values, LCC_Sizes, label = "degree distribution")
plt.xlabel('degree')
# Set the y axis label of the current axis.
plt.ylabel('frequecy')
# Set a title of the current axes.
plt.title('Two or more lines on same plot with suitable legends ')
# show a legend on the plot
plt.legend()
# Display a figure.
plt.show()


# ########################################################################
# ########################################################################
#      Commented Codes  START
# ########################################################################
# ########################################################################

######## draw graph in inset
# plt.title("Degree rank plot")
# plt.ylabel("degree")
# plt.xlabel("rank")
# plt.axes([0.45, 0.45, 0.45, 0.45])
# # Gcc = G.subgraph(sorted(nx.connected_components(G), key=len, reverse=True)[0])
# pos = nx.spring_layout(G)
# plt.axis('off')
# nx.draw_networkx_nodes(G, pos, node_size=20)
# nx.draw_networkx_edges(G, pos, alpha=0.4)
# plt.show()

# ########################################################################
# ########################################################################
#      Commented Codes  END
# ########################################################################
# ########################################################################