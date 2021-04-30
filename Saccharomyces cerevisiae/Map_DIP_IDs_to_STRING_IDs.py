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


# First we must read the list of all interactions from a DIP dataset
# All intercations are stored in two lists each containing one end of each interaction.
# reading from processed data where repeated interactions are removed.

print('reading interaction file...\n')

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


# Now we want to map each DIP ID (which is a standard UniProt ID) to a SRTING ID
# 'ID' is used to indicate that the corresponding ID is a UniProt ID
# 'STRING_ID' is used to indicate that the corresponding ID is a STRING ID

print('converting DIP IDs to STRING IDs...\n')

query = ' '.join(all_unique_proteins_in_DIP)
DIP_to_STRING_IDs = convertIDs(query, 'ID', 'STRING_ID')

_str = ('DIP IDs are mapped to STRING IDs:' + '\n'
+ '# of IDs returned by uniprot Mapper: ' + '\n'
+ 'from: ' + str(len(DIP_to_STRING_IDs[0]))  + ', and to: ' +  str(len(DIP_to_STRING_IDs[1]))
+ ', and uniques --> from: ' + str(len(list(set(DIP_to_STRING_IDs[0])))) +', and to: ' +  str(len(list(set(DIP_to_STRING_IDs[1])))) + '\n')
print(_str)

# ######################################################################################
# ######################################################################################
# ######################################################################################

# writing PPIs with their corresponding UniPropt ID into a file.

DIP_to_STRING_hash = {}
counter = 0

for protein_ID in all_unique_proteins_in_DIP:
    DIP_to_STRING_hash[protein_ID] = []
n = len(DIP_to_STRING_IDs[0])
for i in range(0, n):
    if (DIP_to_STRING_IDs[1][i].split('.')[0] == '4932'):
        counter += 1
        DIP_to_STRING_hash[DIP_to_STRING_IDs[0][i]].append(DIP_to_STRING_IDs[1][i].split('.')[1])
print('counter: ', counter)
counter_0 = 0
counter_1 = 0
counter_2 = 0
counter_3 = 0
counter_4 = 0
counter_5 = 0
counter_geq_6 = 0

for key in DIP_to_STRING_hash:
    if (len(list(set(DIP_to_STRING_hash[key]))) == 0):
        counter_0 += 1
    if (len(list(set(DIP_to_STRING_hash[key]))) == 1):
        counter_1 += 1
    if (len(list(set(DIP_to_STRING_hash[key]))) == 2):
        counter_2 += 1
    if (len(list(set(DIP_to_STRING_hash[key]))) == 3):
        counter_3 += 1
    if (len(list(set(DIP_to_STRING_hash[key]))) == 4):
        counter_4 += 1
    if (len(list(set(DIP_to_STRING_hash[key]))) == 5):
        counter_5 += 1
    if (len(list(set(DIP_to_STRING_hash[key]))) > 5):
        counter_geq_6 += 1
print(counter_0, counter_1, counter_2, counter_3, counter_4, counter_5, counter_geq_6)



DEG_File = open("F:\\Courses\\Graph perturbation\\Data\\DEG raw data\\Downloaded on 11 25 2019\\S. cerevisiae\\Saccharomyces cerevisiae_all.txt", "r") 
DEG_IDs = []
DEG_Essentiality = []
for line in DEG_File:
   DEG_IDs.append(line.split('\t')[2])
   DEG_Essentiality.append(line.split('\t')[3])

print(len(DEG_IDs))
print(len(list(set(DEG_IDs))))

DEG_IDs_hash = {}
n = len(DEG_IDs)
for i in range(0, n):
    DEG_IDs_hash[DEG_IDs[i]] = []
for i in range(0, n):
    DEG_IDs_hash[DEG_IDs[i]].append(DEG_Essentiality[i])

DEG_IDs_N_Essentiality = {}
number_of_essential_genes = 0
number_of_non_essential_genes = 0
number_of_unknown_genes = 0
for key in DEG_IDs_hash: 
    _list = DEG_IDs_hash[key]
    NE_counter = 0
    E_counter = 0
    for item in _list:
        if (item == 'NE'):
            NE_counter += 1
        elif (item == 'E'):
            E_counter += 1
        # else:
        #     print('Error', 'item: ', item)
    if (NE_counter > E_counter):
        DEG_IDs_N_Essentiality[key] = 'NE'
        number_of_non_essential_genes += 1
    elif (NE_counter < E_counter):
        DEG_IDs_N_Essentiality[key] = 'E'
        number_of_essential_genes += 1
    else:
        DEG_IDs_N_Essentiality[key] = 'U'
        number_of_unknown_genes += 1
print(number_of_essential_genes, '\t', number_of_non_essential_genes, '\t', number_of_unknown_genes)

with open('DIP\\output\\DIP_IDs_N_Essentiality.txt', 'w') as _file:
    for protein_ID in all_unique_proteins_in_DIP:
        if (len(list(set(DIP_to_STRING_hash[protein_ID]))) == 1):
            _mapped_STRING_ID = DIP_to_STRING_hash[protein_ID][0]
            if (_mapped_STRING_ID in DEG_IDs_N_Essentiality.keys()):
                _file.write(protein_ID + '\t' + DEG_IDs_N_Essentiality[_mapped_STRING_ID] + '\n')
            else: 
                _file.write(protein_ID + '\t' + 'U' + '\n')
        else:
            _file.write(protein_ID + '\t' + 'U' + '\n')