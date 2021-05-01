import networkx as nx

def get_essential_proteins_info():
    Essentiality_File = open("E:\\Javad Rezaei\\Second Paper\\Network_Analysis\\Escherichia coli\\DIP\\output\\DIP_IDs_N_Essentiality.txt", "r") 
    # Essentiality_File = open("E:\\Javad Rezaei\\Second Paper\\Network_Analysis\\Saccharomyces cerevisiae\\DIP\\output\\DIP_IDs_N_Essentiality.txt", "r") 
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
    print('###################')
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
    centrality_list = ['degree', 'betweenness', 'closeness', 'eigenvector'] # 
    for centrality in centrality_list:
        analysis[centrality] = get_alalysis(G, centrality)
    return analysis

def get_alalysis(G, centrality): 
    print('############')
    print(centrality)
    centrality_based_nodes_file = open(".\\Escherichia coli\\DIP\\output\\global_centrality_analysis\\removed_nodes_based_on_" + centrality + "_centrality.budget_400.txt", "r") 
    # centrality_based_nodes_file = open(".\\Saccharomyces cerevisiae\\DIP\\output\\global_centrality_analysis\\removed_nodes_based_on_" + centrality + "_centrality.budget_950.txt", "r") 
    centrality_based_nodes = []
    centrality_based_nodes_centrality = {}
    _index = 0
    for line in centrality_based_nodes_file:
        if (_index >= 1): # for the header
            centrality_based_nodes.append(line.split('\t')[0])
            centrality_based_nodes_centrality[line.split('\t')[0]] = line.split('\t')[1]
        _index += 1
  
    centrality_dictionary = get_centrality(G, centrality)

    essential_proteins_info = get_essential_proteins_info() # [_IDs, _Essentiality, essential_IDs, unknown_essential_IDs]    
    proteins_ID = essential_proteins_info[0]
    proteins_Essentiality = essential_proteins_info[1]
    essential_proteins_ID = essential_proteins_info[2]
    unknown_essential_proteins_ID = essential_proteins_info[3]

    for i in range(50, 401, 50): # for i in range(50, 951, 50):
        GA_critical_nodes_file = open("E:\\Javad Rezaei\\Second Paper\\Boost\\Boost\\E.coli\\Result\\critical.nodes.found.by.GA." + str(i) + ".txt", "r") 
        # GA_critical_nodes_file = open("E:\\Javad Rezaei\\Second Paper\\Boost\\Boost\\S.cerevisiae\\Result\\critical.nodes.found.by.GA." + str(i) + ".txt", "r") 
        critical_nodes = []
        _index = 0
        for line in GA_critical_nodes_file:
            if (_index >= 2): # for the header
                critical_nodes.append(line.split()[1])
            _index += 1        
        critical_node_centrality = get_critical_node_centrality(G, critical_nodes, centrality, centrality_dictionary)  

        
        critical_nodes_N_essentials = [value for value in critical_nodes if value in essential_proteins_ID]
        critical_nodes_N_unknown_essentials = [value for value in critical_nodes if value in unknown_essential_proteins_ID]

        centrality_based_nodes_N_essentials = [value for value in centrality_based_nodes if value in essential_proteins_ID]
        centrality_based_nodes_N_unknown_essentials = [value for value in centrality_based_nodes if value in unknown_essential_proteins_ID]
        print('Number of nodes:\t', i)
        print('critical_nodes_N_essentials:\t', len(critical_nodes_N_essentials))
        print('critical_nodes_N_unknown_essentials:\t', len(critical_nodes_N_unknown_essentials))
        print('centrality_based_nodes_N_essentials:\t', len(centrality_based_nodes_N_essentials))
        print('centrality_based_nodes_N_unknown_essentials:\t', len(centrality_based_nodes_N_unknown_essentials))
        _lst = [value for value in centrality_based_nodes_N_essentials if value in critical_nodes_N_essentials]
        print(len(_lst))
        print('\n\n')


file_name = ".\\Escherichia coli\\DIP\\output\\original_PPIs_redundancies_N_self_loops_removed_N_Connected.txt"
# file_name = ".\\Saccharomyces cerevisiae\\DIP\\output\\original_PPIs_redundancies_N_self_loops_removed_N_Connected.txt"
G = nx.read_edgelist(file_name, nodetype=str, data=(('weight', int),)) #reading a graph as edge listed
centrality_analysis(G)
