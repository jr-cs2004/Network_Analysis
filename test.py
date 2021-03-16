# deg_File = open("DEG/S.Cerevisiae.Essential.Genes.txt", "r", encoding='utf8')
# _counter = 0
# deg_genes = []
# for line in deg_File:
#     deg_genes.append(line.split('\t')[1])
#     _counter += 1
# print('deg: ', _counter)

# ogee_File = open("OGEE/test.txt", "r")
# _counter = 0
# ogee_genes = []
# for line in ogee_File:
#     ogee_genes.append(line.split('\t')[3])
#     _counter += 1
# print('ogee: ', _counter)

# String_file = open("Saccharomyces cerevisiae/STRING/4932.protein.info.v11.0.txt", "r", encoding='utf8')
# proteins = []
# _counter = 0
# i = 1
# for line in String_file:
#     if (i > 1):
#         proteins.append(line.split()[1])
#         _counter += 1
#     i += 1
# proteins = list(set(proteins))
# print(len(proteins))

# lst = [value for value in proteins if value in deg_genes]

# print('DEG and String intersection: ' , len(lst))

# lst = [value for value in proteins if value in ogee_genes]
# print('OGEE and String intersection: ' , len(lst))



# ######################################################################################
# ######################################################################################
# ######################################################################################




deg_File = open("DEG/D.Melanogaster.Essential.Genes.txt", "r", encoding='utf8')
_counter = 0
deg_genes = []
for line in deg_File:
    deg_genes.append(line.split('\t')[1])
    _counter += 1
print('deg: ', _counter)

ogee_File = open("OGEE/test2.txt", "r")
_counter = 0
ogee_genes = []
for line in ogee_File:
    ogee_genes.append([line.split('\t')[3], line.split('\t')[4]])
    _counter += 1
print('ogee: ', _counter)
essential_counter = 0
non_essential_counter = 0
conditionally_essential_counter = 0
for item in ogee_genes:
    if (item[1] == 'E'):
        essential_counter += 1
    if (item[1] == 'NE'):
        non_essential_counter += 1
    if (item[1] == 'C'):
        conditionally_essential_counter += 1
print('# of essentials: ', essential_counter, '\n# of non-essentials: ', non_essential_counter,
        '\n# of conditionally essentials: ', conditionally_essential_counter)

String_file = open("Drosophila Melanogaster/STRING/7227.protein.info.v11.0.txt", "r", encoding='utf8')
STRING_protein_IDs = []
STRING_gene_names = []
_counter = 0
i = 1
for line in String_file:
    if (i > 1):
        STRING_protein_IDs.append(line.split()[0])
        STRING_gene_names.append(line.split()[1])
        _counter += 1
    i += 1
print('PPIs in STRING - # of unique IDs: ', len(list(set(STRING_protein_IDs))))

lst = [value for value in STRING_gene_names if value in deg_genes]

print('DEG and String intersection: ' , len(lst))

lst = [value for value in ogee_genes if value[0] in deg_genes]

print('OGEE and DEG intersection: ' , len(lst))

lst = [value for value in ogee_genes if value[0] if value in STRING_gene_names]
print('OGEE and String intersection: ' , len(lst))

essential_counter = 0
non_essential_counter = 0
conditionally_essential_counter = 0
contradiction_counter = 0
for item in lst:
    if (item[1] == 'E'):
        essential_counter += 1
    if (item[1] == 'NE'):
        non_essential_counter += 1        
        if (item[0] in deg_genes):
            contradiction_counter += 1
    if (item[1] == 'C'):
        conditionally_essential_counter += 1

print('# of essentials: ', essential_counter, '\n# of non-essentials: ', non_essential_counter,
        '\n# of conditionally essentials: ', conditionally_essential_counter)
print('# of contradiction between OGEE and DEG: ', contradiction_counter)





# ######################################################################################
# ######################################################################################
# ######################################################################################

import sys
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


original_PPIs_file = open("Drosophila Melanogaster/HitPredict/original_PPIs.txt", "r")

source_protein_IDs = []
target_protein_IDs = []
for line in original_PPIs_file:
   source_protein_IDs.append(line.split()[0])
   target_protein_IDs.append(line.split()[1])

_str = ('the interaction file was read:' + '\n'
+ '# of lines in the PPI files read for source interacting proteins: ' + str(len(source_protein_IDs)) + '\n'
+ '# of lines in the PPI files read for target interacting proteins: ' + str(len(target_protein_IDs)) + '\n'
+ '# of unique proteins in the source lines: ' + str(len(list(set(source_protein_IDs)))) + '\n'
+ '# of unique proteins in the target lines: ' + str(len(list(set(target_protein_IDs)))) + '\n')
print(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################


unique_proteins = []
unique_proteins.extend(source_protein_IDs)
unique_proteins.extend(target_protein_IDs)
unique_proteins = list(set(unique_proteins))
_str = '# of unique_proteins: ' + str(len(unique_proteins)) + '\n'
print(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################


print('converting local DB IDs (UniProt IDs) to FlyBase IDs...\n')

query = ' '.join(unique_proteins)
localDB_IDs_to_FlyBase_IDs = convertIDs(query, 'ID', 'STRING_ID')

_str = ('local DB IDs IDs are mapped to FlyBase IDs:' + '\n'
+ '# of IDs returned by uniprot Mapper: ' + '\n'
+ 'from: ' + str(len(localDB_IDs_to_FlyBase_IDs[0]))  + ', and to: ' +  str(len(localDB_IDs_to_FlyBase_IDs[1]))
+ ', and uniques --> from: ' + str(len(list(set(localDB_IDs_to_FlyBase_IDs[0])))) +', and to: ' +  str(len(list(set(localDB_IDs_to_FlyBase_IDs[1])))) + '\n')
print(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################


_str = ('# of all_proteins_having_at_least_an_ID_in_FlyBase: '
+ str(len(list(set(localDB_IDs_to_FlyBase_IDs[0])))) + '\n'
+ '# of all_FlyBase_IDs_obtained_by_mapping_uniprot_to_FlyBase: '
+ str(len(list(set(localDB_IDs_to_FlyBase_IDs[1])))) + '\n')
print(_str)



lst = [value for value in STRING_protein_IDs if value if value in localDB_IDs_to_FlyBase_IDs[1]]
print('hitpredict and String intersection: ' , len(lst))

_counter_1 = 0
_counter_2 = 0


# ######################################################################################
# ######################################################################################
# ######################################################################################
