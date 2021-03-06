import networkx as nx
import csv

def get_essential_proteins_info():
    # Essentiality_File = open(".\\Escherichia coli\\DIP\\output\\DIP_IDs_N_Essentiality.txt", "r") 
    Essentiality_File = open(".\\Saccharomyces cerevisiae\\DIP\\output\\DIP_IDs_N_Essentiality.txt", "r") 
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

def get_centrality(G, centrality):
    if (centrality == 'Degree'):
        return nx.degree_centrality(G)
    if (centrality == 'Betweenness'):
        return nx.betweenness_centrality(G)
    if (centrality == 'Closeness'):
        return nx.closeness_centrality(G)
    if (centrality == 'Eigenvector'):
        return nx.eigenvector_centrality(G, max_iter=5000)

def get_critical_node_centrality(G, critical_nodes, centrality, centrality_dictionary): 
    critical_node_centrality = {}
    if (centrality != 'Degree'):
        for node in critical_nodes:        
            critical_node_centrality[node] = centrality_dictionary[node]
    else:
        for node in critical_nodes:        
            critical_node_centrality[node] = G.degree[node]
    return critical_node_centrality

def centrality_criticality_analysis(G):
    analysis = {}
    centrality_list = ['Degree', 'Betweenness', 'Closeness', 'Eigenvector'] # 
    for centrality in centrality_list:
        analysis[centrality] = get_alalysis(G, centrality)
    return analysis

def get_alalysis(G, centrality): 
    print('##################################')
    print('##################################')
    print(centrality)
    # centrality_based_nodes_file = open(".\\Escherichia coli\\DIP\\output\\global_centrality_analysis\\removed_nodes_based_on_" + centrality + "_centrality.budget_400.txt", "r") 
    centrality_based_nodes_file = open(".\\Saccharomyces cerevisiae\\DIP\\output\\global_centrality_analysis\\removed_nodes_based_on_" + centrality + "_centrality.budget_950.txt", "r") 
    
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
    unknown_essential_proteins_ID = essential_proteins_info[3]

    for i in range(50, 951, 50): # for i in range(50, 951, 50):
        # GA_critical_nodes_file = open(".\\Escherichia coli\\DIP\\output\\Boost\\Result\\critical.nodes.found.by.GA." + str(i) + ".txt", "r") 
        GA_critical_nodes_file = open(".\\Saccharomyces cerevisiae\\DIP\\output\\Boost\\Result\\critical.nodes.found.by.GA." + str(i) + ".txt", "r") 
        critical_nodes = []
        _index = 0
        for line in GA_critical_nodes_file:
            if (_index >= 2): # for the header
                critical_nodes.append(line.split()[1])
            _index += 1        
        critical_node_centrality = get_critical_node_centrality(G, critical_nodes, centrality, centrality_dictionary)  

        
        critical_nodes_N_essentials = [value for value in critical_nodes if value in essential_proteins_ID]
        critical_nodes_N_unknown_essentials = [value for value in critical_nodes if value in unknown_essential_proteins_ID]

        centrality_based_nodes_N_essentials = [value for value in centrality_based_nodes[0:i+1] if value in essential_proteins_ID]
        centrality_based_nodes_N_unknown_essentials = [value for value in centrality_based_nodes[0:i+1] if value in unknown_essential_proteins_ID]
        print('Number of nodes:\t', i)
        print('critical_nodes_N_essentials:\t', len(critical_nodes_N_essentials))
        print('critical_nodes_N_unknown_essentials:\t', len(critical_nodes_N_unknown_essentials))
        print('centrality_based_nodes_N_essentials:\t', len(centrality_based_nodes_N_essentials))
        print('centrality_based_nodes_N_unknown_essentials:\t', len(centrality_based_nodes_N_unknown_essentials))
        _lst = [value for value in centrality_based_nodes_N_essentials if value in critical_nodes_N_essentials]
        print(len(_lst), '\t', len(_lst) / len(critical_nodes_N_essentials) * 100, '%')
        print('\n\n')

        # output_file_name = ".\\Escherichia coli\\DIP\\output\\Boost\\Result\\intersection_statistics\\" + centrality + "\\budget_" + str(i) + ".txt"
        output_file_name = ".\\Saccharomyces cerevisiae\\DIP\\output\\Boost\\Result\\intersection_statistics\\" + centrality + "\\budget_" + str(i) + ".txt"       
        output_file = open(output_file_name, 'w')
                
        # CSV_output_file_name = ".\\Escherichia coli\\DIP\\output\\Boost\\Result\\intersection_statistics\\" + centrality + "\\budget_" + str(i) + ".csv"
        CSV_output_file_name = ".\\Saccharomyces cerevisiae\\DIP\\output\\Boost\\Result\\intersection_statistics\\" + centrality + "\\budget_" + str(i) + ".csv"       
        CSV_output_file = open(CSV_output_file_name, mode='w')
        CSV_output_writer = csv.writer(CSV_output_file, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL, lineterminator='\n')    
        CSV_output_writer.writerow(['P', 'x'])    

        output_file.write('critical_nodes_N_essentials:\t'+ str(len(critical_nodes_N_essentials)) + '\n')
        output_file.write('critical_nodes_N_unknown_essentials:\t' + str(len(critical_nodes_N_unknown_essentials)) + '\n')
        output_file.write('centrality_based_nodes_N_essentials:\t' + str(len(centrality_based_nodes_N_essentials)) + '\n')
        output_file.write('centrality_based_nodes_N_unknown_essentials:\t' + str(len(centrality_based_nodes_N_unknown_essentials)) + '\n')
        output_file.write('essential_nodes_intersection:\t' + str(len(_lst)) + '\t' + str(len(_lst) / len(critical_nodes_N_essentials) * 100) + '%\n')
        output_file.write('\n##################\n\n')
        output_file.write('Node\tCentrality\n')
        output_file.write('critical_nodes\n')  
        for node in critical_nodes_N_essentials:
            output_file.write(node + '\t' + str(critical_node_centrality[node]) + '\n')
            CSV_output_writer.writerow(['Genetic_Algorithm', str(critical_node_centrality[node])])
        
        output_file.write('\n##################\n\n')
        output_file.write('centrality_based_nodes\n')        
        for node in centrality_based_nodes_N_essentials:
            output_file.write(node + '\t' + str(centrality_based_nodes_centrality[node]) + '\n')
            CSV_output_writer.writerow([centrality + '_Centrality', str(centrality_based_nodes_centrality[node])])
        output_file.close
        


# file_name = ".\\Escherichia coli\\DIP\\output\\original_PPIs_redundancies_N_self_loops_removed_N_Connected.txt"
file_name = ".\\Saccharomyces cerevisiae\\DIP\\output\\original_PPIs_redundancies_N_self_loops_removed_N_Connected.txt"
G = nx.read_edgelist(file_name, nodetype=str, data=(('weight', int),)) #reading a graph as edge listed
centrality_criticality_analysis(G)
