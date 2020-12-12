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


# First we must read the list of all interactions from a BioGrid dataset
# All intercations are stored in two lists each containing one end of each interaction.

print('reading interaction file...\n')

# bioGrid_File = open("I:\\myUniversity\\Drosophila melanogaster\\BIOGRID\\BIOGRID_ORGANISM_Drosophila_melanogaster_4.0.189.mitab__Without_Header_Line.txt", "r")
bioGrid_File = open("BIOGRID_ORGANISM_Drosophila_melanogaster_4.0.189.mitab__Without_Header_Line.txt", "r")
biogrid_source_protein_IDs = []
biogrid_target_protein_IDs = []
for line in bioGrid_File:
   biogrid_source_protein_IDs.append(line.split()[1].split(':')[1])
   biogrid_target_protein_IDs.append(line.split()[3].split(':')[1])

_str = ('the interaction file was read:' + '\n'
+ '# of lines in the PPI files read for source interacting proteins: ' + str(len(biogrid_source_protein_IDs)) + '\n'
+ '# of lines in the PPI files read for target interacting proteins: ' + str(len(biogrid_target_protein_IDs)) + '\n'
+ '# of unique proteins in the source lines: ' + str(len(list(set(biogrid_source_protein_IDs)))) + '\n'
+ '# of unique proteins in the target lines: ' + str(len(list(set(biogrid_target_protein_IDs)))) + '\n')
print(_str)


# ######################################################################################
# ######################################################################################
# ######################################################################################


all_unique_proteins_in_biogrid = []
all_unique_proteins_in_biogrid.extend(biogrid_source_protein_IDs)
all_unique_proteins_in_biogrid.extend(biogrid_target_protein_IDs)

_str = '# of all_unique_proteins_in_biogrid: ' + str(len(list(set(all_unique_proteins_in_biogrid)))) + '\n'
print(_str)

# ######################################################################################
# ######################################################################################
# ######################################################################################


# Now we want to map each BioGrid ID (which is an Entrez Gene ID) to a standard UniProt ID
# 'P_ENTREZGENEID' is used to indicate that the corresponding ID is an Entrez Gene ID (GeneID)
# 'ID' is used to indicate that the corresponding ID is a UniProt ID.
# The output of "convertIDs" function is a 2D array where the first column contains "P_ENTREZGENEID"s
# as source IDs and the second column contains their corresponding "ID"s as target IDs.
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

query = ' '.join(biogrid_target_protein_IDs)
biogrid_target_to_uniprot_IDs = convertIDs(query, 'P_ENTREZGENEID', 'ID')

_str = ('biogrid IDs are mapped to uniprot IDs:' + '\n'
+ '# of IDs returned by uniprot Mapper: ' + '\n'
+ 'Target: ' + '\n'
+ 'from: ' + str(len(biogrid_target_to_uniprot_IDs[0]))  + ', and to: ' +  str(len(biogrid_target_to_uniprot_IDs[1]))
+ ', and uniques --> from: ' + str(len(list(set(biogrid_target_to_uniprot_IDs[0]))))  + ', and to: ' +  str(len(list(set(biogrid_target_to_uniprot_IDs[1])))) + '\n')
print(_str)

queries = list(set(biogrid_target_to_uniprot_IDs[1]))[1:1000]
# queries.extend(list(set(biogrid_target_to_uniprot_IDs[1])))
queries = list(set(queries))

output_file = open('output.txt', 'w')

print(len(queries))

params = {
    'from':'ACC+ID',
    'to':'ACC',
    'format':'FASTA',
    'query':' '.join(queries)
}


data = urllib.parse.urlencode(params)
data = data.encode('utf-8')
req = urllib.request.Request(url, data)
with urllib.request.urlopen(req) as f:
    response = f.read()

# output_file.write(response.decode('utf-8'))

protein_sequence_mapper = {}
proteins_sequences = response.decode('utf-8')
lines_of_proteins_sequences = proteins_sequences.splitlines()
t = 0
n = len(lines_of_proteins_sequences)
print(n)
line = lines_of_proteins_sequences[t]
while t < n:    
    if line[0] == '>':
        protein_uniprot_id = line.split('|')[1]
        sequence = ''
        t += 1
        line = lines_of_proteins_sequences[t]
        while  line[0] != '>':
            sequence += line
            t += 1
            if (t < n):
                line = lines_of_proteins_sequences[t]
            else:
                break
        protein_sequence_mapper[protein_uniprot_id] = sequence
    # print(t)    

for protein_uniprot_id, sequence in protein_sequence_mapper.items():
    output_file.write(protein_uniprot_id + '\n' + sequence + '\n')

# _str = response.decode('utf-8')
# counter = 0
# for line in _str: 
#     if(line[0] == '>'):
#         counter += 1
# print(counter)