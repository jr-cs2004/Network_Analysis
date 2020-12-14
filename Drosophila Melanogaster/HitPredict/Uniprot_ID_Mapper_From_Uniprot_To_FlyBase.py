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

hitPredict_File = open("D_melanogaster_interactions_without_header_lines.txt", "r")
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


all_unique_proteins_in_hitpredict = []
all_unique_proteins_in_hitpredict.extend(hitpredict_source_protein_IDs)
all_unique_proteins_in_hitpredict.extend(hitpredict_target_protein_IDs)

_str = '# of all_unique_proteins_in_hitpredict: ' + str(len(list(set(all_unique_proteins_in_hitpredict)))) + '\n'
print(_str)
statistics_file.write(_str)


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

query = ' '.join(hitpredict_source_protein_IDs)
hitpredict_source_to_flybase_IDs = convertIDs(query, 'ID', 'FLYBASE_ID')

_str = ('IntAct IDs are mapped to flybase IDs:' + '\n'
+ '# of IDs returned by uniprot Mapper: ' + '\n'
+ 'Source: ' + '\n'
+ 'from: ' + str(len(hitpredict_source_to_flybase_IDs[0]))  + ', and to: ' +  str(len(hitpredict_source_to_flybase_IDs[1]))
+ ', and uniques --> from: ' + str(len(list(set(hitpredict_source_to_flybase_IDs[0])))) +', and to: ' +  str(len(list(set(hitpredict_source_to_flybase_IDs[1])))) + '\n')
print(_str)
statistics_file.write(_str)

query = ' '.join(hitpredict_target_protein_IDs)
hitpredict_target_to_flybase_IDs = convertIDs(query, 'ID', 'FLYBASE_ID')

_str = ('IntAct IDs are mapped to flybase IDs:' + '\n'
+ '# of IDs returned by uniprot Mapper: ' + '\n'
+ 'Target: ' + '\n'
+ 'from: ' + str(len(hitpredict_target_to_flybase_IDs[0]))  + ', and to: ' +  str(len(hitpredict_target_to_flybase_IDs[1]))
+ ', and uniques --> from: ' + str(len(list(set(hitpredict_target_to_flybase_IDs[0]))))  + ', and to: ' +  str(len(list(set(hitpredict_target_to_flybase_IDs[1])))) + '\n')
print(_str)
statistics_file.write(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################


all_hitpredict_proteins_having_at_least_an_ID_in_flybase = []
all_hitpredict_proteins_having_at_least_an_ID_in_flybase.extend(hitpredict_source_to_flybase_IDs[0])
all_hitpredict_proteins_having_at_least_an_ID_in_flybase.extend(hitpredict_target_to_flybase_IDs[0])

all_flybase_IDs_obtained_by_mapping_uniprot_to_flybase = []
all_flybase_IDs_obtained_by_mapping_uniprot_to_flybase.extend(hitpredict_source_to_flybase_IDs[1])
all_flybase_IDs_obtained_by_mapping_uniprot_to_flybase.extend(hitpredict_target_to_flybase_IDs[1])

_str = ('# of all_hitpredict_proteins_having_at_least_an_ID_in_flybase: '
+ str(len(list(set(all_hitpredict_proteins_having_at_least_an_ID_in_flybase)))) + '\n'
+ '# of all_flybase_IDs_obtained_by_mapping_uniprot_to_flybase: '
+ str(len(list(set(all_flybase_IDs_obtained_by_mapping_uniprot_to_flybase)))) + '\n')
print(_str)
statistics_file.write(_str)

# ######################################################################################
# ######################################################################################
# ######################################################################################


hitpredict_source_to_flybase_hash = {}
hitpredict_target_to_flybase_hash = {}
all_hitpredict_to_flybase_hash = {}

# for x in list(set(hitpredict_source_to_flybase_IDs[0])):
for x in list(set(hitpredict_source_protein_IDs)):
   hitpredict_source_to_flybase_hash[x] = []
   all_hitpredict_to_flybase_hash[x] = []

n = len(hitpredict_source_to_flybase_IDs[0])
for i in range(0, n): 
   hitpredict_source_to_flybase_hash[hitpredict_source_to_flybase_IDs[0][i]].append(hitpredict_source_to_flybase_IDs[1][i])
   all_hitpredict_to_flybase_hash[hitpredict_source_to_flybase_IDs[0][i]].append(hitpredict_source_to_flybase_IDs[1][i])

# for x in list(set(hitpredict_target_to_flybase_IDs[0])):
for x in list(set(hitpredict_target_protein_IDs)):
   hitpredict_target_to_flybase_hash[x] = []
   all_hitpredict_to_flybase_hash[x] = []

n = len(hitpredict_target_to_flybase_IDs[0])
for i in range(0, n): 
   hitpredict_target_to_flybase_hash[hitpredict_target_to_flybase_IDs[0][i]].append(hitpredict_target_to_flybase_IDs[1][i])
   all_hitpredict_to_flybase_hash[hitpredict_target_to_flybase_IDs[0][i]].append(hitpredict_target_to_flybase_IDs[1][i])

_temp = list(all_hitpredict_to_flybase_hash.keys())
_str = ('# of all_hitpredict_to_flybase_hash_keys_length: ' + str(len(_temp))
+ ', and unique: ' + str(len(list(set(_temp)))))
print(_str)
statistics_file.write(_str)

hitpredict_proteins_having_no_intersection_in_their_corresponding_map_in_flybase = []
hitpredict_proteins_having_intersection_in_their_corresponding_map_in_flybase = []
hitpredict_proteins_having_the_same_corresponding_map_in_flybase = []
for key in all_hitpredict_to_flybase_hash:
   lst_1 = list(set(all_hitpredict_to_flybase_hash[key]))
   flag = True
   for key_2 in all_hitpredict_to_flybase_hash:
      lst_2 = list(set(all_hitpredict_to_flybase_hash[key_2]))
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
hitpredict_proteins_mapped_to_exactly_one_unique_ID = [[],[]]
unique_hitpredict_to_flybase_hash = {}

for key in all_hitpredict_to_flybase_hash:
   if (len(list(set(all_hitpredict_to_flybase_hash[key]))) == 0):
      counter_0 += 1
   elif (len(list(set(all_hitpredict_to_flybase_hash[key]))) == 1):
      counter_1 += 1
      if (key in hitpredict_proteins_having_no_intersection_in_their_corresponding_map_in_flybase):
         unique_hitpredict_to_flybase_hash[key] = all_hitpredict_to_flybase_hash[key][0]
         hitpredict_proteins_mapped_to_exactly_one_unique_ID[0].append(key)
         hitpredict_proteins_mapped_to_exactly_one_unique_ID[1].append(all_hitpredict_to_flybase_hash[key][0])

   elif (len(list(set(all_hitpredict_to_flybase_hash[key]))) > 1):
      counter_geq_2 += 1
      
_str = ('The statistics about how HitPredict proeins are mapped to FlyBase IDs: ' + '\n' 
+ '# of proteins having no corresponding ID): ' + str(counter_0) + '\n'
+ '# of proteins mapped to exactly one ID): ' + str(counter_1) + '\n'
+ '# of proteins having more than one corresponding ID): ' + str(counter_geq_2) + '\n')
print(_str)
statistics_file.write(_str)

_str = ('# of unique proteins having only one corresponding flybase ID: '
+ str(len(hitpredict_proteins_mapped_to_exactly_one_unique_ID[0]))
+ ', and unique: ' + str(len(list(set(hitpredict_proteins_mapped_to_exactly_one_unique_ID[0])))) + '\n')
print(_str)
statistics_file.write(_str)

_counter = 0
for x in hitpredict_proteins_mapped_to_exactly_one_unique_ID[1]:
   counter = 0
   for y in hitpredict_proteins_mapped_to_exactly_one_unique_ID[1]:
      if (x == y):
         counter += 1
   if (counter > 1):
      _counter += 1
print(_counter)

n = len(hitpredict_proteins_mapped_to_exactly_one_unique_ID[0])
with open('output.txt', 'a') as _file:
   for i in range(0, n):
      _file.write(hitpredict_proteins_mapped_to_exactly_one_unique_ID[0][i] + '\t' + hitpredict_proteins_mapped_to_exactly_one_unique_ID[1][i] + '\n')

n = len(hitpredict_source_protein_IDs)
counter = 0
with open('hitpredict.PPI.Network.using.flybase.IDs.txt', 'a') as _file:
   for i in range(0, n):
      if (unique_hitpredict_to_flybase_hash.get(hitpredict_source_protein_IDs[i], False) and unique_hitpredict_to_flybase_hash.get(hitpredict_target_protein_IDs[i], False)):
         _file.write(unique_hitpredict_to_flybase_hash[hitpredict_source_protein_IDs[i]] + '\t' +
            unique_hitpredict_to_flybase_hash[hitpredict_target_protein_IDs[i]] + '\n')
         counter += 1

_str = ('# of interactions using flybase ID: ' + str(counter) + '\n')
print(_str)
statistics_file.write(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################