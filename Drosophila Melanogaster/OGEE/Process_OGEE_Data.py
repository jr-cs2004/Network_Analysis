OGEE_File = open("7227_without_header_line.txt", "r")
open('7227_processed.txt', 'w').close()
processed_OGEE_File = open("7227_processed.txt", "a")
genes = []
essentiality = []
for line in OGEE_File:
    genes.append(line.split()[3])
    essentiality.append(line.split()[4])

print('# of genes: ', len(genes))
print('# of unique genes: ', len(list(set(genes))))


# ######################################################################################
# ######################################################################################
# ######################################################################################

# to check if some genes are repeated or no,
# if so, to check how many times each gene is repeated.

# temp_counter = 0
# counter_1 = 0
# counter_2 = 0
# counter_3 = 0
# counter_4 = 0
# counter_5 = 0
# for gene in genes:
#     temp_counter = 0
#     for _gene in genes:
#         if (gene == _gene):
#             temp_counter += 1
#     if (temp_counter == 1):
#         counter_1 += 1
#     if (temp_counter == 2):
#         counter_2 += 1
#     if (temp_counter == 3):
#         counter_3 += 1
#     if (temp_counter == 4):
#         counter_4 += 1
# print(counter_1, '   ',counter_2, '   ',counter_3, '   ',counter_4)


# ######################################################################################
# ######################################################################################
# ######################################################################################

# In the previous step we found that if any gene is repeated, it is repeated exactly two
# times. here we check that for each gene, both case reports the same results (both E or both NE) or 
# different result is reported by each experiment (one E and the other NE).

n = len(genes)
counter_redundant = 0
counter_conflict = 0
removing_indices = []
for i in range(0, n):
    counter = 0
    for j in range(0, n):
        if (i < j and genes[i] == genes[j] and essentiality[i] != essentiality[j]):
            counter_conflict += 1
            removing_indices.append(i)
            removing_indices.append(j)
        if (i < j and genes[i] == genes[j] and essentiality[i] == essentiality[j]):
            counter_redundant += 1
            removing_indices.append(j)
print('# of genes with repeats where different essentiality reported for each repeat: ', counter_conflict)
print('# of genes with repeats where the same essentiality reported for both case: ', counter_redundant)


# ######################################################################################
# ######################################################################################
# ######################################################################################

# removing genes with different results in the two experiments.
# removing the redundant data of genes having the same results in the two experiments.

for indx in sorted(removing_indices, reverse = True):  
    del genes[indx] 
    del essentiality[indx] 


# ######################################################################################
# ######################################################################################
# ######################################################################################

# counting hom many essential and non-essentiel genes are existed in the data.

n = len(genes)
counter_essential = 0
counter_non_essential = 0
counter = 0
for i in range(0, n):
    processed_OGEE_File.write(genes[i] + '\t' + essentiality[i] + '\n')
    if (essentiality[i] == 'E'):
        counter_essential += 1
    elif (essentiality[i] == 'NE'):
        counter_non_essential += 1
    else:
        counter += 1
print('# of essential genes: ', counter_essential)
print('# of non-essential genes: ', counter_non_essential)
print('# of non-determined: ', counter)