import networkx as nx

def get_essential_proteins_info():
    Essentiality_File = open(".\\Escherichia coli\\DIP\\output\\DIP_IDs_N_Essentiality.txt", "r") 
    # Essentiality_File = open(".\\Saccharomyces cerevisiae\\DIP\\output\\DIP_IDs_N_Essentiality.txt", "r") 
    _IDs = []
    _Essentiality = []
    essential_IDs = []
    unknown_essential_IDs = []
    for line in Essentiality_File:
        _IDs.append(line.split()[0])
        _Essentiality.append(line.split()[1])

    n = len(_IDs)
    for i in range(0, n):
        if (_Essentiality[i] == 'E'):
            essential_IDs.append(_IDs[i])
        if (_Essentiality[i] == 'U'):
            unknown_essential_IDs.append(_IDs[i])

    print(len(_IDs))
    print(len(essential_IDs))
    print(len(unknown_essential_IDs))
    print('###################')


    ###############################################################
    ###############################################################
    file_name = ".\\Escherichia coli\\DIP\\output\\original_PPIs_redundancies_N_self_loops_removed_N_Connected.txt"
    network_file = open(file_name, 'r')
    _______proteins_ID = []
    for line in network_file:
        _______proteins_ID.append(line.split()[0])
        _______proteins_ID.append(line.split()[1])
    

    print('net: ' ,len(_______proteins_ID))
    print('net proteins: ', len(list(set(_______proteins_ID))))
    _lst = [value for value in _______proteins_ID if value in essential_IDs]
    print(len(list(set(_lst))))
    ###############################################################
    ###############################################################


    return [_IDs, _Essentiality, essential_IDs, unknown_essential_IDs]

def get_centrality(G, centrality):
    if (centrality == 'degree'):
        return nx.degree_centrality(G)
    if (centrality == 'betweenness'):
        return nx.betweenness_centrality(G)
    if (centrality == 'closeness'):
        return nx.closeness_centrality(G)
    if (centrality == 'eigenvector'):
        return nx.eigenvector_centrality(G, max_iter=5000)

def get_critical_node_centrality(G, critical_nodes, centrality, centrality_dictionary): 
    critical_node_centrality = {}
    if (centrality != 'degree'):
        for node in critical_nodes:        
            critical_node_centrality[node] = centrality_dictionary[node]
    else:
        for node in critical_nodes:        
            critical_node_centrality[node] = G.degree[node]
    return critical_node_centrality

def centrality_analysis(G):
    analysis = {}
    centrality_list = ['degree'] # , 'betweenness', 'closeness', 'eigenvector'
    for centrality in centrality_list:
        analysis[centrality] = get_alalysis(G, centrality)
    return analysis

def get_alalysis(G, centrality): 
    print('##################################')
    print('##################################')
    print(centrality)
    centrality_based_nodes_file = open(".\\Escherichia coli\\DIP\\output\\global_centrality_analysis\\removed_nodes_based_on_" + centrality + "_centrality.budget_2000.txt", "r") 
    # centrality_based_nodes_file = open(".\\Saccharomyces cerevisiae\\DIP\\output\\global_centrality_analysis\\removed_nodes_based_on_" + centrality + "_centrality.budget_950.txt", "r") 
    
    centrality_dictionary = get_centrality(G, centrality)

    centrality_based_nodes = []
    centrality_based_nodes_centrality = {}
    _index = 0
    for line in centrality_based_nodes_file:
        if (_index >= 1): # for the header
            centrality_based_nodes.append(line.split('\t')[0])
            centrality_based_nodes_centrality[line.split('\t')[0]] = line.split('\t')[1]
        _index += 1
      
    essential_proteins_info = get_essential_proteins_info() # [_IDs, _Essentiality, essential_IDs, unknown_essential_IDs]    
    proteins_ID = essential_proteins_info[0]
    proteins_Essentiality = essential_proteins_info[1]
    essential_proteins_ID = essential_proteins_info[2]
    print('number of Essential IDs: ', len(essential_proteins_ID))
    print('number of Essential IDs (Unique): ', len(list(set(essential_proteins_ID))))
    unknown_essential_proteins_ID = essential_proteins_info[3]

    for i in range(50, 2500, 50): # for i in range(50, 951, 50):
        centrality_based_nodes_N_essentials = [value for value in centrality_based_nodes[0:i+1] if value in essential_proteins_ID]
        centrality_based_nodes_N_unknown_essentials = [value for value in centrality_based_nodes[0:i+1] if value in unknown_essential_proteins_ID]
        print('Number of nodes:\t', i)
        print('centrality_based_nodes_N_essentials:\t', len(centrality_based_nodes_N_essentials), '\t', round(len(centrality_based_nodes_N_essentials) / i, 2))
        # print('centrality_based_nodes_N_unknown_essentials:\t', len(centrality_based_nodes_N_unknown_essentials))
        print('\n\n')


file_name = ".\\Escherichia coli\\DIP\\output\\original_PPIs_redundancies_N_self_loops_removed_N_Connected.txt"
# file_name = ".\\Saccharomyces cerevisiae\\DIP\\output\\original_PPIs_redundancies_N_self_loops_removed_N_Connected.txt"
G = nx.read_edgelist(file_name, nodetype=str, data=(('weight', int),)) #reading a graph as edge listed
centrality_analysis(G)
