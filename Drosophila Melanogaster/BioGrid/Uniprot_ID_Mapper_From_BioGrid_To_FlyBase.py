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


def remove_proteins_having_the_same_uniprot_id_in_common(biogrid_source_to_uniprot_IDs):
   proteins_to_be_removed = []
   index = 0
   for x in biogrid_source_to_uniprot_IDs[1]:
      counter = 0
      for y in biogrid_source_to_uniprot_IDs[1]:
         if (x == y):
            counter += 1
      if (counter > 1):
         proteins_to_be_removed.append(biogrid_source_to_uniprot_IDs[0][index])
      index += 1

   indices_of_proteins_to_be_removed = []

   index = 0
   for x in biogrid_source_to_uniprot_IDs[0]:
      if x in set(proteins_to_be_removed):
         indices_of_proteins_to_be_removed.append(index)
      index += 1

   for ele in sorted(indices_of_proteins_to_be_removed, reverse = True):  
      del biogrid_source_to_uniprot_IDs[0][ele]
      del biogrid_source_to_uniprot_IDs[1][ele]
   return biogrid_source_to_uniprot_IDs
   
def remove_uniprot_entries_mapping_to_the_different_flybase_IDs(uniprot_of_source_to_flybase_IDs):
   proteins_to_be_removed = []
   index = 0
   for x in uniprot_of_source_to_flybase_IDs[0]:
      counter = 0
      for y in uniprot_of_source_to_flybase_IDs[0]:
         if (x == y):
            counter += 1
      if (counter > 1):
         proteins_to_be_removed.append(uniprot_of_source_to_flybase_IDs[0][index])
      index += 1

   indices_of_proteins_to_be_removed = []

   index = 0
   for x in uniprot_of_source_to_flybase_IDs[0]:
      if x in set(proteins_to_be_removed):
         indices_of_proteins_to_be_removed.append(index)
      index += 1

   for ele in sorted(indices_of_proteins_to_be_removed, reverse = True):  
      del uniprot_of_source_to_flybase_IDs[0][ele]
      del uniprot_of_source_to_flybase_IDs[1][ele]
   return uniprot_of_source_to_flybase_IDs

def combine_biogrid_to_uniprot_and_uniprot_to_flybase(biogrid_source_to_uniprot_IDs, uniprot_of_source_to_flybase_IDs):
   return []

statistics_file = open('statistics.txt', 'a')

# ######################################################################################
# ######################################################################################
# ######################################################################################

# First we must read the list of all interactions from a BioGrid dataset
# All intercations are stored in two lists each containing one end of each interaction.
# reading from original data obtained directly from BioGrid website

# print('reading interaction file...\n')

# bioGrid_File = open("Original_PPI_without_header_line.txt", "r")
# biogrid_source_protein_IDs = []
# biogrid_target_protein_IDs = []
# for line in bioGrid_File:
#    biogrid_source_protein_IDs.append(line.split()[1].split(':')[1])
#    biogrid_target_protein_IDs.append(line.split()[3].split(':')[1])

# _str = ('the interaction file was read:' + '\n'
# + '# of lines in the PPI files read for source interacting proteins: ' + str(len(biogrid_source_protein_IDs)) + '\n'
# + '# of lines in the PPI files read for target interacting proteins: ' + str(len(biogrid_target_protein_IDs)) + '\n'
# + '# of unique proteins in the source lines: ' + str(len(list(set(biogrid_source_protein_IDs)))) + '\n'
# + '# of unique proteins in the target lines: ' + str(len(list(set(biogrid_target_protein_IDs)))) + '\n')
# print(_str)
# statistics_file.write(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################

# First we must read the list of all interactions from a BioGrid dataset
# All intercations are stored in two lists each containing one end of each interaction.
# reading from processed data where repeated interactions are removed.

print('reading interaction file...\n')

bioGrid_File = open("PPI_without_repeats.txt", "r")
biogrid_source_protein_IDs = []
biogrid_target_protein_IDs = []
for line in bioGrid_File:
   biogrid_source_protein_IDs.append(line.split()[0])
   biogrid_target_protein_IDs.append(line.split()[1])

_str = ('the interaction file was read:' + '\n'
+ '# of lines in the PPI files read for source interacting proteins: ' + str(len(biogrid_source_protein_IDs)) + '\n'
+ '# of lines in the PPI files read for target interacting proteins: ' + str(len(biogrid_target_protein_IDs)) + '\n'
+ '# of unique proteins in the source lines: ' + str(len(list(set(biogrid_source_protein_IDs)))) + '\n'
+ '# of unique proteins in the target lines: ' + str(len(list(set(biogrid_target_protein_IDs)))) + '\n')
print(_str)
statistics_file.write(_str)

# ######################################################################################
# ######################################################################################
# ######################################################################################

# to check if some PPIs are repeated or no,
# if so, to check how many times each PPI is repeated.

# temp_counter = 0
# counter_0 = 0
# counter_1 = 0
# counter_2 = 0
# counter_3 = 0
# counter_4 = 0
# counter_5 = 0
# counter_6 = 0
# removing_indices = []
# counter_hash = {}
# for i in range(0, 100):
#    counter_hash[i] = 0
# n = len(biogrid_source_protein_IDs)
# for i in range(0, n):
#    if (i < n): # at each iteration, n may changes
#       if (i % 100 == 0):
#          print (round(i / n * 100, 1), '%', end="\r")
      
#       source_i = biogrid_source_protein_IDs[i]
#       target_i = biogrid_target_protein_IDs[i]
#       temp_counter = 0
#       removing_indices = []
#       for j in range(0,n):
#          if(i < j):
#             source_j = biogrid_source_protein_IDs[j]
#             target_j = biogrid_target_protein_IDs[j]     
#             if ( (source_i == source_j and target_i == target_j) or (source_i == target_j and source_j == target_i)):
#                removing_indices.append(j)
#                temp_counter += 1
#       for indx in sorted(removing_indices, reverse = True):
#          del biogrid_source_protein_IDs[indx] 
#          del biogrid_target_protein_IDs[indx]
#       n = len(biogrid_source_protein_IDs)
#       counter_hash[temp_counter] = counter_hash[temp_counter] + 1
#       if (temp_counter == 0):
#          counter_0 += 1   
#       if (temp_counter == 1):
#          counter_1 += 1
#       if (temp_counter == 2):
#          counter_2 += 1
#       if (temp_counter == 3):
#          counter_3 += 1
#       if (temp_counter == 4):
#          counter_4 += 1
#       if (temp_counter == 5):
#          counter_5 += 1
#       if (temp_counter == 6):
#          counter_6 += 1

# print(len(removing_indices))
# print(len(list(set(removing_indices))))

# n = len(biogrid_source_protein_IDs)
# with open('PPI_without_repeats.txt', 'w') as _file:
#    for i in range(0, n):
#       _file.write(biogrid_source_protein_IDs[i] + '\t' + biogrid_target_protein_IDs[i] + '\n')

# with open('Repeats_statistics.txt', 'w') as _file:
#    for key in counter_hash:
#       _file.write(str(key) + '\t' + str(counter_hash[key]) + '\n')
# quit()

# ######################################################################################
# ######################################################################################
# ######################################################################################


all_unique_proteins_in_biogrid = []
all_unique_proteins_in_biogrid.extend(biogrid_source_protein_IDs)
all_unique_proteins_in_biogrid.extend(biogrid_target_protein_IDs)

_str = '# of all_unique_proteins_in_biogrid: ' + str(len(list(set(all_unique_proteins_in_biogrid)))) + '\n'
print(_str)
statistics_file.write(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################


# Now we want to map each BioGrid ID (which is an Entrez Gene ID) to a standard UniProt ID
# 'P_ENTREZGENEID' is used to indicate that the corresponding ID is an Entrez Gene ID (GeneID)
# 'ID' is used to indicate that the corresponding ID is a UniProt ID
# note:  for each unique Entrez Gene ID there may exists several UniProt IDs!!!
#        We may interpret this event as: each protein reported in BioGrid DB, 
#        may be inserted to UniProt DB with some different studies around the world.

print('converting biogrid IDs to uniprot IDs...\n')

query = ' '.join(biogrid_source_protein_IDs)
biogrid_source_to_uniprot_IDs = convertIDs(query, 'P_ENTREZGENEID', 'ID')

_str = ('biogrid IDs are mapped to uniprot IDs:' + '\n'
+ '# of IDs returned by uniprot Mapper: ' + '\n'
+ 'Source: ' + '\n'
+ 'from: ' + str(len(biogrid_source_to_uniprot_IDs[0]))  + ', and to: ' +  str(len(biogrid_source_to_uniprot_IDs[1]))
+ ', and uniques --> from: ' + str(len(list(set(biogrid_source_to_uniprot_IDs[0])))) +', and to: ' +  str(len(list(set(biogrid_source_to_uniprot_IDs[1])))) + '\n')
print(_str)
statistics_file.write(_str)

query = ' '.join(biogrid_target_protein_IDs)
biogrid_target_to_uniprot_IDs = convertIDs(query, 'P_ENTREZGENEID', 'ID')

_str = ('biogrid IDs are mapped to uniprot IDs:' + '\n'
+ '# of IDs returned by uniprot Mapper: ' + '\n'
+ 'Target: ' + '\n'
+ 'from: ' + str(len(biogrid_target_to_uniprot_IDs[0]))  + ', and to: ' +  str(len(biogrid_target_to_uniprot_IDs[1]))
+ ', and uniques --> from: ' + str(len(list(set(biogrid_target_to_uniprot_IDs[0]))))  + ', and to: ' +  str(len(list(set(biogrid_target_to_uniprot_IDs[1])))) + '\n')
print(_str)
statistics_file.write(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################


all_biogrid_proteins_having_at_least_an_ID_in_uniprot = []
all_biogrid_proteins_having_at_least_an_ID_in_uniprot.extend(biogrid_source_to_uniprot_IDs[0])
all_biogrid_proteins_having_at_least_an_ID_in_uniprot.extend(biogrid_target_to_uniprot_IDs[0])

all_uniprot_IDs_obtained_by_mapping_biogrid_to_uniprot = []
all_uniprot_IDs_obtained_by_mapping_biogrid_to_uniprot.extend(biogrid_source_to_uniprot_IDs[1])
all_uniprot_IDs_obtained_by_mapping_biogrid_to_uniprot.extend(biogrid_target_to_uniprot_IDs[1])

_str = ('# of all_biogrid_proteins_having_at_least_an_ID_in_uniprot: '
+ str(len(list(set(all_biogrid_proteins_having_at_least_an_ID_in_uniprot)))) + '\n'
+ '# of all_uniprot_IDs_obtained_by_mapping_biogrid_to_uniprot: '
+ str(len(list(set(all_uniprot_IDs_obtained_by_mapping_biogrid_to_uniprot)))) + '\n')
print(_str)
statistics_file.write(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################


# Now we want to map each UniProt ID to a FlyBase ID
# 'FLYBASE_ID' is used to indicate that the corresponding ID is a FlyBase ID
# 'ID' is used to indicate that the corresponding ID is a UniProt ID
# note:  for each unique UniProt ID there may exists several FlyBase IDs!!!
#        We may interpret this event as: each protein may be synthesised by
#        different genes in a gene family.

print('converting uniprot IDs to flybase IDs...\n')

uniprot_of_source_protein_IDs = biogrid_source_to_uniprot_IDs[1]
query = ' '.join(uniprot_of_source_protein_IDs)
uniprot_of_source_to_flybase_IDs = convertIDs(query, 'ID', 'FLYBASE_ID')

_str = ('uniprot IDs are mapped to flybase IDs:' + '\n'
+ '# of IDs returned by uniprot Mapper: ' + '\n'
+ 'Source: ' + '\n'
+ 'from: ' + str(len(uniprot_of_source_to_flybase_IDs[0]))  + ', and to: ' +  str(len(uniprot_of_source_to_flybase_IDs[1]))
+ ', and uniques --> from: ' + str(len(list(set(uniprot_of_source_to_flybase_IDs[0])))) +', and to: ' +  str(len(list(set(uniprot_of_source_to_flybase_IDs[1])))) + '\n')
print(_str)
statistics_file.write(_str)

uniprot_of_target_protein_IDs = biogrid_target_to_uniprot_IDs[1]
query = ' '.join(uniprot_of_target_protein_IDs)
uniprot_of_target_to_flybase_IDs = convertIDs(query, 'ID', 'FLYBASE_ID')

_str = ('uniprot IDs are mapped to flybase IDs:' + '\n'
+ '# of IDs returned by uniprot Mapper: ' + '\n'
+ 'Target: ' + '\n'
+ 'from: ' + str(len(uniprot_of_target_to_flybase_IDs[0]))  + ', and to: ' +  str(len(uniprot_of_target_to_flybase_IDs[1]))
+ ', and uniques --> from: ' + str(len(list(set(uniprot_of_target_to_flybase_IDs[0])))) +', and to: ' +  str(len(list(set(uniprot_of_target_to_flybase_IDs[1])))) + '\n')
print(_str)
statistics_file.write(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################


all_uniprot_proteins_having_at_least_an_ID_in_flybase = []
all_uniprot_proteins_having_at_least_an_ID_in_flybase.extend(uniprot_of_source_to_flybase_IDs[0])
all_uniprot_proteins_having_at_least_an_ID_in_flybase.extend(uniprot_of_target_to_flybase_IDs[0])

all_flybase_IDs_obtained_by_mapping_uniprot_to_flybase = []
all_flybase_IDs_obtained_by_mapping_uniprot_to_flybase.extend(uniprot_of_source_to_flybase_IDs[1])
all_flybase_IDs_obtained_by_mapping_uniprot_to_flybase.extend(uniprot_of_target_to_flybase_IDs[1])

_str = ('# of all_uniprot_proteins_having_at_least_an_ID_in_flybase: '
+ str(len(list(set(all_uniprot_proteins_having_at_least_an_ID_in_flybase)))) + '\n'
+ '# of all_flybase_IDs_obtained_by_mapping_uniprot_to_flybase: '
+ str(len(list(set(all_flybase_IDs_obtained_by_mapping_uniprot_to_flybase)))) + '\n')
print(_str)
statistics_file.write(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################


biogrid_source_to_uniprot_hash = {}
biogrid_target_to_uniprot_hash = {}
all_biogrid_to_uniprot_hash = {}

# for x in list(set(biogrid_source_to_uniprot_IDs[0])):
for x in list(set(biogrid_source_protein_IDs)):
   biogrid_source_to_uniprot_hash[x] = []
   all_biogrid_to_uniprot_hash[x] = []

n = len(biogrid_source_to_uniprot_IDs[0])
for i in range(0, n): 
   biogrid_source_to_uniprot_hash[biogrid_source_to_uniprot_IDs[0][i]].append(biogrid_source_to_uniprot_IDs[1][i])
   all_biogrid_to_uniprot_hash[biogrid_source_to_uniprot_IDs[0][i]].append(biogrid_source_to_uniprot_IDs[1][i])

# for x in list(set(biogrid_target_to_uniprot_IDs[0])):
for x in list(set(biogrid_target_protein_IDs)):
   biogrid_target_to_uniprot_hash[x] = []
   all_biogrid_to_uniprot_hash[x] = []

n = len(biogrid_target_to_uniprot_IDs[0])
for i in range(0, n): 
   biogrid_target_to_uniprot_hash[biogrid_target_to_uniprot_IDs[0][i]].append(biogrid_target_to_uniprot_IDs[1][i])
   all_biogrid_to_uniprot_hash[biogrid_target_to_uniprot_IDs[0][i]].append(biogrid_target_to_uniprot_IDs[1][i])

_temp = list(all_biogrid_to_uniprot_hash.keys())
_str = ('# of all_biogrid_to_uniprot_hash_keys_length: ' + str(len(_temp))
+ ', and unique: ' + str(len(list(set(_temp)))))
print(_str)
statistics_file.write(_str)

biogrid_proteins_having_no_intersection_in_their_corresponding_map_in_uniprot = []
biogrid_proteins_having_intersection_in_their_corresponding_map_in_uniprot = []
biogrid_proteins_having_the_same_corresponding_map_in_uniprot = []

all_counter = [0, 0]
no_intersection_counter = [0, 0]
with_intersection_counter = [0, 0]
the_same_counter = [0, 0]

for key in all_biogrid_to_uniprot_hash:
   lst_1 = list(set(all_biogrid_to_uniprot_hash[key]))
   if (len(lst_1) == 1):
      all_counter[0] += 1
   if (len(lst_1) > 1):
      all_counter[1] += 1
   flag = True
   for key_2 in all_biogrid_to_uniprot_hash:      
      if (key != key_2):
         lst_2 = list(set(all_biogrid_to_uniprot_hash[key_2]))
         lst_3 = [value for value in lst_1 if value in lst_2]
         if (len(lst_3) > 0):
            flag = False
            biogrid_proteins_having_intersection_in_their_corresponding_map_in_uniprot.append(key)
            if (len(lst_3) == 1):
               with_intersection_counter[0] += 1
            if (len(lst_3) > 1):
               with_intersection_counter[1] += 1

            if (len(lst_3) == len(lst_1) or len(lst_3) == len(lst_2)):
               biogrid_proteins_having_the_same_corresponding_map_in_uniprot.append(key)
               if (len(lst_3) == 1):
                  the_same_counter[0] += 1
               if (len(lst_3) > 1):
                  the_same_counter[1] += 1
   if (flag and len(lst_1) > 0):
      biogrid_proteins_having_no_intersection_in_their_corresponding_map_in_uniprot.append(key)
      if (len(lst_1) == 1):
         no_intersection_counter[0] += 1
      if (len(lst_1) > 1):
         no_intersection_counter[1] += 1

print(str(all_counter[0]) + '\t' + str(all_counter[1]))

_str = ('# of biogrid_proteins_having_no_intersection_in_their_corresponding_map_in_uniprot: '
+ str(len(biogrid_proteins_having_no_intersection_in_their_corresponding_map_in_uniprot))
+ ', and uniques: ' + str(len(list(set(biogrid_proteins_having_no_intersection_in_their_corresponding_map_in_uniprot)))) + '\n'
+ 'mapped to exactly on ID: ' + str(no_intersection_counter[0]) + '\t' + 'mapped to more than one ID: ' + str(no_intersection_counter[1]))
print(_str)
statistics_file.write(_str)

_str = ('# of biogrid_proteins_having_intersection_in_their_corresponding_map_in_uniprot: '
+ str(len(biogrid_proteins_having_intersection_in_their_corresponding_map_in_uniprot))
+ ', and uniques: ' + str(len(list(set(biogrid_proteins_having_intersection_in_their_corresponding_map_in_uniprot)))) + '\n'
+ 'mapped to exactly on ID: ' + str(with_intersection_counter[0]) + '\t' + 'mapped to more than one ID: ' + str(with_intersection_counter[1]))
print(_str)
statistics_file.write(_str)

_str = ('# of biogrid_proteins_having_the_same_corresponding_map_in_uniprot: '
+ str(len(biogrid_proteins_having_the_same_corresponding_map_in_uniprot))
+ ', and uniques: ' + str(len(list(set(biogrid_proteins_having_the_same_corresponding_map_in_uniprot)))) + '\n'
+ 'mapped to exactly on ID: ' + str(the_same_counter[0]) + '\t' + 'mapped to more than one ID: ' + str(the_same_counter[1]))
print(_str)
statistics_file.write(_str)
quit()

# ######################################################################################
# ######################################################################################
# ######################################################################################


uniprot_of_source_to_flybase_hash = {}
uniprot_of_target_to_flybase_hash = {}
all_uniprot_to_flybase_hash = {}

for x in list(set(biogrid_source_to_uniprot_IDs[1])):
   uniprot_of_source_to_flybase_hash[x] = []
   all_uniprot_to_flybase_hash[x] = []

n = len(uniprot_of_source_to_flybase_IDs[0])
for i in range(0, n): 
   uniprot_of_source_to_flybase_hash[uniprot_of_source_to_flybase_IDs[0][i]].append(uniprot_of_source_to_flybase_IDs[1][i])
   all_uniprot_to_flybase_hash[uniprot_of_source_to_flybase_IDs[0][i]].append(uniprot_of_source_to_flybase_IDs[1][i])

for x in list(set(biogrid_target_to_uniprot_IDs[1])):
   uniprot_of_target_to_flybase_hash[x] = []
   all_uniprot_to_flybase_hash[x] = []

n = len(uniprot_of_target_to_flybase_IDs[0])
for i in range(0, n): 
   uniprot_of_target_to_flybase_hash[uniprot_of_target_to_flybase_IDs[0][i]].append(uniprot_of_target_to_flybase_IDs[1][i])
   all_uniprot_to_flybase_hash[uniprot_of_target_to_flybase_IDs[0][i]].append(uniprot_of_target_to_flybase_IDs[1][i])

_temp = list(all_uniprot_to_flybase_hash.keys())
_str = ('# of all_uniprot_to_flybase_hash_keys_length: ' + str(len(_temp))
+ ', and unique: ' + str(len(list(set(_temp)))))
print(_str)
statistics_file.write(_str)

uniprot_entries_having_no_intersection_in_their_corresponding_map_in_flybase = []
uniprot_entries_having_intersection_in_their_corresponding_map_in_flybase = []
uniprot_entries_having_the_same_corresponding_map_in_flybase = []
for key in all_uniprot_to_flybase_hash:
   lst_1 = all_uniprot_to_flybase_hash[key]
   flag = True
   for key_2 in all_uniprot_to_flybase_hash:      
      if (key != key_2):
         lst_2 = all_uniprot_to_flybase_hash[key_2]
         lst_3 = [value for value in lst_1 if value in lst_2]
         if (len(lst_3) > 0):
            flag = False
            uniprot_entries_having_intersection_in_their_corresponding_map_in_flybase.append(key)
            if (len(lst_3) == len(lst_1) or len(lst_3) == len(lst_2)):
               uniprot_entries_having_the_same_corresponding_map_in_flybase.append(key)
   if (flag and len(lst_1) > 0):
      uniprot_entries_having_no_intersection_in_their_corresponding_map_in_flybase.append(key)

_str = ('# of uniprot_entries_having_no_intersection_in_their_corresponding_map_in_flybase: '
+ str(len(uniprot_entries_having_no_intersection_in_their_corresponding_map_in_flybase))
+ ', and uniques: ' + str(len(list(set(uniprot_entries_having_no_intersection_in_their_corresponding_map_in_flybase)))) + '\n')
print(_str)
statistics_file.write(_str)

_str = ('# of uniprot_entries_having_intersection_in_their_corresponding_map_in_flybase: '
+ str(len(uniprot_entries_having_intersection_in_their_corresponding_map_in_flybase))
+ ', and uniques: ' + str(len(list(set(uniprot_entries_having_intersection_in_their_corresponding_map_in_flybase)))) + '\n')
print(_str)
statistics_file.write(_str)

_str = ('# of uniprot_entries_having_the_same_corresponding_map_in_flybase: '
+ str(len(uniprot_entries_having_the_same_corresponding_map_in_flybase))
+ ', and uniques: ' + str(len(list(set(uniprot_entries_having_the_same_corresponding_map_in_flybase)))) + '\n')
print(_str)
statistics_file.write(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################


biogrid_source_to_flybase_hash = {}
biogrid_target_to_flybase_hash = {}
all_biogrid_to_flybase_hash = {}

for x in list(set(biogrid_source_to_uniprot_IDs[0])):
   biogrid_source_to_flybase_hash[x] = []
   all_biogrid_to_flybase_hash[x] = []

for x in list(set(biogrid_source_to_uniprot_IDs[0])):
   for y in biogrid_source_to_uniprot_hash[x]:
      biogrid_source_to_flybase_hash[x].extend(uniprot_of_source_to_flybase_hash[y])
      all_biogrid_to_flybase_hash[x].extend(uniprot_of_source_to_flybase_hash[y])

for x in list(set(biogrid_target_to_uniprot_IDs[0])):
   biogrid_target_to_flybase_hash[x] = []
   all_biogrid_to_flybase_hash[x] = []

for x in list(set(biogrid_target_to_uniprot_IDs[0])):
   for y in biogrid_target_to_uniprot_hash[x]:
      biogrid_target_to_flybase_hash[x].extend(uniprot_of_target_to_flybase_hash[y])
      all_biogrid_to_flybase_hash[x].extend(uniprot_of_target_to_flybase_hash[y])

_temp = list(all_biogrid_to_flybase_hash.keys())
_str = ('# of all_biogrid_to_flybase_hash_keys_length: ' + str(len(_temp))
+ ', and unique: ' + str(len(list(set(_temp)))))
print(_str)
statistics_file.write(_str)

biogrid_proteins_having_no_intersection_in_their_corresponding_map_in_flybase = []
biogrid_proteins_having_intersection_in_their_corresponding_map_in_flybase = []
biogrid_proteins_having_the_same_corresponding_map_in_flybase = []
for key in all_biogrid_to_flybase_hash:
   lst_1 = all_biogrid_to_flybase_hash[key]
   flag = True
   for key_2 in all_biogrid_to_flybase_hash:      
      if (key != key_2):
         lst_2 = all_biogrid_to_flybase_hash[key_2]
         lst_3 = [value for value in lst_1 if value in lst_2]
         if (len(lst_3) > 0):
            flag = False
            biogrid_proteins_having_intersection_in_their_corresponding_map_in_flybase.append(key)
            if (len(lst_3) == len(lst_1) or len(lst_3) == len(lst_2)):
               biogrid_proteins_having_the_same_corresponding_map_in_flybase.append(key)
   if (flag and len(lst_1) > 0):
      biogrid_proteins_having_no_intersection_in_their_corresponding_map_in_flybase.append(key)

_str = ('# of biogrid_proteins_having_no_intersection_in_their_corresponding_map_in_flybase: '
+ str(len(biogrid_proteins_having_no_intersection_in_their_corresponding_map_in_flybase))
+ ', and uniques: ' + str(len(list(set(biogrid_proteins_having_no_intersection_in_their_corresponding_map_in_flybase)))) + '\n')
print(_str)
statistics_file.write(_str)

_str = ('# of biogrid_proteins_having_intersection_in_their_corresponding_map_in_flybase: '
+ str(len(biogrid_proteins_having_intersection_in_their_corresponding_map_in_flybase))
+ ', and uniques: ' + str(len(list(set(biogrid_proteins_having_intersection_in_their_corresponding_map_in_flybase)))) + '\n')
print(_str)
statistics_file.write(_str)

_str = ('# of biogrid_proteins_having_the_same_corresponding_map_in_flybase: '
+ str(len(biogrid_proteins_having_the_same_corresponding_map_in_flybase))
+ ', and uniques: ' + str(len(list(set(biogrid_proteins_having_the_same_corresponding_map_in_flybase)))) + '\n')
print(_str)
statistics_file.write(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################


counter_0 = 0
counter_1 = 0
counter_geq_2 = 0
for key in all_biogrid_to_uniprot_hash:
   if (len(list(set(all_biogrid_to_uniprot_hash[key]))) == 0):
      counter_0 += 1
   elif (len(list(set(all_biogrid_to_uniprot_hash[key]))) == 1):
      counter_1 += 1
   elif (len(list(set(all_biogrid_to_uniprot_hash[key]))) > 1):
      counter_geq_2 += 1

_str = ('The statistics about how biogrid proeins are mapped to UniProt IDs: ' + '\n' 
+ '# of proteins having no corresponding ID): ' + str(counter_0) + '\n'
+ '# of proteins mapped to exactly one ID): ' + str(counter_1) + '\n'
+ '# of proteins having more than one corresponding ID): ' + str(counter_geq_2) + '\n')
print(_str)
statistics_file.write(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################


counter_0 = 0
counter_1 = 0
counter_geq_2 = 0
for key in all_uniprot_to_flybase_hash:
   if (len(list(set(all_uniprot_to_flybase_hash[key]))) > 1):
      counter_geq_2 += 1
      # print(key, all_uniprot_to_flybase_hash[key])
   if (len(list(set(all_uniprot_to_flybase_hash[key]))) == 0):
      counter_0 += 1
   if (len(list(set(all_uniprot_to_flybase_hash[key]))) == 1):
      counter_1 += 1

# print(len(uniprot_of_source_to_flybase_IDs[1]))
# print(len(list(set(uniprot_of_source_to_flybase_IDs[1]))))

_str = ('The statistics about how uniprot IDs are mapped to FlyBase IDs: ' + '\n' 
+ '# of proteins having no corresponding ID): ' + str(counter_0) + '\n'
+ '# of proteins mapped to exactly one ID): ' + str(counter_1) + '\n'
+ '# of proteins having more than one corresponding ID): ' + str(counter_geq_2) + '\n')
print(_str)
statistics_file.write(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################


counter_0 = 0
counter_1 = 0
counter_geq_2 = 0
biogrid_proteins_mapped_to_exactly_one_unique_ID = [[],[]]
unique_biogrid_to_flybase_hash = {}
_geq_2_list = []
for key in all_biogrid_to_flybase_hash:
   if (len(list(set(all_biogrid_to_flybase_hash[key]))) > 1):
      counter_geq_2 += 1
      _geq_2_list.extend(list(set(all_biogrid_to_flybase_hash[key])))
      # print(key, all_biogrid_to_flybase_hash[key])
   if (len(list(set(all_biogrid_to_flybase_hash[key]))) == 0):
      counter_0 += 1
   if (len(list(set(all_biogrid_to_flybase_hash[key]))) == 1):
      counter_1 += 1
      unique_biogrid_to_flybase_hash[key] = all_biogrid_to_flybase_hash[key][0]
      biogrid_proteins_mapped_to_exactly_one_unique_ID[0].append(key)
      biogrid_proteins_mapped_to_exactly_one_unique_ID[1].append(all_biogrid_to_flybase_hash[key][0])
      # It is possible that some proteins in bioGrid dataset are mapped into multiple IDs in uniprot. And only one of the many
      # uniprot IDs is mapped to a ID in flybase. We assume this ptoreing to be mapped to one unique ID in flybase.

_str = ('The statistics about how BioGrid IDs are mapped to FlyBase IDs: ' + '\n' 
+ '# of proteins having no corresponding ID): ' + str(counter_0) + '\n'
+ '# of proteins mapped to exactly one ID): ' + str(counter_1) + '\n'
+ '# of proteins having more than one corresponding ID): ' + str(counter_geq_2) + '\n')
print(_str)
statistics_file.write(_str)

# print(len(biogrid_proteins_mapped_to_exactly_one_unique_ID[0]))
# print(len(list(set(biogrid_proteins_mapped_to_exactly_one_unique_ID[0]))))

_counter = 0
for x in biogrid_proteins_mapped_to_exactly_one_unique_ID[1]:
   counter = 0
   for y in biogrid_proteins_mapped_to_exactly_one_unique_ID[1]:
      if (x == y):
         counter += 1
   if (counter > 1):
      _counter += 1
print(_counter)

n = len(biogrid_proteins_mapped_to_exactly_one_unique_ID[0])
with open('output.txt', 'a') as _file:
   for i in range(0, n):
      _file.write(biogrid_proteins_mapped_to_exactly_one_unique_ID[0][i] + '\t' + biogrid_proteins_mapped_to_exactly_one_unique_ID[1][i] + '\n')

n = len(biogrid_source_protein_IDs)
with open('biogrid.PPI.Network.using.flybase.IDs.txt', 'a') as _file:
   for i in range(0, n):
      if (unique_biogrid_to_flybase_hash.get(biogrid_source_protein_IDs[i], False) and unique_biogrid_to_flybase_hash.get(biogrid_target_protein_IDs[i], False)):
         _file.write(unique_biogrid_to_flybase_hash[biogrid_source_protein_IDs[i]] + '\t' +
            unique_biogrid_to_flybase_hash[biogrid_target_protein_IDs[i]] + '\n')

# ######################################################################################
# ######################################################################################
# ######################################################################################


# i = 0
# for x in uniprot_of_source_to_flybase_IDs[1]:
#    counter = 0
#    j = 0
#    for y in uniprot_of_source_to_flybase_IDs[1]:
#       if (x == y and biogrid_source_to_uniprot_IDs[0][i] != biogrid_source_to_uniprot_IDs[0][j]):
#          counter += 1
#       j += 1
#    # if (counter > 1):
#       # print('i: ' + str(i))
#    i += 1

# ######################################################################################
# ######################################################################################
# ######################################################################################
