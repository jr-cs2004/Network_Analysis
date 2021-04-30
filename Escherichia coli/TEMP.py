# Essentiality_File = open("E:\\Javad Rezaei\\Second Paper\\Network_Analysis\\Escherichia coli\\DIP\\output\\DIP_IDs_N_Essentiality.txt", "r") 
Essentiality_File = open("E:\\Javad Rezaei\\Second Paper\\Network_Analysis\\Saccharomyces cerevisiae\\DIP\\output\\DIP_IDs_N_Essentiality.txt", "r") 
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
# quit()
# GA_critical_nodes_file = open("E:\\Javad Rezaei\\Second Paper\\Boost\\Boost\\E.coli\\Result\\4 20 2021 based on new implementation\\critical.nodes.found.by.GA.350.txt", "r") 
GA_critical_nodes_file = open("E:\\Javad Rezaei\\Second Paper\\Boost\\Boost\\S.cerevisiae\\Result\\critical.nodes.found.by.GA.100.txt", "r") 
critical_nodes = []
_index = 0
for line in GA_critical_nodes_file:
    if (_index >= 2):
        critical_nodes.append(line.split()[1])
    _index += 1


# hub_nodes_file = open("E:\\Javad Rezaei\\Second Paper\\Boost\\Boost\\E.coli\\Result\\4 20 2021 based on new implementation\\hubs.removal.350.txt", "r") 
hub_nodes_file = open("E:\\Javad Rezaei\\Second Paper\\Boost\\Boost\\S.cerevisiae\\Result\\hubs.removal.100.txt", "r") 
hub_nodes = []
_index = 0
for line in hub_nodes_file:
    if (_index >= 1):
        hub_nodes.append(line.split()[1])
    _index += 1

critical_nodes_N_essentials = [value for value in critical_nodes if value in essential_IDs]
critical_nodes_N_unknown_essentials = [value for value in critical_nodes if value in unknown_essential_IDs]

hub_nodes_N_essentials = [value for value in hub_nodes if value in essential_IDs]
hub_nodes_N_unknown_essentials = [value for value in hub_nodes if value in unknown_essential_IDs]


print(len(critical_nodes_N_essentials))
print(len(critical_nodes_N_unknown_essentials))
print(len(hub_nodes_N_essentials))
print(len(hub_nodes_N_unknown_essentials))


_lst = [value for value in hub_nodes_N_essentials if value in critical_nodes_N_essentials]
print(len(_lst))
