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


uniprot_IDs_File = open("All_UniProt_IDs.list", "r")
uniprot_IDs = []
for line in uniprot_IDs_File:
   uniprot_IDs.append(line.split()[0])

# removing any repetitions
uniprot_IDs = list(set(uniprot_IDs))

uniprot_IDs_and_their_corresponding_FlyBase_IDs_file = open('uniprot_IDs_and_their_corresponding_FlyBase_IDs.txt', 'w')
number_of_uniprot_ids = len(uniprot_IDs)
print('number_of_uniprot_ids: ', number_of_uniprot_ids)

Uniprot_FlyBase_mapper = {}
for x in uniprot_IDs:
    Uniprot_FlyBase_mapper[x] = []
# Uniprot has some limitation on the size of the query list
_counter = {}
for i in range(0, 100): 
    _counter[i] = 0
segmentation_size = 2000
m = int(number_of_uniprot_ids / segmentation_size)
for i in range(0, m + 1):
    print (round(i / m * 100, 1), '%', end="\r")
    if ((i + 1) * segmentation_size <= number_of_uniprot_ids):
        last_index = (i + 1) * segmentation_size
    else: 
        last_index = number_of_uniprot_ids
    query_list = uniprot_IDs[i * segmentation_size : last_index]
    query = ' '.join(query_list)
    Uniprot_to_FlyBase = convertIDs(query, 'ACC+ID', 'FLYBASE_ID')
    
    local_Uniprot_FlyBase_mapper = {}
    n = len(Uniprot_to_FlyBase[0])
    for x in query_list:
        local_Uniprot_FlyBase_mapper[x] = []
    for i in range(0, n):
        local_Uniprot_FlyBase_mapper[Uniprot_to_FlyBase[0][i]].append(Uniprot_to_FlyBase[1][i])
        Uniprot_FlyBase_mapper[Uniprot_to_FlyBase[0][i]].append(Uniprot_to_FlyBase[1][i])
    for Uniprot_ID, FlyBase_IDs in local_Uniprot_FlyBase_mapper.items():
        uniprot_IDs_and_their_corresponding_FlyBase_IDs_file.write(Uniprot_ID + '\t')
        _counter[len(FlyBase_IDs)] += 1
        for x in FlyBase_IDs:
            uniprot_IDs_and_their_corresponding_FlyBase_IDs_file.write(x + '\t')
        uniprot_IDs_and_their_corresponding_FlyBase_IDs_file.write('\n')

for i in range(0, 100):
    if (_counter[i] > 0):
        print(i, '  ', _counter[i])

print('#########')
print(len(Uniprot_FlyBase_mapper.keys()))
print('#########')
FlyBase_UniProt_mapper = {}
for x in Uniprot_FlyBase_mapper.values():
    for y in x:
        FlyBase_UniProt_mapper[y] = []

for key, values in Uniprot_FlyBase_mapper.items():
    for v in values:
        FlyBase_UniProt_mapper[v].append(key)
print('#########')
print(len(FlyBase_UniProt_mapper.keys()))
print('#########')

_counter = {}
for i in range(0, 500): 
    _counter[i] = 0
for x in FlyBase_UniProt_mapper.values():
    _counter[len(x)] += 1
for i in range(0, 100):
    if (_counter[i] > 0):
        print(i, '  ', _counter[i])
# ######################################################################################
# ######################################################################################
# ######################################################################################
