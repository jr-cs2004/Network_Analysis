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


# statistics_file = open('statistics.txt', 'a')

# # First we must read the list of all interactions from a intact dataset
# # All intercations are stored in two lists each containing one end of each interaction.

# print('reading interaction file...\n')

# IntAct_File = open("PPIs.txt", "r")
# intact_source_protein_IDs = []
# intact_target_protein_IDs = []
# counter = 0
# for line in IntAct_File:
#    counter += 1
#    source = line.split()[0]
#    target = line.split()[1]
#    intact_source_protein_IDs.append(source)
#    intact_target_protein_IDs.append(target)

# _str = ('the interaction file was read:' + '\n'
# + '# of lines in the PPI files read for source interacting proteins: ' + str(len(intact_source_protein_IDs)) + '\n'
# + '# of lines in the PPI files read for target interacting proteins: ' + str(len(intact_target_protein_IDs)) + '\n'
# + '# of unique proteins in the source lines: ' + str(len(list(set(intact_source_protein_IDs)))) + '\n'
# + '# of unique proteins in the target lines: ' + str(len(list(set(intact_target_protein_IDs)))) + '\n')
# print(_str)
# statistics_file.write(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################


statistics_file = open('statistics.txt', 'a')

# First we must read the list of all interactions from a intact dataset
# All intercations are stored in two lists each containing one end of each interaction.

print('reading interaction file...\n')

IntAct_File = open("PPI_without_repeats.txt", "r")
intact_source_protein_IDs = []
intact_target_protein_IDs = []
counter = 0
for line in IntAct_File:
   counter += 1
   source = line.split()[0]
   target = line.split()[1]
   intact_source_protein_IDs.append(source)
   intact_target_protein_IDs.append(target)

_str = ('the interaction file was read:' + '\n'
+ '# of lines in the PPI files read for source interacting proteins: ' + str(len(intact_source_protein_IDs)) + '\n'
+ '# of lines in the PPI files read for target interacting proteins: ' + str(len(intact_target_protein_IDs)) + '\n'
+ '# of unique proteins in the source lines: ' + str(len(list(set(intact_source_protein_IDs)))) + '\n'
+ '# of unique proteins in the target lines: ' + str(len(list(set(intact_target_protein_IDs)))) + '\n')
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
# loop_counter = 0
# removing_indices = []
# counter_hash = {}
# for i in range(0, 100):
#    counter_hash[i] = 0
# n = len(intact_source_protein_IDs)
# for i in range(0, n):
#    source_i = intact_source_protein_IDs[i]
#    target_i = intact_target_protein_IDs[i]
#    if (source_i == target_i):
#       loop_counter += 1
#       removing_indices.append(i)
# print('# of self loops: ', loop_counter)

# # removing self loops interactions.
# for indx in sorted(removing_indices, reverse = True):
#    del intact_source_protein_IDs[indx] 
#    del intact_target_protein_IDs[indx]

# n = len(intact_source_protein_IDs)
# for i in range(0, n):
#    if (i < n): # at each iteration, n may changes
#       if (i % 100 == 0):
#          print (round(i / n * 100, 1), '%', end="\r")
      
#       source_i = intact_source_protein_IDs[i]
#       target_i = intact_target_protein_IDs[i]
#       temp_counter = 0
#       removing_indices = []
#       for j in range(0,n):
#          if(i < j):
#             source_j = intact_source_protein_IDs[j]
#             target_j = intact_target_protein_IDs[j]     
#             if ( (source_i == source_j and target_i == target_j) or (source_i == target_j and source_j == target_i)):
#                removing_indices.append(j)
#                temp_counter += 1
#       for indx in sorted(removing_indices, reverse = True):
#          del intact_source_protein_IDs[indx] 
#          del intact_target_protein_IDs[indx]
#       n = len(intact_source_protein_IDs)
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

# n = len(intact_source_protein_IDs)
# with open('PPI_without_repeats.txt', 'w') as _file:
#    for i in range(0, n):
#       _file.write(intact_source_protein_IDs[i] + '\t' + intact_target_protein_IDs[i] + '\n')

# with open('Repeats_statistics.txt', 'w') as _file:
#    for key in counter_hash:
#       _file.write(str(key) + '\t' + str(counter_hash[key]) + '\n')


# ######################################################################################
# ######################################################################################
# ######################################################################################


unique_proteins_in_intact = []
unique_proteins_in_intact.extend(intact_source_protein_IDs)
unique_proteins_in_intact.extend(intact_target_protein_IDs)
unique_proteins_in_intact = list(set(unique_proteins_in_intact))
_str = '# of unique_proteins_in_intact: ' + str(len(list(set(unique_proteins_in_intact)))) + '\n'
print(_str)
statistics_file.write(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################


# Now we want to map each IntAct ID (which is a UniPort ID) to a FlyBase ID
# 'FLYBASE_ID' is used to indicate that the corresponding ID is a FlyBase ID
# 'ID' is used to indicate that the corresponding ID is a UniProt ID
# note:  for each unique UniProt ID there may exists several FlyBase IDs!!!
#        We may interpret this event as: each protein may be synthesised by
#        different genes in a gene family.

print('converting intact IDs to flybase IDs...\n')

query = ' '.join(unique_proteins_in_intact)
intact_to_flybase_IDs = convertIDs(query, 'ID', 'FLYBASE_ID')

_str = ('IntAct IDs are mapped to flybase IDs:' + '\n'
+ '# of IDs returned by uniprot Mapper: ' + '\n'
+ 'from: ' + str(len(intact_to_flybase_IDs[0])) + ', and to: ' + str(len(intact_to_flybase_IDs[1]))
+ ', and uniques --> from: ' + str(len(list(set(intact_to_flybase_IDs[0])))) +', and to: ' +  str(len(list(set(intact_to_flybase_IDs[1])))) + '\n')
print(_str)
statistics_file.write(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################


_str = ('# of intact_proteins_having_at_least_an_ID_in_flybase: '
+ str(len(list(set(intact_to_flybase_IDs[0])))) + '\n'
+ '# of flybase_IDs_obtained_by_mapping_uniprot_to_flybase: '
+ str(len(list(set(intact_to_flybase_IDs[1])))) + '\n')
print(_str)
statistics_file.write(_str)

# ######################################################################################
# ######################################################################################
# ######################################################################################


intact_to_flybase_hash = {}

for x in list(set(unique_proteins_in_intact)):
   intact_to_flybase_hash[x] = []

n = len(intact_to_flybase_IDs[0])
for i in range(0, n): 
   intact_to_flybase_hash[intact_to_flybase_IDs[0][i]].append(intact_to_flybase_IDs[1][i])

# this segment of code is just to test the correctness of the code
_temp = list(intact_to_flybase_hash.keys())
_str = ('# of intact_to_flybase_hash_keys_length: ' + str(len(_temp))
+ ', and unique: ' + str(len(list(set(_temp)))) + '\n')
print(_str)
statistics_file.write(_str)

intact_proteins_having_no_intersection_in_their_corresponding_map_in_flybase = []
intact_proteins_having_intersection_in_their_corresponding_map_in_flybase = []
intact_proteins_having_the_same_corresponding_map_in_flybase = []
for key in intact_to_flybase_hash:
   lst_1 = list(set(intact_to_flybase_hash[key]))
   flag = True
   for key_2 in intact_to_flybase_hash:
      lst_2 = list(set(intact_to_flybase_hash[key_2]))
      if (key != key_2):
         lst_3 = [value for value in lst_1 if value in lst_2]
         if (len(lst_3) > 0):
            flag = False
            intact_proteins_having_intersection_in_their_corresponding_map_in_flybase.append(key)
            if (len(lst_3) == len(lst_1) or len(lst_3) == len(lst_2)):
               intact_proteins_having_the_same_corresponding_map_in_flybase.append(key)      
   if (flag and len(lst_1) > 0):
      intact_proteins_having_no_intersection_in_their_corresponding_map_in_flybase.append(key)
_str = ('# of intact_proteins_having_no_intersection_in_their_corresponding_map_in_flybase: ' 
+ str(len(intact_proteins_having_no_intersection_in_their_corresponding_map_in_flybase)) 
+ ', and uniques: ' + str(len(list(set(intact_proteins_having_no_intersection_in_their_corresponding_map_in_flybase)))) + '\n')
print(_str)
statistics_file.write(_str)

_str = ('# of intact_proteins_having_intersection_in_their_corresponding_map_in_flybase: '
+ str(len(intact_proteins_having_intersection_in_their_corresponding_map_in_flybase))
+ ', and uniques: ' + str(len(list(set(intact_proteins_having_intersection_in_their_corresponding_map_in_flybase)))) + '\n')
print(_str)
statistics_file.write(_str)

_str = ('# of intact_proteins_having_the_same_corresponding_map_in_flybase: '
+ str(len(intact_proteins_having_the_same_corresponding_map_in_flybase))
+ ', and uniques: ' + str(len(list(set(intact_proteins_having_the_same_corresponding_map_in_flybase)))) + '\n')
print(_str)
statistics_file.write(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################


counter_0 = 0
counter_1 = 0
counter_geq_2 = 0
intact_proteins_mapped_to_exactly_one_unique_ID = [[],[]]
unique_intact_to_flybase_hash = {}

for key in intact_to_flybase_hash:
   if (len(list(set(intact_to_flybase_hash[key]))) == 0):
      counter_0 += 1
   elif (len(list(set(intact_to_flybase_hash[key]))) == 1):
      counter_1 += 1
      if (key in intact_proteins_having_no_intersection_in_their_corresponding_map_in_flybase or key in intact_proteins_having_the_same_corresponding_map_in_flybase):
         unique_intact_to_flybase_hash[key] = intact_to_flybase_hash[key][0]
         intact_proteins_mapped_to_exactly_one_unique_ID[0].append(key)
         intact_proteins_mapped_to_exactly_one_unique_ID[1].append(intact_to_flybase_hash[key][0])

   elif (len(list(set(intact_to_flybase_hash[key]))) > 1):
      counter_geq_2 += 1
      
_str = ('The statistics about how IntAct proeins are mapped to FlyBase IDs:' + '\n'
+ '# of proteins having no corresponding ID: ' + str(counter_0) + '\n'
+ '# of proteins mapped to exactly one ID: ' + str(counter_1) + '\n'
+ '# of proteins having more than one corresponding ID: ' + str(counter_geq_2) + '\n')
print(_str)
statistics_file.write(_str)

_str = ('# of unique proteins having only one corresponding flybase ID: '
+ str(len(intact_proteins_mapped_to_exactly_one_unique_ID[0]))
+ ', and unique: ' + str(len(list(set(intact_proteins_mapped_to_exactly_one_unique_ID[0])))) + '\n')
print(_str)
statistics_file.write(_str)

_counter = 0
for x in intact_proteins_mapped_to_exactly_one_unique_ID[1]:
   counter = 0
   for y in intact_proteins_mapped_to_exactly_one_unique_ID[1]:
      if (x == y):
         counter += 1
   if (counter > 1):
      _counter += 1
print('# of FlyBase IDs which are in common for atleast two IntAct proteins: ' ,_counter)

n = len(intact_proteins_mapped_to_exactly_one_unique_ID[0])
with open('intact.IDs.mapping.to.flybase.IDs.txt', 'a') as _file:
   for i in range(0, n):
      _file.write(intact_proteins_mapped_to_exactly_one_unique_ID[0][i] + '\t' + intact_proteins_mapped_to_exactly_one_unique_ID[1][i] + '\n')

n = len(intact_source_protein_IDs)
counter = 0
with open('intact.GGI.Network.Unique.txt', 'a') as _file:
   for i in range(0, n):
      if (unique_intact_to_flybase_hash.get(intact_source_protein_IDs[i], False) and unique_intact_to_flybase_hash.get(intact_target_protein_IDs[i], False)):
         _file.write(unique_intact_to_flybase_hash[intact_source_protein_IDs[i]] + '\t' +
            unique_intact_to_flybase_hash[intact_target_protein_IDs[i]] + '\n')
         counter += 1

_str = ('# of interactions using flybase ID: ' + str(counter) + '\n')
print(_str)
statistics_file.write(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################