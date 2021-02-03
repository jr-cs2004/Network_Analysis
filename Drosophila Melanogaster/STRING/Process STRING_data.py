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

# First we must read the list of all interactions from a STRING dataset
# All intercations are stored in two lists each containing one end of each interaction.

print('reading interaction file...\n')

STRING_File = open("7227.protein.links.v11.0.txt", "r")
STRING_source_protein_IDs = []
STRING_target_protein_IDs = []
counter = 0
for line in STRING_File:
   counter += 1
   if (counter == 1): 
      continue
   if (int(line.split()[2]) > 900):
      source = line.split()[0]
      target = line.split()[1]
      STRING_source_protein_IDs.append(source)
      STRING_target_protein_IDs.append(target)

_str = ('the interaction file was read:' + '\n'
+ '# of lines in the PPI files read for source interacting proteins: ' + str(len(STRING_source_protein_IDs)) + '\n'
+ '# of lines in the PPI files read for target interacting proteins: ' + str(len(STRING_target_protein_IDs)) + '\n'
+ '# of unique proteins in the source lines: ' + str(len(list(set(STRING_source_protein_IDs)))) + '\n'
+ '# of unique proteins in the target lines: ' + str(len(list(set(STRING_target_protein_IDs)))) + '\n')
print(_str)
statistics_file.write(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################

# to check if some PPIs are repeated or no,
# if so, to check how many times each PPI is repeated.

temp_counter = 0
counter_0 = 0
counter_1 = 0
counter_2 = 0
counter_3 = 0
counter_4 = 0
counter_5 = 0
counter_6 = 0
loop_counter = 0
removing_indices = []
counter_hash = {}
for i in range(0, 100):
   counter_hash[i] = 0
n = len(STRING_source_protein_IDs)
for i in range(0, n):
   source_i = STRING_source_protein_IDs[i]
   target_i = STRING_target_protein_IDs[i]
   if (source_i == target_i):
      loop_counter += 1
      removing_indices.append(i)
print('# of self loops: ', loop_counter)

# removing self loops interactions.
for indx in sorted(removing_indices, reverse = True):
   del STRING_source_protein_IDs[indx] 
   del STRING_target_protein_IDs[indx]

n = len(STRING_source_protein_IDs)
for i in range(0, n):
   if (i < n): # at each iteration, n may changes
      if (i % 100 == 0):
         print (round(i / n * 100, 1), '%', end="\r")
      
      source_i = STRING_source_protein_IDs[i]
      target_i = STRING_target_protein_IDs[i]
      temp_counter = 0
      removing_indices = []
      for j in range(0,n):
         if(i < j):
            source_j = STRING_source_protein_IDs[j]
            target_j = STRING_target_protein_IDs[j]     
            if ( (source_i == source_j and target_i == target_j) or (source_i == target_j and source_j == target_i)):
               removing_indices.append(j)
               temp_counter += 1
      for indx in sorted(removing_indices, reverse = True):
         del STRING_source_protein_IDs[indx] 
         del STRING_target_protein_IDs[indx]
      n = len(STRING_source_protein_IDs)
      counter_hash[temp_counter] = counter_hash[temp_counter] + 1
      if (temp_counter == 0):
         counter_0 += 1   
      if (temp_counter == 1):
         counter_1 += 1
      if (temp_counter == 2):
         counter_2 += 1
      if (temp_counter == 3):
         counter_3 += 1
      if (temp_counter == 4):
         counter_4 += 1
      if (temp_counter == 5):
         counter_5 += 1
      if (temp_counter == 6):
         counter_6 += 1

print(len(removing_indices))
print(len(list(set(removing_indices))))

n = len(STRING_source_protein_IDs)
with open('PPI_without_repeats_threshold_900.txt', 'w') as _file:
   for i in range(0, n):
      _file.write(STRING_source_protein_IDs[i] + '\t' + STRING_target_protein_IDs[i] + '\n')

with open('Repeats_statistics_threshold_900.txt', 'w') as _file:
   for key in counter_hash:
      _file.write(str(key) + '\t' + str(counter_hash[key]) + '\n')


# ######################################################################################
# ######################################################################################
# ######################################################################################


unique_proteins_in_STRING = []
unique_proteins_in_STRING.extend(STRING_source_protein_IDs)
unique_proteins_in_STRING.extend(STRING_target_protein_IDs)
unique_proteins_in_STRING = list(set(unique_proteins_in_STRING))
_str = '# of unique_proteins_in_STRING: ' + str(len(list(set(unique_proteins_in_STRING)))) + '\n'
print(_str)
statistics_file.write(_str)

# ######################################################################################
# ######################################################################################
# ######################################################################################


# Now we want to map each STRING ID (which is a UniPort ID) to a FlyBase ID
# 'FLYBASE_ID' is used to indicate that the corresponding ID is a FlyBase ID
# 'ID' is used to indicate that the corresponding ID is a UniProt ID
# note:  for each unique UniProt ID there may exists several FlyBase IDs!!!
#        We may interpret this event as: each protein may be synthesised by
#        different genes in a gene family.

print('converting STRING IDs to flybase IDs...\n')

query = ' '.join(unique_proteins_in_STRING)
STRING_to_flybase_IDs = convertIDs(query, 'STRING_ID', 'ID')

_str = ('STRING IDs are mapped to flybase IDs:' + '\n'
+ '# of IDs returned by uniprot Mapper: ' + '\n'
+ 'from: ' + str(len(STRING_to_flybase_IDs[0])) + ', and to: ' + str(len(STRING_to_flybase_IDs[1]))
+ ', and uniques --> from: ' + str(len(list(set(STRING_to_flybase_IDs[0])))) +', and to: ' +  str(len(list(set(STRING_to_flybase_IDs[1])))) + '\n')
print(_str)
statistics_file.write(_str)


_str = ('# of STRING_proteins_having_at_least_an_ID_in_flybase: '
+ str(len(list(set(STRING_to_flybase_IDs[0])))) + '\n'
+ '# of flybase_IDs_obtained_by_mapping_uniprot_to_flybase: '
+ str(len(list(set(STRING_to_flybase_IDs[1])))) + '\n')
print(_str)
statistics_file.write(_str)
