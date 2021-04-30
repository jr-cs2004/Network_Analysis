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


# ######################################################################################
# ######################################################################################
# ######################################################################################


DIP_File = open("DIP\\output\\original_PPIs_redundancies_N_self_loops_removed_N_Connected.txt", "r")
DIP_source_protein_IDs = []
DIP_target_protein_IDs = []
for line in DIP_File:
   DIP_source_protein_IDs.append(line.split()[0])
   DIP_target_protein_IDs.append(line.split()[1])

_str = ('the interaction file was read:' + '\n'
+ '# of lines in the PPI files read for source interacting proteins: ' + str(len(DIP_source_protein_IDs)) + '\n'
+ '# of lines in the PPI files read for target interacting proteins: ' + str(len(DIP_target_protein_IDs)) + '\n'
+ '# of unique proteins in the source lines: ' + str(len(list(set(DIP_source_protein_IDs)))) + '\n'
+ '# of unique proteins in the target lines: ' + str(len(list(set(DIP_target_protein_IDs)))) + '\n')
print(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################


all_unique_proteins_in_DIP = []
all_unique_proteins_in_DIP.extend(DIP_source_protein_IDs)
all_unique_proteins_in_DIP.extend(DIP_target_protein_IDs)

_str = '# of all_unique_proteins_in_DIP: ' + str(len(list(set(all_unique_proteins_in_DIP)))) + '\n'
print(_str)
all_unique_proteins_in_DIP = list(set(all_unique_proteins_in_DIP))


# ######################################################################################
# ######################################################################################
# ######################################################################################


import random
sample_size = 50
for sample_size in range(50, 1000, 50):
    essentials_in_random_samples_percentage = 0
    for i in range(0, 5): 
        random_samples = random.sample(all_unique_proteins_in_DIP, sample_size)   
        essentials_in_random_samples = [value for value in random_samples if value in essential_IDs]
        essentials_in_random_samples_percentage += round(len(essentials_in_random_samples) / sample_size * 100)
    essentials_in_random_samples_percentage /= 5
    print(round(essentials_in_random_samples_percentage), '%')
