import networkx as nx

def get_centrality(G, centrality):
    if (centrality == 'Degree'):
        all_nodes = list(G.nodes)
        _dictionary = {}
        for node in all_nodes:
            _dictionary[node] = G.degree[node]
        return _dictionary
    if (centrality == 'Betweenness'):
        return nx.betweenness_centrality(G)
    if (centrality == 'Closeness'):
        return nx.closeness_centrality(G)
    if (centrality == 'Eigenvector'):
        return nx.eigenvector_centrality(G, max_iter=5000)

def get_essential_proteins_info(species):
    Essentiality_File = open(".\\" + species + "\\DIP\\output\\DIP_IDs_N_Essentiality.txt", "r") 
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

# species = "Escherichia coli"
species = "Saccharomyces cerevisiae"

file_name = ".\\" + species + "\\DIP\\output\\original_PPIs_redundancies_N_self_loops_removed_N_Connected.txt"
G = nx.read_edgelist(file_name, nodetype=str, data=(('weight', int),)) #reading a graph as edge listed
print("G has ", G.number_of_nodes(), " nodes and ", G.number_of_edges(), " edges.")
all_nodes = list(G.nodes)

all_essential_proteins = get_essential_proteins_info(species)[2]

centrality_list = ['Degree', 'Betweenness', 'Closeness', 'Eigenvector'] # 
for centrality in centrality_list:
    print('getting ' + centrality + ' centrality...')
    centrality_dictionary = get_centrality(G, centrality)
    print('writing ' + centrality + ' centrality...')

    # writing all proteins
    output_file = open(".\\" + species + "\\DIP\\output\\global_centrality_analysis\\all_proteins_" + centrality.lower() + "_centrality.txt", 'w')
    output_file.write("Node\tCentrality\n")
    for node in all_nodes:
        output_file.write(node + '\t' + str(centrality_dictionary[node]) + '\n')
    output_file.close()

    # writing all essential proteins
    output_file = open(".\\" + species + "\\DIP\\output\\global_centrality_analysis\\all_essential_proteins_" + centrality.lower() + "_centrality.txt", 'w')
    output_file.write("Node\tCentrality\n")
    for node in all_essential_proteins:
        output_file.write(node + '\t' + str(centrality_dictionary[node]) + '\n')
    output_file.close()