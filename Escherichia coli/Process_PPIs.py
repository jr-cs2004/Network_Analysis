#!/usr/bin/python

import sys

# ######################################################################################
# ######################################################################################
# ######################################################################################


import urllib.parse
import urllib.request

url = 'https://www.uniprot.org/uploadlists/'

def convertIDs(query, source_type, target_type):
   params = {
      'from': source_type,
      'to': target_type,
      'format': 'tab',
      'query': query
   }
   data = urllib.parse.urlencode(params)
   data = data.encode('utf-8')
   req = urllib.request.Request(url, data)
   with urllib.request.urlopen(req) as f:
      response = f.read()
   # print(response.decode('utf-8'))
   result = response.decode('utf-8').split()
   index = 0
   return_list = [[],[]]
   for x in result:
      if (index % 2 == 0 and index > 1):
         return_list[0].append(x)
      if (index % 2 == 1 and index > 1):
         return_list[1].append(x)
      index = index + 1
   return return_list

def remove_redundancy(source_protein_IDs, target_protein_IDs):
    repeat_counter = 0
    loop_counter = 0
    removing_indices = []
    n = len(source_protein_IDs)
    for i in range(0, n):
        source_i = source_protein_IDs[i]
        target_i = target_protein_IDs[i]
        if (source_i == target_i):
            loop_counter += 1
            removing_indices.append(i)
    print('# of self loops: ', loop_counter)

    # removing self loops interactions.
    for indx in sorted(removing_indices, reverse = True):
        del source_protein_IDs[indx] 
        del target_protein_IDs[indx]

    n = len(source_protein_IDs)
    for i in range(0, n):
        if (i < n): # at each iteration, n may changes
            if (i % 100 == 0):
                print (round(i / n * 100, 1), '%', end="\r")            
            source_i = source_protein_IDs[i]
            target_i = target_protein_IDs[i]
            removing_indices = []
            for j in range(i+1, n):
                source_j = source_protein_IDs[j]
                target_j = target_protein_IDs[j]     
                if (source_i == source_j and target_i == target_j) or (source_i == target_j and source_j == target_i):
                    removing_indices.append(j)
                    repeat_counter += 1
                    print(source_i, target_i)
                    print(source_j, target_j)
            for indx in sorted(removing_indices, reverse = True):
                del source_protein_IDs[indx] 
                del target_protein_IDs[indx]
            n = len(source_protein_IDs)
    print('# of duplications: ', repeat_counter)
    
    return [source_protein_IDs, target_protein_IDs]
     




# ######################################################################################
# ######################################################################################
# ######################################################################################


print('Number of arguments:', len(sys.argv), 'arguments.')
print(sys.argv)
root_folder_path = sys.argv[1]

statistics_file_name = root_folder_path + '/output/statistics.txt'
original_PPIs_file_name = root_folder_path + '/original_PPIs.txt'
PPIs_without_repeats_file_name = root_folder_path + '/output/PPIs_without_repeats.txt'
repeats_statistics_file_name = root_folder_path + '/output/repeats_statistics.txt'
GGIs_file_name = root_folder_path + '/output/GGIs.txt'
GGIs_Filtered_By_Essentiality_Information_file_name = root_folder_path + '/output/GGIs_Filtered_By_Essentiality_Information.txt'


# ######################################################################################
# ######################################################################################
# ######################################################################################


deg_File = open("DEG/E.Coli.MG1655.I.Essential.Genes.txt", "r", encoding='utf8')
_counter = 0
deg_genes = []
for line in deg_File:
    deg_genes.append(line.split('\t')[1])
    _counter += 1
print('# of genes reported by deg: ', _counter)
print('# of unique genes reported by deg: ', len(list(set(deg_genes))))


# ######################################################################################
# ######################################################################################
# ######################################################################################


ogee_File = open("OGEE/report_1.txt", "r")
_counter = 0
ogee_genes = []
ogee_essential_genes = []
ogee_non_essential_genes = []
ogee_conditionally_essential_genes = []
for line in ogee_File:
    ogee_genes.append([line.split('\t')[4], line.split('\t')[6]])
    _counter += 1
print('# of genes reported by ogee: ', _counter)

essential_counter = 0
non_essential_counter = 0
conditionally_essential_counter = 0

deg_and_ogee_essential_intersection_coounter = 0
deg_and_ogee_non_essential_intersection_coounter = 0
deg_and_ogee_conditionally_essential_intersection_coounter = 0

for item in ogee_genes:
    if (item[1] == 'E'):
        essential_counter += 1
        ogee_essential_genes.append(item[0])
        if item[0] in deg_genes:
            deg_and_ogee_essential_intersection_coounter += 1
    if (item[1] == 'NE'):
        non_essential_counter += 1
        ogee_non_essential_genes.append(item[0])
        if item[0] in deg_genes:
            deg_and_ogee_non_essential_intersection_coounter += 1
    if (item[1] == 'C'):
        conditionally_essential_counter += 1
        ogee_conditionally_essential_genes.append(item[0])
        if item[0] in deg_genes:
            deg_and_ogee_conditionally_essential_intersection_coounter += 1
print('OGEE: # of essentials: ', essential_counter, '\n# of non-essentials: ', non_essential_counter,
        '\n# of conditionally essentials: ', conditionally_essential_counter)

print('OGEE: # of unique essentials: ', essential_counter, '\n# of unique non-essentials: ', non_essential_counter,
        '\n# of unique conditionally essentials: ', conditionally_essential_counter)

print('# of DEG and OGEE \nessentials intersection: ', deg_and_ogee_essential_intersection_coounter, 
        '\nnon-essentials intersection: ', deg_and_ogee_non_essential_intersection_coounter,
        '\nconditionally essentials intersection: ', deg_and_ogee_conditionally_essential_intersection_coounter)

combined_deg_ogee = [[][]]

# ######################################################################################
# ######################################################################################
# ######################################################################################


statistics_file = open(statistics_file_name, 'w')

# First we must read the list of all interactions from the local DB dataset
# All intercations are stored in two lists each containing one end of each interaction.

print('reading interaction file...\n')

original_PPIs_file = open(original_PPIs_file_name, "r")

source_protein_IDs = []
target_protein_IDs = []
interaction_score = []

protein_essentiality_based_on_deg = {}
protein_essentiality_based_on_OGEE = {}

i = 0
for line in original_PPIs_file:
   source_protein_IDs.append(line.split(' ')[0])
   target_protein_IDs.append(line.split(' ')[1])
   interaction_score.append(int(line.split(' ')[2]))

_str = ('the interaction file was read:' + '\n'
+ '# of lines in the PPI files read for source interacting proteins: ' + str(len(source_protein_IDs)) + '\n'
+ '# of lines in the PPI files read for target interacting proteins: ' + str(len(target_protein_IDs)) + '\n'
+ '# of unique proteins in the source lines: ' + str(len(list(set(source_protein_IDs)))) + '\n'
+ '# of unique proteins in the target lines: ' + str(len(list(set(target_protein_IDs)))) + '\n'
+ '# of unique proteins: ' + str(len(list(set(source_protein_IDs + target_protein_IDs)))) + '\n\n')
print(_str)
statistics_file.write(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################


unique_proteins = []
unique_proteins.extend(source_protein_IDs)
unique_proteins.extend(target_protein_IDs)
unique_proteins = list(set(unique_proteins))
_str = '# of unique_proteins: ' + str(len(unique_proteins)) + '\n\n'
print(_str)
statistics_file.write(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################


for i in range(900, 1000, 100):
    _file = open(root_folder_path + '/output/original_PPIs_threshold_' + str(i) + '.txt', 'w')
    _source_protein_IDs = []
    _target_protein_IDs = []
    index = 0
    n = len(source_protein_IDs)
    for index in range(0, n):
        if interaction_score[index] >= i: 
            _source_protein_IDs.append(source_protein_IDs[index])
            _target_protein_IDs.append(target_protein_IDs[index])
            _file.write(source_protein_IDs[index] + '\t' + target_protein_IDs[index] + '\n')
    _file.close()
    print('# of interaction with threshold ' + str(i) + ': ', len(_source_protein_IDs))
    _all_proteins = []
    _all_proteins.extend(_source_protein_IDs)
    _all_proteins.extend(_target_protein_IDs)
    _all_proteins = list(set(_all_proteins))
    print('# of unique proteins with threshold ' + str(i) + ': ', len(_all_proteins))
    
    unique_interactions = remove_redundancy(_source_protein_IDs, _target_protein_IDs)
    __source_protein_IDs = unique_interactions[0]
    __target_protein_IDs = unique_interactions[1]    
    print('# of interaction with threshold ' + str(i) + ': ', len(__source_protein_IDs))
    _all_proteins = []
    _all_proteins.extend(__source_protein_IDs)
    _all_proteins.extend(__target_protein_IDs)
    _all_proteins = list(set(_all_proteins))
    print('# of unique proteins with threshold ' + str(i) + ': ', len(_all_proteins))


# ######################################################################################
# ######################################################################################
# ######################################################################################
