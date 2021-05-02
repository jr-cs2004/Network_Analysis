import networkx as nx


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
    _removing_nodes_centrality = []
    print(centrality, ': ')
    centrality_dictionary = get_centrality(temp_G, centrality)
    centrality_sequence = [(k, v) for k, v in centrality_dictionary.items()]
    centrality_sequence = sorted(centrality_sequence, key=lambda item: item[1], reverse=True)
    while i < (budget):
        # print(centrality_sequence)
        _removing_nodes.append(centrality_sequence[i][0])
        if (centrality != 'degree'):
            _removing_nodes_centrality.append(centrality_sequence[i][1])
        else: 
            _removing_nodes_centrality.append(G.degree[centrality_sequence[i][0]])

        temp_G.remove_node(centrality_sequence[i][0])
        _list['largest_connected_component_size'].append(get_LCC_size(temp_G))
        _list['number_of_connected_components'].append(get_number_of_connected_components(temp_G))
        _list['pairwise_connectivity'].append(get_pairwise_connectivity(temp_G))
        print("%.0f%%" % (i / budget * 100) , end='\r')
        i = i + 1
        if (i % 50 == 0):
            print(_list['largest_connected_component_size'][i-1])

    i = 0
    removing_nodes_file = open('.\\Saccharomyces cerevisiae\\DIP\\output\\global_centrality_analysis\\removed_nodes_based_on_' + centrality + '_centrality.budget_' + str(budget) + '.txt', 'w')
    # removing_nodes_file = open('.\\Escherichia coli\\DIP\\output\\global_centrality_analysis\\removed_nodes_based_on_' + centrality + '_centrality.budget_' + str(budget) + '.txt', 'w')
    removing_nodes_file.write('nodes\tcentrality_value\tlargest_connected_component_size\tnumber_of_connected_components\tpairwise_connectivity\n')
    while i < (budget):
        removing_nodes_file.write(_removing_nodes[i] + '\t' + str(_removing_nodes_centrality[i]) + '\t' +
                            str(_list['largest_connected_component_size'][i]) + '\t' +
                            str( _list['number_of_connected_components'][i]) + '\t' +
                            str(_list['pairwise_connectivity'][i]) + '\n')
        i += 1
    removing_nodes_file.close()
    return _list

def centrality_analysis(G, budget):
    analysis = {}
    centrality_list = ['degree', 'betweenness', 'closeness', 'eigenvector']
    for centrality in centrality_list:
        analysis[centrality] = get_alalysis(G, budget, centrality)
    return analysis



 
# ########################################################################
# ########################################################################
#      Functions   END
# ########################################################################
# ########################################################################



original_PPIs_file_name = ".\\Saccharomyces cerevisiae\\DIP\\output\\original_PPIs_redundancies_N_self_loops_removed_N_Connected.txt"
# original_PPIs_file_name = ".\\Escherichia coli\\DIP\\output\\original_PPIs_redundancies_N_self_loops_removed_N_Connected.txt"
G = nx.read_edgelist(original_PPIs_file_name, nodetype=str, data=(('weight', int),)) #reading a graph as edge listed
print(G.number_of_nodes())
print(G.number_of_edges())
_result = centrality_analysis(G, 950)
