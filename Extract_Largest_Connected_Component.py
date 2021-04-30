import networkx as nx

N = 700

# original_PPIs_file_name = ".\\Escherichia coli\\DIP\\output\\original_PPIs_threshold_" + str(N) + "_redundancies_N_self_loops_removed.txt"
original_PPIs_file_name = ".\\Drosophila Melanogaster\\DIP\\output\\original_PPIs_redundancies_N_self_loops_removed.txt"
G = nx.read_edgelist(original_PPIs_file_name, nodetype=str, data=(('weight', int),)) #reading a graph as edge listed

print('number_of_nodes: ', G.number_of_nodes())
print('number_of_edges: ', G.number_of_edges())

largest_cc = max(nx.connected_components(G), key=len)
print(len(largest_cc))

original_PPIs_file = open(original_PPIs_file_name, "r")

source_protein_IDs = []
target_protein_IDs = []
for line in original_PPIs_file:
   source_protein_IDs.append(line.split()[0])
   target_protein_IDs.append(line.split()[1])

_str = ('the interaction file was read:' + '\n'
+ '# of lines in the PPI files read for source interacting proteins: ' + str(len(source_protein_IDs)) + '\n'
+ '# of lines in the PPI files read for target interacting proteins: ' + str(len(target_protein_IDs)) + '\n'
+ '# of unique proteins in the source lines: ' + str(len(list(set(source_protein_IDs)))) + '\n'
+ '# of unique proteins in the target lines: ' + str(len(list(set(target_protein_IDs)))) + '\n'
+ '# of unique proteins: ' + str(len(list(set(source_protein_IDs + target_protein_IDs)))) + '\n\n')
print(_str)

# original_PPIs_file = open('.\\Escherichia coli\\STRING\\output\\original_PPIs_threshold_' + str(N) + '_redundancies_N_self_loops_removed_N_Connected.txt', "w")
original_PPIs_file = open('.\\Drosophila Melanogaster\\DIP\\output\\original_PPIs_redundancies_N_self_loops_removed_N_Connected.txt', "w")
i = 0
n = len(source_protein_IDs)
counter = 0
for i in range(0, n):
    if (source_protein_IDs[i] in largest_cc and target_protein_IDs[i] in largest_cc):
        counter += 1
        original_PPIs_file.write(source_protein_IDs[i] + '\t' + target_protein_IDs[i] + '\n')

print(counter)
        
# original_PPIs_file_name = ".\\Escherichia coli\\STRING\\output\\original_PPIs_threshold_" + str(N) + "_redundancies_N_self_loops_removed_N_Connected.txt"
original_PPIs_file_name = ".\\Drosophila Melanogaster\\DIP\\output\\original_PPIs_redundancies_N_self_loops_removed_N_Connected.txt"

original_PPIs_file = open(original_PPIs_file_name, "r")

source_protein_IDs = []
target_protein_IDs = []
for line in original_PPIs_file:
   source_protein_IDs.append(line.split()[0])
   target_protein_IDs.append(line.split()[1])

_str = ('the interaction file was read:' + '\n'
+ '# of lines in the PPI files read for source interacting proteins: ' + str(len(source_protein_IDs)) + '\n'
+ '# of lines in the PPI files read for target interacting proteins: ' + str(len(target_protein_IDs)) + '\n'
+ '# of unique proteins in the source lines: ' + str(len(list(set(source_protein_IDs)))) + '\n'
+ '# of unique proteins in the target lines: ' + str(len(list(set(target_protein_IDs)))) + '\n'
+ '# of unique proteins: ' + str(len(list(set(source_protein_IDs + target_protein_IDs)))) + '\n\n')
print(_str)

G_prime = nx.read_edgelist(original_PPIs_file_name, nodetype=str, data=(('weight', int),)) #reading a graph as edge listed
print('number_of_nodes: ', G_prime.number_of_nodes())
print('number_of_edges: ', G_prime.number_of_edges())

largest_cc = max(nx.connected_components(G_prime), key=len)
print(len(G_prime))