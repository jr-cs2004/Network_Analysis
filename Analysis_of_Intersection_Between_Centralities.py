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
    return [_IDs, _Essentiality, essential_IDs, unknown_essential_IDs]

def centrality_analysis():
    analysis = {}
    centrality_list = ['degree', 'betweenness', 'closeness', 'eigenvector'] #
    i = 0
    j = 0 
    for centrality_1 in centrality_list:
        j = 0
        for centrality_2 in centrality_list:
            if (j > i):
                get_alalysis(centrality_1, centrality_2)
            j += 1
        i += 1

def get_alalysis(centrality_1, centrality_2): 
    print('##################################')
    print('##################################')
    print(centrality_1 + ' vs ' + centrality_2)
    centrality_based_nodes_file_1 = open(".\\Escherichia coli\\DIP\\output\\global_centrality_analysis\\removed_nodes_based_on_" + centrality_1 + "_centrality.budget_400.txt", "r") 
    centrality_based_nodes_file_2 = open(".\\Escherichia coli\\DIP\\output\\global_centrality_analysis\\removed_nodes_based_on_" + centrality_2 + "_centrality.budget_400.txt", "r") 
    # centrality_based_nodes_file = open(".\\Saccharomyces cerevisiae\\DIP\\output\\global_centrality_analysis\\removed_nodes_based_on_" + centrality + "_centrality.budget_950.txt", "r") 
    

    centrality_based_nodes_1 = []
    centrality_based_nodes_centrality_1 = {}
    _index = 0
    for line in centrality_based_nodes_file_1:
        if (_index >= 1): # for the header
            centrality_based_nodes_1.append(line.split('\t')[0])
            centrality_based_nodes_centrality_1[line.split('\t')[0]] = line.split('\t')[1]
        _index += 1
  
    centrality_based_nodes_2 = []
    centrality_based_nodes_centrality_2 = {}
    _index = 0
    for line in centrality_based_nodes_file_2:
        if (_index >= 1): # for the header
            centrality_based_nodes_2.append(line.split('\t')[0])
            centrality_based_nodes_centrality_2[line.split('\t')[0]] = line.split('\t')[1]
        _index += 1

    essential_proteins_info = get_essential_proteins_info() # [_IDs, _Essentiality, essential_IDs, unknown_essential_IDs]    
    proteins_ID = essential_proteins_info[0]
    proteins_Essentiality = essential_proteins_info[1]
    essential_proteins_ID = essential_proteins_info[2]
    unknown_essential_proteins_ID = essential_proteins_info[3]

    for i in range(50, 401, 50): # for i in range(50, 951, 50):
        GA_critical_nodes_file = open(".\\Escherichia coli\\DIP\\output\\Boost\\Result\\critical.nodes.found.by.GA." + str(i) + ".txt", "r") 
        # GA_critical_nodes_file = open(".\\Saccharomyces cerevisiae\\DIP\\output\\Boost\\Result\\critical.nodes.found.by.GA." + str(i) + ".txt", "r") 
        critical_nodes = []
        _index = 0
        for line in GA_critical_nodes_file:
            if (_index >= 2): # for the header
                critical_nodes.append(line.split()[1])
            _index += 1        

        critical_nodes_N_centrality_1 = [value for value in critical_nodes if value in centrality_based_nodes_1[0:i]]
        critical_nodes_N_centrality_2 = [value for value in critical_nodes if value in centrality_based_nodes_2[0:i]]
        centrality_1_N_centrality_2 = [value for value in centrality_based_nodes_2[0:i] if value in centrality_based_nodes_1[0:i]]

        critical_nodes_N_centrality_1_N_Essential = [value for value in critical_nodes_N_centrality_1 if value in essential_proteins_ID]
        critical_nodes_N_centrality_2_N_Essential = [value for value in critical_nodes_N_centrality_2 if value in essential_proteins_ID]
        centrality_1_N_centrality_2_N_Essential = [value for value in centrality_1_N_centrality_2 if value in essential_proteins_ID]

        print('Number of nodes:\t', i)
        print('critical_nodes_N_centrality_1:\t', len(critical_nodes_N_centrality_1))
        print('critical_nodes_N_centrality_2:\t', len(critical_nodes_N_centrality_2))
        print('centrality_1_N_centrality_2:\t', len(centrality_1_N_centrality_2))
        print('critical_nodes_N_centrality_1_N_Essential:\t', len(critical_nodes_N_centrality_1_N_Essential))
        print('critical_nodes_N_centrality_2_N_Essential:\t', len(critical_nodes_N_centrality_2_N_Essential))
        print('centrality_1_N_centrality_2_N_Essential:\t', len(centrality_1_N_centrality_2_N_Essential))
        print('\n')        


centrality_analysis()
