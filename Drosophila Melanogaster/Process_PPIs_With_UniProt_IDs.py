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


# ######################################################################################
# ######################################################################################
# ######################################################################################


print('Number of arguments:', len(sys.argv), 'arguments.')
print(sys.argv)
root_folder_path = sys.argv[1]

statistics_file_name = root_folder_path + '/output/statistics.txt'
original_PPIs_file_name = root_folder_path + '/original_PPIs.txt'
all_UniProt_IDs_file_name = 'UniProt Data/All_UniProt_IDs.list'
DEG_OGEE_combined_data_file_name = 'DEG_OGEE_combined_data.txt'

PPIs_without_repeats_file_name = root_folder_path + '/output/PPIs_without_repeats.txt'
repeats_statistics_file_name = root_folder_path + '/output/repeats_statistics.txt'
PPIs_without_repeats_intersected_with_UniProt_IDs_file_name = root_folder_path + '/output/PPIs_without_repeats_intersected_with_UniProt_IDs.txt'
localDB_IDs_not_in_UniProt_IDs_file_name = root_folder_path + '/output/Protein_IDs_not_in_UniProt_IDs.txt'
UniProt_ID_to_FlyBase_ID_file_name = root_folder_path + '/output/UniProt_ID_to_FlyBase_ID.txt'
GGIs_file_name = root_folder_path + '/output/GGIs.txt'
GGIs_Filtered_By_Essentiality_Information_file_name = root_folder_path + '/output/GGIs_Filtered_By_Essentiality_Information.txt'

statistics_file = open(statistics_file_name, 'w')

# First we must read the list of all interactions from the local DB dataset
# All intercations are stored in two lists each containing one end of each interaction.

print('reading interaction file...\n')

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
statistics_file.write(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################

# # to check if some PPIs are repeated or no,
# # if so, to check how many times each PPI is repeated.

# # we ran this part and saw that there is no repeat in local DB data and thus made 
# # this part of the code, as commented.

repeat_counter = 0
loop_counter = 0
removing_indices = []
counter_hash = {}
for i in range(0, 100):
   counter_hash[i] = 0
n = len(source_protein_IDs)
for i in range(0, n):
   if (i < n): # at each iteration, n may changes
      if (i % 100 == 0):
         print (round(i / n * 100, 1), '%', end='\r', flush=True)
      
      source_i = source_protein_IDs[i]
      target_i = target_protein_IDs[i]

      if (source_i == target_i):
         loop_counter += 1      
         del source_protein_IDs[i] 
         del target_protein_IDs[i]
         n = len(source_protein_IDs)
         continue

      repeat_counter = 0
      removing_indices = []
      for j in range(0,n):
         if(i < j):
            source_j = source_protein_IDs[j]
            target_j = target_protein_IDs[j]     
            if ( (source_i == source_j and target_i == target_j) or (source_i == target_j and source_j == target_i)):
               removing_indices.append(j)
               repeat_counter += 1
      for indx in sorted(removing_indices, reverse = True):
         del source_protein_IDs[indx] 
         del target_protein_IDs[indx]
      
      n = len(source_protein_IDs)
      counter_hash[repeat_counter] = counter_hash[repeat_counter] + 1

# print(len(removing_indices))
# print(len(list(set(removing_indices))))

_str = ('removing replications and self_loops: \n'
+ '# of replications: ' + str(repeat_counter) + '\n'
+ '# of self_loops: ' + str(loop_counter) + '\n')
print(_str)
statistics_file.write(_str)

n = len(source_protein_IDs)
with open(PPIs_without_repeats_file_name, 'w') as _file:
   for i in range(0, n):
      _file.write(source_protein_IDs[i] + '\t' + target_protein_IDs[i] + '\n')

with open(repeats_statistics_file_name, 'w') as _file:
   for key in counter_hash:
      _file.write(str(key) + '\t' + str(counter_hash[key]) + '\n')


# ######################################################################################
# ######################################################################################
# ######################################################################################


unique_proteins = []
unique_proteins.extend(source_protein_IDs)
unique_proteins.extend(target_protein_IDs)
unique_proteins = list(set(unique_proteins))
_str = '# of unique_proteins after removing replications and self_loops: ' + str(len(unique_proteins)) + '\n\n'
print(_str)
statistics_file.write(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################

# counting the number of IDs which are not included in UniProt DB

all_UniProt_IDs_File = open(all_UniProt_IDs_file_name, 'r')
all_UniProt_IDs = []
for line in all_UniProt_IDs_File:
   all_UniProt_IDs.append(line.split()[0])

# print(len(all_UniProt_IDs))
print(len(list(set(all_UniProt_IDs))))
localDB_IDs_not_in_UniProt_IDs = []
removing_indices = []
node_counter = 0
n = len(unique_proteins)
for x in unique_proteins:
   if x in all_UniProt_IDs:
      node_counter += 1
   else:
      print(x)
      localDB_IDs_not_in_UniProt_IDs.append(x)
_str = ('# of protein IDs not included in UniProt database: ' + str(n - node_counter) + '\n')
print(_str)
print(node_counter)
statistics_file.write(_str)

edge_counter = 0
n = len(source_protein_IDs)
for i in range(0, n):
   source_i = source_protein_IDs[i]
   target_i = target_protein_IDs[i]
   if source_i in all_UniProt_IDs and target_i in all_UniProt_IDs:
      edge_counter += 1
   else: 
      removing_indices.append(i)
_str = ('# of PPIs of which at least one of the corresponding protein IDs is not included in UniProt database: ' + str(n - edge_counter) + '\n\n')
print(_str)
print(edge_counter)
statistics_file.write(_str)

for indx in sorted(removing_indices, reverse = True):
   del source_protein_IDs[indx] 
   del target_protein_IDs[indx]

n = len(source_protein_IDs)
with open(PPIs_without_repeats_intersected_with_UniProt_IDs_file_name, 'w') as _file:
   for i in range(0, n):
      _file.write(source_protein_IDs[i] + '\t' + target_protein_IDs[i] + '\n')

localDB_IDs_not_in_UniProt_IDs = list(set(localDB_IDs_not_in_UniProt_IDs))
n = len(localDB_IDs_not_in_UniProt_IDs)
with open(localDB_IDs_not_in_UniProt_IDs_file_name, 'w') as _file:
   for i in range(0, n):
      _file.write(localDB_IDs_not_in_UniProt_IDs[i] + '\n')

# ######################################################################################
# ######################################################################################
# ######################################################################################


# Now we want to map each local DB ID (which is a UniPort ID) to a FlyBase ID
# 'FLYBASE_ID' is used to indicate that the corresponding ID is a FlyBase ID
# 'ID' is used to indicate that the corresponding ID is a UniProt ID
# note:  for each unique UniProt ID there may exists several FlyBase IDs!!!
#        We may interpret this event as: each protein may be synthesised by
#        different genes in a gene family.

print('converting local DB IDs (UniProt IDs) to FlyBase IDs...\n')

query = ' '.join(unique_proteins)
localDB_IDs_to_FlyBase_IDs = convertIDs(query, 'ID', 'FLYBASE_ID')

_str = ('localDB IDs are mapped to FlyBase IDs:' + '\n'
+ '# of IDs returned by uniprot Mapper: '
+ 'from: ' + str(len(localDB_IDs_to_FlyBase_IDs[0]))  + ' to: ' +  str(len(localDB_IDs_to_FlyBase_IDs[1]))
+ ' ---- uniques --> from: ' + str(len(list(set(localDB_IDs_to_FlyBase_IDs[0])))) +' to: ' +  str(len(list(set(localDB_IDs_to_FlyBase_IDs[1])))) + '\n')
print(_str)
statistics_file.write(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################


_str = ('# of all_proteins_having_at_least_an_ID_in_FlyBase: '
+ str(len(list(set(localDB_IDs_to_FlyBase_IDs[0])))) + '\n'
+ '# of all_FlyBase_IDs_obtained_by_mapping_uniprot_to_FlyBase: '
+ str(len(list(set(localDB_IDs_to_FlyBase_IDs[1])))) + '\n')
print(_str)
statistics_file.write(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################


localDB_IDs_to_FlyBase_IDs_hash = {}

for x in list(set(unique_proteins)):
   localDB_IDs_to_FlyBase_IDs_hash[x] = []

n = len(localDB_IDs_to_FlyBase_IDs[0])
for i in range(0, n): 
   localDB_IDs_to_FlyBase_IDs_hash[localDB_IDs_to_FlyBase_IDs[0][i]].append(localDB_IDs_to_FlyBase_IDs[1][i])

# _temp = list(localDB_IDs_to_FlyBase_IDs_hash.keys())
# _str = ('# of localDB_IDs_to_FlyBase_IDs_hash_keys_length: ' + str(len(_temp))
# + ', and unique: ' + str(len(list(set(_temp)))))
# print(_str)
# statistics_file.write(_str)

proteins_having_no_intersection_in_their_corresponding_map_in_FlyBase = []
proteins_having_intersection_in_their_corresponding_map_in_FlyBase = []
proteins_having_the_same_corresponding_map_in_FlyBase = []
for key in localDB_IDs_to_FlyBase_IDs_hash:
   lst_1 = list(set(localDB_IDs_to_FlyBase_IDs_hash[key]))
   flag = True
   for key_2 in localDB_IDs_to_FlyBase_IDs_hash:
      lst_2 = list(set(localDB_IDs_to_FlyBase_IDs_hash[key_2]))
      if (key != key_2):
         lst_3 = [value for value in lst_1 if value in lst_2]
         if (len(lst_3) > 0):
            flag = False
            proteins_having_intersection_in_their_corresponding_map_in_FlyBase.append(key)
            if (len(lst_3) == len(lst_1) or len(lst_3) == len(lst_2)):
               proteins_having_the_same_corresponding_map_in_FlyBase.append(key)      
   if (flag and len(lst_1) > 0):
      proteins_having_no_intersection_in_their_corresponding_map_in_FlyBase.append(key)

_str = ('# of proteins_having_no_intersection_in_their_corresponding_map_in_FlyBase: '
+ str(len(proteins_having_no_intersection_in_their_corresponding_map_in_FlyBase))
+ ', and uniques: ' + str(len(list(set(proteins_having_no_intersection_in_their_corresponding_map_in_FlyBase)))) + '\n')
print(_str)
statistics_file.write(_str)

_str = ('# of proteins_having_intersection_in_their_corresponding_map_in_FlyBase: '
+ str(len(proteins_having_intersection_in_their_corresponding_map_in_FlyBase))
+ ', and uniques: ' + str(len(list(set(proteins_having_intersection_in_their_corresponding_map_in_FlyBase)))) + '\n')
print(_str)
statistics_file.write(_str)

_str = ('# of proteins_having_the_same_corresponding_map_in_FlyBase: '
+ str(len(proteins_having_the_same_corresponding_map_in_FlyBase))
+ ', and uniques: ' + str(len(list(set(proteins_having_the_same_corresponding_map_in_FlyBase)))) + '\n\n')
print(_str)
statistics_file.write(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################


counter_0 = 0
counter_1 = 0
counter_geq_2 = 0
proteins_having_only_one_corresponding_FlyBase_ID = 0
proteins_mapped_to_exactly_one_unique_ID = [[],[]]
unique_localDB_IDs_to_FlyBase_IDs_hash = {}

for key in localDB_IDs_to_FlyBase_IDs_hash:
   if (len(list(set(localDB_IDs_to_FlyBase_IDs_hash[key]))) == 0):
      counter_0 += 1
   elif (len(list(set(localDB_IDs_to_FlyBase_IDs_hash[key]))) == 1):
      counter_1 += 1
      if (key in proteins_having_no_intersection_in_their_corresponding_map_in_FlyBase or key in proteins_having_the_same_corresponding_map_in_FlyBase):
         proteins_having_only_one_corresponding_FlyBase_ID += 1
         unique_localDB_IDs_to_FlyBase_IDs_hash[key] = localDB_IDs_to_FlyBase_IDs_hash[key][0]
         proteins_mapped_to_exactly_one_unique_ID[0].append(key)
         proteins_mapped_to_exactly_one_unique_ID[1].append(localDB_IDs_to_FlyBase_IDs_hash[key][0])
   elif (len(list(set(localDB_IDs_to_FlyBase_IDs_hash[key]))) > 1):
      counter_geq_2 += 1
      
_str = ('The statistics about how proeins are mapped to FlyBase IDs: ' + '\n' 
+ '# of proteins having no corresponding ID): ' + str(counter_0) + '\n'
+ '# of proteins mapped to exactly one ID): ' + str(counter_1) + '\n'
+ '# of proteins having more than one corresponding ID): ' + str(counter_geq_2) + '\n')
print(_str)
statistics_file.write(_str)

_str = ('# proteins_having_only_one_corresponding_FlyBase_ID: '
+ str(proteins_having_only_one_corresponding_FlyBase_ID) + '\n')
print(_str)
statistics_file.write(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################


_counter = {}
n = len(proteins_mapped_to_exactly_one_unique_ID[1])
for i in range(0, n):
   _counter[i] = 0
for i in range(0, n):
   counter = 0
   for j in range(0, n):
      if (proteins_mapped_to_exactly_one_unique_ID[1][i] == proteins_mapped_to_exactly_one_unique_ID[1][j]):
         counter += 1
   _counter[counter] += 1
for i in range(0, n):
   if (_counter[i] > 0):
      print(_counter[i], ' proteins have   ', i-1, '   common correspnding FlyBase IDs, with other proteins')

n = len(proteins_mapped_to_exactly_one_unique_ID[0])
with open(UniProt_ID_to_FlyBase_ID_file_name, 'w') as _file:
   for i in range(0, n):
      _file.write(proteins_mapped_to_exactly_one_unique_ID[0][i] + '\t' + proteins_mapped_to_exactly_one_unique_ID[1][i] + '\n')


# ######################################################################################
# ######################################################################################
# ######################################################################################


DEG_OGEE_combined_data_File = open(DEG_OGEE_combined_data_file_name, 'r')
list_of_valid_genes = []
for line in DEG_OGEE_combined_data_File:
    list_of_valid_genes.append(line.split()[0])
print(len(list(set(list_of_valid_genes))))


# ######################################################################################
# ######################################################################################
# ######################################################################################


n = len(source_protein_IDs)
counter_GGIs = 0
counter_filtered_GGIs = 0
GGIs_file = open(GGIs_file_name, 'w')
filtered_GGIs_file = open(GGIs_Filtered_By_Essentiality_Information_file_name, 'w')
unique_genes_in_GGIs = []
unique_genes_in_filtered_GGIs = []
for i in range(0, n):
   if (unique_localDB_IDs_to_FlyBase_IDs_hash.get(source_protein_IDs[i], False) and unique_localDB_IDs_to_FlyBase_IDs_hash.get(target_protein_IDs[i], False)):
      GGIs_file.write(unique_localDB_IDs_to_FlyBase_IDs_hash[source_protein_IDs[i]] + '\t' + unique_localDB_IDs_to_FlyBase_IDs_hash[target_protein_IDs[i]] + '\n')
      unique_genes_in_GGIs.append(unique_localDB_IDs_to_FlyBase_IDs_hash[source_protein_IDs[i]])
      unique_genes_in_GGIs.append(unique_localDB_IDs_to_FlyBase_IDs_hash[target_protein_IDs[i]])
      counter_GGIs += 1
   if (unique_localDB_IDs_to_FlyBase_IDs_hash.get(source_protein_IDs[i], False) and unique_localDB_IDs_to_FlyBase_IDs_hash.get(target_protein_IDs[i], False) 
      and (unique_localDB_IDs_to_FlyBase_IDs_hash[source_protein_IDs[i]] in list_of_valid_genes) and (unique_localDB_IDs_to_FlyBase_IDs_hash[target_protein_IDs[i]] in list_of_valid_genes)):
      filtered_GGIs_file.write(unique_localDB_IDs_to_FlyBase_IDs_hash[source_protein_IDs[i]] + '\t' + unique_localDB_IDs_to_FlyBase_IDs_hash[target_protein_IDs[i]] + '\n')
      unique_genes_in_filtered_GGIs.append(unique_localDB_IDs_to_FlyBase_IDs_hash[source_protein_IDs[i]])
      unique_genes_in_filtered_GGIs.append(unique_localDB_IDs_to_FlyBase_IDs_hash[target_protein_IDs[i]])
      counter_filtered_GGIs += 1

print(counter_GGIs, counter_filtered_GGIs)
print(len(list(set(unique_genes_in_GGIs))), len(list(set(unique_genes_in_filtered_GGIs))))
