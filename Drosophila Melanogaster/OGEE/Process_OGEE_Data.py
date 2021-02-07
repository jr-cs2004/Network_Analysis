OGEE_File = open("7227_without_header_line.txt", "r")
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
# times. here we check that for each gene if both cases report the same results (both E or both NE)


n = len(genes)
counter_redundant = 0
removing_redundant_indices = []
double_essential_gene_list = []
double_NoN_essential_gene_list = []
for i in range(0, n):
    flag = False
    for j in range(0, n):
        if (i < j and genes[i] == genes[j] and essentiality[i] == essentiality[j]):
            counter_redundant += 1
            removing_redundant_indices.append(j)
            flag = True
    if (flag):
        removing_redundant_indices.append(i)
        if (essentiality[i] == "E"):
            double_essential_gene_list.append(genes[i])
        if (essentiality[i] == "NE"):
            double_NoN_essential_gene_list.append(genes[i])
print('# of genes with repeats where the same essentiality reported for both case: ', counter_redundant)


# ######################################################################################
# ######################################################################################
# ######################################################################################

# removing the redundant data of genes having the same results in the two experiments.

for indx in sorted(removing_redundant_indices, reverse = True):  
    del genes[indx] 
    del essentiality[indx]  


# ######################################################################################
# ######################################################################################
# ######################################################################################

# In the previous step we found that if any gene is repeated, it is repeated exactly two
# times. here we check that for each gene if different result is reported by each 
# experiment (one E and the other NE).

n = len(genes)
counter_conflict = 0
removing_conflict_indices = []
unknown_gene_list = []
for i in range(0, n):
    flag = False
    for j in range(0, n):
        if (i < j and genes[i] == genes[j] and essentiality[i] != essentiality[j]):
            counter_conflict += 1
            removing_conflict_indices.append(i) # since the repeat number for each gene is only 2, this line is OK, otherwise it must be rewritten in another way.
            removing_conflict_indices.append(j)
            flag = True
    if (flag):
        unknown_gene_list.append(genes[i])
print('# of genes with repeats where different essentiality reported for each repeat: ', counter_conflict)


# ######################################################################################
# ######################################################################################
# ######################################################################################

# removing genes with different results in the two experiments.

for indx in sorted(removing_conflict_indices, reverse = True):  
    del genes[indx] 
    del essentiality[indx]


# ######################################################################################
# ######################################################################################
# ######################################################################################

# adding redundant genes (genes with the same results in the two experiments)
# if it is reported both times as "E", we add it by "EE" state
# if it is reported both times as "NE", we add it by "NN" state

for x in double_essential_gene_list:  
    genes.append(x)
    essentiality.append('EE')

for x in double_NoN_essential_gene_list:  
    genes.append(x)
    essentiality.append('NN')


# ######################################################################################
# ######################################################################################
# ######################################################################################

# adding unknown genes (genes with different results in the two experiments)
# we add these genes by "U" state

for x in unknown_gene_list:  
    genes.append(x)
    essentiality.append('U')
    

# ######################################################################################
# ######################################################################################
# ######################################################################################

# counting hom many essential and non-essentiel genes are existed in the data and writing
# the processed data into a file.

processed_OGEE_File = open("OGEE_redundants_as_EE_conflicts_as_U.txt", "w")
n = len(genes)
counter_essential = 0
counter_non_essential = 0
counter_unknown = 0
counter_double_essential = 0
counter_double_NoN_essential = 0
for i in range(0, n):
    processed_OGEE_File.write(genes[i] + '\t' + essentiality[i] + '\n')
    if (essentiality[i] == 'E'):
        counter_essential += 1
    elif (essentiality[i] == 'EE'):
        counter_double_essential += 1
    elif (essentiality[i] == 'NE'):
        counter_non_essential += 1
    elif (essentiality[i] == 'NN'):
        counter_double_NoN_essential += 1
    else:
        counter_unknown += 1
print('# of essential genes: ', counter_essential)
print('# of essential genes (redundants): ', counter_double_essential)
print('# of non-essential genes: ', counter_non_essential)
print('# of non-essential genes (redundants): ', counter_double_NoN_essential)
print('# of non-determined: ', counter_unknown)


# ######################################################################################
# ######################################################################################
# ######################################################################################
