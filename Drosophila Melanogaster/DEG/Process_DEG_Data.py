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
        'query': 'organism:Drosophila melanogaster',
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
   
DEG_file = open("gene_names.txt", "r")

gene_names = []
for line in DEG_file:
   gene_names.append(line.split()[0])

gene_names = list(set(gene_names))
print('# of unique genes: ' + str(len(gene_names)) + '\n')

# ######################################################################################
# ######################################################################################
# ######################################################################################
   
UniProt_file = open("Uniprot_ID_Mapping_for_Drosophila_Complete_File.txt", "r")
uniProt_IDs = {}
for line in UniProt_file:
    uniProt_IDs[line.split()[0]] = {}
UniProt_file.close()
print('# of uniProt_IDs: ' + str(len(uniProt_IDs.keys())) + '\n')
   
UniProt_file = open("Uniprot_ID_Mapping_for_Drosophila_Complete_File.txt", "r")
for line in UniProt_file:
    uniProt_IDs[line.split()[0]][line.split()[1]] = line.split()[2]
UniProt_file.close()


# ######################################################################################
# ######################################################################################
# ######################################################################################

gene_names_to_uniProt_IDs_and_FlyBase_IDs = [[], [], []]

all_gene_names_in_UniProt = []

counter = 0
for uniProt_ID, value in uniProt_IDs.items():
   gene_name = ''
   FlyBase_ID = ''
   for x, y in value.items():
      if (x == 'Gene_Name'):
         gene_name = y
      if (x == 'FlyBase'):
         FlyBase_ID = y
   if (gene_name != '' and FlyBase_ID != '' and gene_name in gene_names):
      gene_names_to_uniProt_IDs_and_FlyBase_IDs[0].append(uniProt_ID)
      gene_names_to_uniProt_IDs_and_FlyBase_IDs[1].append(gene_name)
      gene_names_to_uniProt_IDs_and_FlyBase_IDs[2].append(FlyBase_ID)
      all_gene_names_in_UniProt.append(gene_name)
   if (gene_name != '' and FlyBase_ID == ''):
      counter += 1

print('# of unique gene names in UniProt: ' + str(len(list(set(all_gene_names_in_UniProt)))) + '\n')
print('counter: ', counter)

_file = open("gene_names_UniProt_IDs_FlyBase_IDs.txt", "w")
n = len(gene_names_to_uniProt_IDs_and_FlyBase_IDs[0])
gene_name_to_FlyBase_IDs_hash = {}
gene_name_to_UniProt_IDs_hash = {}
for i in range(0, n):
   _file.write(gene_names_to_uniProt_IDs_and_FlyBase_IDs[0][i] + '\t' + gene_names_to_uniProt_IDs_and_FlyBase_IDs[1][i] + '\t' + gene_names_to_uniProt_IDs_and_FlyBase_IDs[2][i] + '\n')
   gene_name_to_FlyBase_IDs_hash[gene_names_to_uniProt_IDs_and_FlyBase_IDs[1][i]] = []
   gene_name_to_UniProt_IDs_hash[gene_names_to_uniProt_IDs_and_FlyBase_IDs[1][i]] = []

for i in range(0, n):
   gene_name_to_FlyBase_IDs_hash[gene_names_to_uniProt_IDs_and_FlyBase_IDs[1][i]].append(gene_names_to_uniProt_IDs_and_FlyBase_IDs[2][i])
   gene_name_to_UniProt_IDs_hash[gene_names_to_uniProt_IDs_and_FlyBase_IDs[1][i]].append(gene_names_to_uniProt_IDs_and_FlyBase_IDs[0][i])

_file = open("gene_names_to_FlyBase_IDs.txt", "w")
_file_2 = open("gene_names_to_FlyBase_IDs_non_unique.txt", "w")
for x in gene_name_to_FlyBase_IDs_hash:
   if (len(list(set(gene_name_to_FlyBase_IDs_hash[x]))) == 1):
      _file.write(x + '\t' + gene_name_to_FlyBase_IDs_hash[x][0] + '\n')
   else:
      _file_2.write(x + '\t')
      _temp_list = list(set(gene_name_to_FlyBase_IDs_hash[x]))
      for y in _temp_list:
         _file_2.write(y + '\t')
      _file_2.write('\n')

_file = open("gene_names_to_UniProt_IDs.txt", "w")
for x, y in gene_name_to_UniProt_IDs_hash.items():
   _file.write(x + '\t')
   for z in y:
      _file.write(z + '\t')
   _file.write('\n')



# this file is downloaded directly from flybase.org as FlyBase IDs of 
# essential genes reported by DEG
_file = open("FlyBase_IDs_Extracted_Using_flybase.org_website.txt", "r")
gene_ids_1 = []
for line in _file:
   gene_ids_1.append(line.split()[0])


# this file contains FlyBase IDs of essential genes which we extracted
# by processing DEG gene_names and UniProt ID mapping
_file = open("gene_names_to_FlyBase_IDs.txt", "r")
gene_ids_2 = []
for line in _file:
   gene_ids_2.append(line.split()[1])

Deg_Essential_FlyBase_IDs_intersection_between_flybase_org_N_handy_exracted = list(set(gene_ids_1) & set(gene_ids_2))
# it seems the progress is in true direction! see the result.
print(len(Deg_Essential_FlyBase_IDs_intersection_between_flybase_org_N_handy_exracted))
_file = open("gene_names_to_FlyBase_IDs_intersection_between_flybase.org_N_handy_exracted.txt", "w")
for x in Deg_Essential_FlyBase_IDs_intersection_between_flybase_org_N_handy_exracted:
   _file.write(x + '\n')

