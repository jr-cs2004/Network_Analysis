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
   
UniProt_file = open("DROME_7227_idmapping.dat", "r")

uniProt_ids = []
other_id_types = []
other_id_values = []
for line in UniProt_file:
    uniProt_ids.append(line.split()[0])
    other_id_types.append(line.split()[1])
    other_id_values.append(line.split()[2])

print('# of uniProt_ids: ' + str(len(uniProt_ids)) + '\n')



# ######################################################################################
# ######################################################################################
# ######################################################################################


n = len(uniProt_ids)
_uniProt_ids = []
_other_id_types = []
_other_id_values = []
for i in range(0, n):
    if (other_id_types[i] == 'Gene_Name'):
        _uniProt_ids.append(uniProt_ids[i])
        _other_id_types.append(other_id_types[i])
        _other_id_values.append(other_id_values[i])
print('# of _uniProt_ids: ' + str(len(_uniProt_ids)) + '\n')
gene_names_to_UniProt_IDs = [[], []]
m = len(gene_names)
n = len(_uniProt_ids)
for i in range(0, m):
    counter = 0
    for j in range(0 , n):
        if (_other_id_values[j] == gene_names[i]):
            counter += 1
            gene_names_to_UniProt_IDs[0].append(gene_names[i])
            gene_names_to_UniProt_IDs[1].append(_uniProt_ids[j])

test_file = open("test.txt", "w")
n = len(gene_names_to_UniProt_IDs[0])
for i in range(0, n):
    test_file.write(gene_names_to_UniProt_IDs[0][i] + '\t' + gene_names_to_UniProt_IDs[1][i] + '\n')


print('# of unique finds: ' + str(len(list(set(gene_names_to_UniProt_IDs[0])))) + '\n')