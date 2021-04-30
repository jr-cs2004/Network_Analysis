import networkx as nx
import matplotlib.pyplot as plt
import operator
# import collections

### for saving a plot as figure
import matplotlib as mpl
mpl.use("pgf")
plt.rcParams.update({
    "text.usetex": True,     # use inline math for ticks
    "pgf.rcfonts": False,    # don't setup fonts from rc parameters
    "pgf.preamble": "\n".join([
         "\\usepackage{units}",          # load additional packages
         "\\usepackage{metalogo}",
         "\\usepackage{unicode-math}"   # unicode math setup
    ])
})
# ########################################################################
# ########################################################################
#      Functions   START
# ########################################################################
# ########################################################################

def get_LCC_size(G):
  LCC = sorted(nx.connected_components(G), key=len, reverse=True)[0]
  return len(LCC)

def get_number_of_connected_components(G):
  return nx.number_connected_components(G)

def get_pairwise_connectivity(G):
  connected_components = nx.connected_components(G)
  _list = [len(c) for c in connected_components]
  pairwise_connectivity = 0
  for n in _list:
    pairwise_connectivity += n * (n - 1) / 2
  return pairwise_connectivity

def get_centrality(G, centrality):
  if (centrality == 'degree'):
    return nx.degree_centrality(G)
  if (centrality == 'betweenness'):
    return nx.betweenness_centrality(G)
  if (centrality == 'closeness'):
    return nx.closeness_centrality(G)
  if (centrality == 'eigenvector'):
    return nx.eigenvector_centrality(G, max_iter=5000)

def get_alalysis(G, budget, centrality): 
  temp_G = G.copy()
  i = 0
  _list = {}
  _list['largest_connected_component_size'] = []
  _list['number_of_connected_components'] = []
  _list['pairwise_connectivity'] = []
  _removing_nodes = []
  print(centrality, ': ')
  while i < (budget):
    _list['largest_connected_component_size'].append(get_LCC_size(temp_G))
    _list['number_of_connected_components'].append(get_number_of_connected_components(temp_G))
    _list['pairwise_connectivity'].append(get_pairwise_connectivity(temp_G))
    centrality_dictionary = get_centrality(temp_G, centrality)
    centrality_sequence = [(k, v) for k, v in centrality_dictionary.items()] 
    centrality_sequence = sorted(centrality_sequence, key=lambda item: item[1], reverse=True)    
    _removing_nodes.append(centrality_sequence[0][0])
    temp_G.remove_node(centrality_sequence[0][0])
    print("%.0f%%" % (i / budget * 100) , end='\r')
    i = i + 1

  i = 0
  removing_nodes_file = open('removed_nodes_based_on_' + centrality + '.Centrality_budget.' + str(budget) + '.txt', 'w')
  removing_nodes_file.write('nodes\tlargest_connected_component_size\tnumber_of_connected_components\tpairwise_connectivity\n')
  for i in range(0, budget):
    removing_nodes_file.write(_removing_nodes[i] + '\t' + 
                              str(_list['largest_connected_component_size'][i]) + '\t' +
                              str( _list['number_of_connected_components'][i]) + '\t' + 
                              str(_list['pairwise_connectivity'][i]) + '\n')
  removing_nodes_file.close()
  return _list

def centrality_analysis(G, budget):
  analysis = {}
  centrality_list = ['degree', 'betweenness', 'closeness', 'eigenvector'] # 
  for centrality in centrality_list:
    analysis[centrality] = get_alalysis(G, budget, centrality)
  return analysis

def _plot(result):
  for item in result.items():
    x_values = [*range(0, len(item[1]['largest_connected_component_size']))]
    plt.plot(x_values, item[1]['largest_connected_component_size'], label = item[0])
    plt.xlabel('number of removed nodes')
    plt.ylabel('largest connected component size')
    plt.title('')
    plt.legend()
    # plt.show()
    plt.savefig("largest_connected_component_size.png")
  plt.clf() 
  for item in result.items():
    x_values = [*range(0, len(item[1]['number_of_connected_components']))]
    plt.plot(x_values, item[1]['number_of_connected_components'], label = item[0])
    plt.xlabel('number of removed nodes')
    plt.ylabel('number of connected components')
    plt.title('')
    plt.legend()
    # plt.show()
    plt.savefig("number_of_connected_components.png")
  plt.clf() 
  for item in result.items():
    x_values = [*range(0, len(item[1]['pairwise_connectivity']))]
    plt.plot(x_values, item[1]['pairwise_connectivity'], label = item[0])
    plt.xlabel('number of removed nodes')
    plt.ylabel('pairwise connectivity')
    plt.title('')
    plt.legend()
    # plt.show()
    plt.savefig("pairwise_connectivity.png")
    

 
# ########################################################################
# ########################################################################
#      Functions   END
# ########################################################################
# ########################################################################

file_name = ".\\Saccharomyces cerevisiae\\DIP\\output\\original_PPIs_redundancies_N_self_loops_removed_N_Connected.txt"
# file_name = "test.txt"
G = nx.read_edgelist(file_name, nodetype=str, data=(('weight', int),)) #reading a graph as edge listed
print(G.number_of_nodes())
print(G.number_of_edges())
_result = centrality_analysis(G, 1200)
print(_result)
_plot(_result)

# ########################################################################
# ########################################################################
#      Commented Codes  START
# ########################################################################
# ########################################################################

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
#### Simple Graph
# G = nx.Graph()
# G.add_node('1')
# G.add_node('2')
# G.add_node('3')
# G.add_node('4')
# G.add_node('5')
# G.add_node('6')
# G.add_node('7')
# G.add_node('8')
# G.add_node('9')
# G.add_node('10')
# G.add_node('11')
# G.add_node('12')
# G.add_node('13')
# G.add_node('14')
# G.add_node('15')

# G.add_edge('1', '2')
# G.add_edge('1', '3')
# G.add_edge('1', '4')
# G.add_edge('1', '5')
# G.add_edge('1', '6')

# G.add_edge('7', '8')
# G.add_edge('7', '9')
# G.add_edge('7', '10')
# G.add_edge('7', '11')

# G.add_edge('12', '13')
# G.add_edge('12', '14')
# G.add_edge('12', '15')


# ########################################################################
# ########################################################################
#### Degree distribution plot

# degree_freq = nx.degree_histogram(G)
# degree_freq = degree_freq[1:]
# x_values = [*range(1, len(degree_freq) + 1)]
# print(len(degree_freq), len(x_values))
# plt.plot(x_values, degree_freq, label = "degree distribution")
# plt.xlabel('degree')
# plt.ylabel('frequecy')
# plt.title('Two or more lines on same plot with suitable legends ')
# plt.legend()
# plt.show()

# ########################################################################
# ########################################################################
####  plot result - multiple subfigure
# def _plot(result):
#   fig = plt.figure()
#   axs = [plt.subplot2grid((2, 4), (0, 0), colspan=2), plt.subplot2grid((2, 4), (0, 2), colspan=2), plt.subplot2grid((2, 4), (1, 1), colspan=2)]
#   for item in result.items():
#     x_values = [*range(0, len(item[1]['largest_connected_component_size']))]

#     axs[0].plot(x_values, item[1]['largest_connected_component_size'], label = item[0])
#     axs[1].plot(x_values, item[1]['number_of_connected_components'], label = item[0])
#     axs[2].plot(x_values, item[1]['pairwise_connectivity'], label = item[0])

#   plt.xlabel('test')
#   axs[0].set_ylabel('largest_connected_component_size')
#   axs[1].set_ylabel('number_of_connected_components')
#   axs[2].set_ylabel('pairwise_connectivity')
#   plt.title('')
#   plt.legend()
#   plt.tight_layout(0.5)
#   plt.show()
#   plt.savefig("pgf_preamble.png")


# ########################################################################
# ########################################################################
#      Commented Codes  END
# ########################################################################
# ########################################################################