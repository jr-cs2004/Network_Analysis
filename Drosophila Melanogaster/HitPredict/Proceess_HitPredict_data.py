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


statistics_file = open('statistics.txt', 'a')

# First we must read the list of all interactions from a hitpredict dataset
# All intercations are stored in two lists each containing one end of each interaction.

print('reading interaction file...\n')

# hitPredict_File = open("D_melanogaster_interactions_without_header_lines.txt", "r")
hitPredict_File = open("PPI_without_repeats.txt", "r")
# hitPredict_File = open("PPI_without_repeats_intersected_with_All_UniProt_IDs.txt", "r")

hitpredict_source_protein_IDs = []
hitpredict_target_protein_IDs = []
for line in hitPredict_File:
   hitpredict_source_protein_IDs.append(line.split()[0])
   hitpredict_target_protein_IDs.append(line.split()[1])

_str = ('the interaction file was read:' + '\n'
+ '# of lines in the PPI files read for source interacting proteins: ' + str(len(hitpredict_source_protein_IDs)) + '\n'
+ '# of lines in the PPI files read for target interacting proteins: ' + str(len(hitpredict_target_protein_IDs)) + '\n'
+ '# of unique proteins in the source lines: ' + str(len(list(set(hitpredict_source_protein_IDs)))) + '\n'
+ '# of unique proteins in the target lines: ' + str(len(list(set(hitpredict_target_protein_IDs)))) + '\n')
print(_str)
statistics_file.write(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################

# # to check if some PPIs are repeated or no,
# # if so, to check how many times each PPI is repeated.

# # we ran this part and saw that there is no repeat in HitPredict data and thus made 
# # this part of the code, as commented.

# repeat_counter = 0
# loop_counter = 0
# removing_indices = []
# counter_hash = {}
# for i in range(0, 100):
#    counter_hash[i] = 0
# n = len(hitpredict_source_protein_IDs)
# for i in range(0, n):
#    if (i < n): # at each iteration, n may changes
#       if (i % 100 == 0):
#          print (round(i / n * 100, 1), '%', end='\r', flush=True)
      
#       source_i = hitpredict_source_protein_IDs[i]
#       target_i = hitpredict_target_protein_IDs[i]

#       if (source_i == target_i):
#          loop_counter += 1      
#          del hitpredict_source_protein_IDs[i] 
#          del hitpredict_target_protein_IDs[i]
#          n = len(hitpredict_source_protein_IDs)
#          continue

#       repeat_counter = 0
#       removing_indices = []
#       for j in range(0,n):
#          if(i < j):
#             source_j = hitpredict_source_protein_IDs[j]
#             target_j = hitpredict_target_protein_IDs[j]     
#             if ( (source_i == source_j and target_i == target_j) or (source_i == target_j and source_j == target_i)):
#                removing_indices.append(j)
#                repeat_counter += 1
#       for indx in sorted(removing_indices, reverse = True):
#          del hitpredict_source_protein_IDs[indx] 
#          del hitpredict_target_protein_IDs[indx]
      
#       n = len(hitpredict_source_protein_IDs)
#       counter_hash[repeat_counter] = counter_hash[repeat_counter] + 1

# # print(len(removing_indices))
# # print(len(list(set(removing_indices))))

# print('repeat_counter: ', repeat_counter)
# print('loop_counter: ', loop_counter)

# n = len(hitpredict_source_protein_IDs)
# with open('PPI_without_repeats.txt', 'w') as _file:
#    for i in range(0, n):
#       _file.write(hitpredict_source_protein_IDs[i] + '\t' + hitpredict_target_protein_IDs[i] + '\n')

# with open('Repeats_statistics.txt', 'w') as _file:
#    for key in counter_hash:
#       _file.write(str(key) + '\t' + str(counter_hash[key]) + '\n')


# ######################################################################################
# ######################################################################################
# ######################################################################################


unique_proteins_in_hitpredict = []
unique_proteins_in_hitpredict.extend(hitpredict_source_protein_IDs)
unique_proteins_in_hitpredict.extend(hitpredict_target_protein_IDs)
unique_proteins_in_hitpredict = list(set(unique_proteins_in_hitpredict))
_str = '# of unique_proteins_in_hitpredict: ' + str(len(unique_proteins_in_hitpredict)) + '\n'
print(_str)
statistics_file.write(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################

# counting the number of IDs which are not included in UniProt DB

# all_UniProt_IDs_File = open("../UniProt Data/All_UniProt_IDs.list", "r")
# all_UniProt_IDs = []
# for line in all_UniProt_IDs_File:
#    all_UniProt_IDs.append(line.split()[0])

# # print(len(all_UniProt_IDs))
# print(len(list(set(all_UniProt_IDs))))

# removing_indices = []
# node_counter = 0
# n = len(unique_proteins_in_hitpredict)
# for x in unique_proteins_in_hitpredict:
#    if x in all_UniProt_IDs:
#       node_counter += 1
#    else:
#       print(x)
# print('# of protein IDs not included in UniProt database: ', n - node_counter)
# print(node_counter)

# edge_counter = 0
# n = len(hitpredict_source_protein_IDs)
# for i in range(0, n):
#    source_i = hitpredict_source_protein_IDs[i]
#    target_i = hitpredict_target_protein_IDs[i]
#    if source_i in all_UniProt_IDs and target_i in all_UniProt_IDs:
#       edge_counter += 1
#    else: 
#       removing_indices.append(i)
# print('# of protein-protein interactions of which at least one of the corresponding protein IDs is not included in UniProt database: ', n - edge_counter)
# print(edge_counter)

# for indx in sorted(removing_indices, reverse = True):
#    del hitpredict_source_protein_IDs[indx] 
#    del hitpredict_target_protein_IDs[indx]

# n = len(hitpredict_source_protein_IDs)
# with open('PPI_without_repeats_intersected_with_All_UniProt_IDs.txt', 'w') as _file:
#    for i in range(0, n):
#       _file.write(hitpredict_source_protein_IDs[i] + '\t' + hitpredict_target_protein_IDs[i] + '\n')


# ######################################################################################
# ######################################################################################
# ######################################################################################


# Now we want to map each HitPredict ID (which is a UniPort ID) to a FlyBase ID
# 'FLYBASE_ID' is used to indicate that the corresponding ID is a FlyBase ID
# 'ID' is used to indicate that the corresponding ID is a UniProt ID
# note:  for each unique UniProt ID there may exists several FlyBase IDs!!!
#        We may interpret this event as: each protein may be synthesised by
#        different genes in a gene family.

print('converting hitpredict IDs to uniprot IDs...\n')

query = ' '.join(unique_proteins_in_hitpredict)
hitpredict_to_flybase_IDs = convertIDs(query, 'ID', 'FLYBASE_ID')

_str = ('IntAct IDs are mapped to flybase IDs:' + '\n'
+ '# of IDs returned by uniprot Mapper: ' + '\n'
+ 'from: ' + str(len(hitpredict_to_flybase_IDs[0]))  + ', and to: ' +  str(len(hitpredict_to_flybase_IDs[1]))
+ ', and uniques --> from: ' + str(len(list(set(hitpredict_to_flybase_IDs[0])))) +', and to: ' +  str(len(list(set(hitpredict_to_flybase_IDs[1])))) + '\n')
print(_str)
statistics_file.write(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################


_str = ('# of all_hitpredict_proteins_having_at_least_an_ID_in_flybase: '
+ str(len(list(set(hitpredict_to_flybase_IDs[0])))) + '\n'
+ '# of all_flybase_IDs_obtained_by_mapping_uniprot_to_flybase: '
+ str(len(list(set(hitpredict_to_flybase_IDs[1])))) + '\n')
print(_str)
statistics_file.write(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################


hitpredict_to_flybase_hash = {}

for x in list(set(unique_proteins_in_hitpredict)):
   hitpredict_to_flybase_hash[x] = []

n = len(hitpredict_to_flybase_IDs[0])
for i in range(0, n): 
   hitpredict_to_flybase_hash[hitpredict_to_flybase_IDs[0][i]].append(hitpredict_to_flybase_IDs[1][i])

# _temp = list(hitpredict_to_flybase_hash.keys())
# _str = ('# of hitpredict_to_flybase_hash_keys_length: ' + str(len(_temp))
# + ', and unique: ' + str(len(list(set(_temp)))))
# print(_str)
# statistics_file.write(_str)

hitpredict_proteins_having_no_intersection_in_their_corresponding_map_in_flybase = []
hitpredict_proteins_having_intersection_in_their_corresponding_map_in_flybase = []
hitpredict_proteins_having_the_same_corresponding_map_in_flybase = []
for key in hitpredict_to_flybase_hash:
   lst_1 = list(set(hitpredict_to_flybase_hash[key]))
   flag = True
   for key_2 in hitpredict_to_flybase_hash:
      lst_2 = list(set(hitpredict_to_flybase_hash[key_2]))
      if (key != key_2):
         lst_3 = [value for value in lst_1 if value in lst_2]
         if (len(lst_3) > 0):
            flag = False
            hitpredict_proteins_having_intersection_in_their_corresponding_map_in_flybase.append(key)
            if (len(lst_3) == len(lst_1) or len(lst_3) == len(lst_2)):
               hitpredict_proteins_having_the_same_corresponding_map_in_flybase.append(key)      
   if (flag and len(lst_1) > 0):
      hitpredict_proteins_having_no_intersection_in_their_corresponding_map_in_flybase.append(key)

_str = ('# of hitpredict_proteins_having_no_intersection_in_their_corresponding_map_in_flybase: '
+ str(len(hitpredict_proteins_having_no_intersection_in_their_corresponding_map_in_flybase))
+ ', and uniques: ' + str(len(list(set(hitpredict_proteins_having_no_intersection_in_their_corresponding_map_in_flybase)))) + '\n')
print(_str)
statistics_file.write(_str)

_str = ('# of hitpredict_proteins_having_intersection_in_their_corresponding_map_in_flybase: '
+ str(len(hitpredict_proteins_having_intersection_in_their_corresponding_map_in_flybase))
+ ', and uniques: ' + str(len(list(set(hitpredict_proteins_having_intersection_in_their_corresponding_map_in_flybase)))) + '\n')
print(_str)
statistics_file.write(_str)

_str = ('# of hitpredict_proteins_having_the_same_corresponding_map_in_flybase: '
+ str(len(hitpredict_proteins_having_the_same_corresponding_map_in_flybase))
+ ', and uniques: ' + str(len(list(set(hitpredict_proteins_having_the_same_corresponding_map_in_flybase)))) + '\n')
print(_str)
statistics_file.write(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################


counter_0 = 0
counter_1 = 0
counter_geq_2 = 0
proteins_having_only_one_corresponding_flybase_ID = 0
hitpredict_proteins_mapped_to_exactly_one_unique_ID = [[],[]]
unique_hitpredict_to_flybase_hash = {}

for key in hitpredict_to_flybase_hash:
   if (len(list(set(hitpredict_to_flybase_hash[key]))) == 0):
      counter_0 += 1
   elif (len(list(set(hitpredict_to_flybase_hash[key]))) == 1):
      counter_1 += 1
      if (key in hitpredict_proteins_having_no_intersection_in_their_corresponding_map_in_flybase or key in hitpredict_proteins_having_the_same_corresponding_map_in_flybase):
         proteins_having_only_one_corresponding_flybase_ID += 1
         unique_hitpredict_to_flybase_hash[key] = hitpredict_to_flybase_hash[key][0]
         hitpredict_proteins_mapped_to_exactly_one_unique_ID[0].append(key)
         hitpredict_proteins_mapped_to_exactly_one_unique_ID[1].append(hitpredict_to_flybase_hash[key][0])
   elif (len(list(set(hitpredict_to_flybase_hash[key]))) > 1):
      counter_geq_2 += 1
      
_str = ('The statistics about how HitPredict proeins are mapped to FlyBase IDs: ' + '\n' 
+ '# of proteins having no corresponding ID): ' + str(counter_0) + '\n'
+ '# of proteins mapped to exactly one ID): ' + str(counter_1) + '\n'
+ '# of proteins having more than one corresponding ID): ' + str(counter_geq_2) + '\n')
print(_str)
statistics_file.write(_str)

_str = ('# proteins_having_only_one_corresponding_flybase_ID: '
+ str(proteins_having_only_one_corresponding_flybase_ID) + '\n')
print(_str)
statistics_file.write(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################


_counter = {}
n = len(hitpredict_proteins_mapped_to_exactly_one_unique_ID[1])
for i in range(0, n):
   _counter[i] = 0
for i in range(0, n):
   counter = 0
   for j in range(0, n):
      if (hitpredict_proteins_mapped_to_exactly_one_unique_ID[1][i] == hitpredict_proteins_mapped_to_exactly_one_unique_ID[1][j]):
         counter += 1
   _counter[counter] += 1
for i in range(0, n):
   if (_counter[i] > 0):
      print(_counter[i], ' proteins have   ', i-1, '   common correspnding FlyBase IDs, with other proteins')

n = len(hitpredict_proteins_mapped_to_exactly_one_unique_ID[0])
with open('Mapping.UniProt.ID.to.FlyBase.ID.txt', 'w') as _file:
   for i in range(0, n):
      _file.write(hitpredict_proteins_mapped_to_exactly_one_unique_ID[0][i] + '\t' + hitpredict_proteins_mapped_to_exactly_one_unique_ID[1][i] + '\n')


# ######################################################################################
# ######################################################################################
# ######################################################################################


DEG_OGEE_combined_data_File = open('../DEG_OGEE_combined_data.txt', 'r')
list_of_valid_genes = []
for line in DEG_OGEE_combined_data_File:
    list_of_valid_genes.append(line.split()[0])
print(len(list(set(list_of_valid_genes))))


# ######################################################################################
# ######################################################################################
# ######################################################################################


n = len(hitpredict_source_protein_IDs)
counter_GGIs = 0
counter_filtered_GGIs = 0
GGIs_file = open('HitPredict.GGIs.txt', 'w')
filtered_GGIs_file = open('HitPredict.GGIs.Filtered.By.Essentiality.Information.txt', 'w')
unique_genes_in_GGIs = []
unique_genes_in_filtered_GGIs = []
for i in range(0, n):
   if (unique_hitpredict_to_flybase_hash.get(hitpredict_source_protein_IDs[i], False) and unique_hitpredict_to_flybase_hash.get(hitpredict_target_protein_IDs[i], False)):
      GGIs_file.write(unique_hitpredict_to_flybase_hash[hitpredict_source_protein_IDs[i]] + '\t' + unique_hitpredict_to_flybase_hash[hitpredict_target_protein_IDs[i]] + '\n')
      unique_genes_in_GGIs.append(unique_hitpredict_to_flybase_hash[hitpredict_source_protein_IDs[i]])
      unique_genes_in_GGIs.append(unique_hitpredict_to_flybase_hash[hitpredict_target_protein_IDs[i]])
      counter_GGIs += 1
   if (unique_hitpredict_to_flybase_hash.get(hitpredict_source_protein_IDs[i], False) and unique_hitpredict_to_flybase_hash.get(hitpredict_target_protein_IDs[i], False) 
      and (unique_hitpredict_to_flybase_hash[hitpredict_source_protein_IDs[i]] in list_of_valid_genes) and (unique_hitpredict_to_flybase_hash[hitpredict_target_protein_IDs[i]] in list_of_valid_genes)):
      filtered_GGIs_file.write(unique_hitpredict_to_flybase_hash[hitpredict_source_protein_IDs[i]] + '\t' + unique_hitpredict_to_flybase_hash[hitpredict_target_protein_IDs[i]] + '\n')
      unique_genes_in_filtered_GGIs.append(unique_hitpredict_to_flybase_hash[hitpredict_source_protein_IDs[i]])
      unique_genes_in_filtered_GGIs.append(unique_hitpredict_to_flybase_hash[hitpredict_target_protein_IDs[i]])
      counter_filtered_GGIs += 1

print(counter_GGIs, counter_filtered_GGIs)
print(len(list(set(unique_genes_in_GGIs))), len(list(set(unique_genes_in_filtered_GGIs))))
