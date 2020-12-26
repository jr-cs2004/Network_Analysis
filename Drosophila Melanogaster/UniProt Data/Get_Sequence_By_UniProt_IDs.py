import urllib.parse
import urllib.request

url = 'https://www.uniprot.org/uploadlists/'
# ######################################################################################
# ######################################################################################
# ######################################################################################


uniprot_IDs_File = open("All_UniProt_IDs.list", "r")
uniprot_IDs = []
for line in uniprot_IDs_File:
   uniprot_IDs.append(line.split()[0])

# removing any repetitions
uniprot_IDs = list(set(uniprot_IDs))

uniprot_IDs_and_their_corresponding_sequences_file = open('uniprot_IDs_and_their_corresponding_sequences.txt', 'w')
number_of_uniprot_ids = len(uniprot_IDs)
print('number_of_uniprot_ids: ', number_of_uniprot_ids)
# Uniprot has some limitation on the size of the query list
segmentation_size = 2000
m = int(number_of_uniprot_ids / segmentation_size)
for i in range(0, m + 1):
    print (round(i / m * 100, 1), '%', end="\r")
    if ((i + 1) * segmentation_size <= number_of_uniprot_ids):
        last_index = (i + 1) * segmentation_size
    else: 
        last_index = number_of_uniprot_ids
    queries = uniprot_IDs[i * segmentation_size : last_index]
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

    for protein_uniprot_id, sequence in protein_sequence_mapper.items():
        uniprot_IDs_and_their_corresponding_sequences_file.write(protein_uniprot_id + '\n' + sequence + '\n')


# ######################################################################################
# ######################################################################################
# ######################################################################################
