import networkx as nx

Essentiality_File = open("E:\\Javad Rezaei\\Second Paper\\Network_Analysis\\Escherichia coli\\DIP\\output\\DIP_IDs_N_Essentiality.txt", "r") 
_IDs = []
_Essentiality = []
essential_IDs = []
unknown_essential_IDs = []
for line in Essentiality_File:
   _IDs.append(line.split()[0])
   _Essentiality.append(line.split()[1])


file_name = "E:\\Javad Rezaei\\Second Paper\\Network_Analysis\\Escherichia coli\\DIP\\output\\original_PPIs_redundancies_N_self_loops_removed_N_Connected.txt"
# file_name = "test.txt"
G = nx.read_edgelist(file_name, nodetype=str, data=(('weight', int),)) #reading a graph as edge listed
print(G.number_of_nodes())
print(G.number_of_edges())


n = len(_IDs)
output_file = open("E:\\Javad Rezaei\\Second Paper\\Network_Analysis\\Escherichia coli\\DIP\\output\\Essential_Genes_Degree.txt", "w") 
for i in range(0, n):
    if (_Essentiality[i] == 'E'):
        output_file.write(_IDs[i] + '\t' + str(G.degree[_IDs[i]]) + '\n')
    