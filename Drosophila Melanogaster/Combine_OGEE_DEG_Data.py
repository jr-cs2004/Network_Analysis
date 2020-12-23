# ######################################################################################
# ######################################################################################
# ######################################################################################


OGEE_File = open("OGEE/7227_processed.txt", "r")

OGEE_genes = []
OGEE_essentiality = []
essential_counter = 0
non_essential_counter = 0
for line in OGEE_File:
    OGEE_genes.append(line.split()[0])
    OGEE_essentiality.append(line.split()[1])
    if (line.split()[1] == 'E'):
        essential_counter += 1
    elif (line.split()[1] == 'NE'):
        non_essential_counter += 1

print('###################\n###################')
print('OGEE Data:')
print('\t# of unique genes: ', len(list(set(OGEE_genes))))
print('\t# of essential genes: ', essential_counter)
print('\t# of non-essential genes: ', non_essential_counter)


# ######################################################################################
# ######################################################################################
# ######################################################################################


DEG_File = open("DEG/FlyBase_IDs_Extracted_Using_flybase.org_website.txt", "r")

DEG_genes = []

for line in DEG_File:
    DEG_genes.append(line.split()[0])
print('###################\n###################')
print('DEG Data:')
print('\t# of unique genes: ', len(list(set(DEG_genes))))


# ######################################################################################
# ######################################################################################
# ######################################################################################


n = len(OGEE_genes)
m = len(DEG_genes)
intersection = 0
conflict = 0
DEG_removing_indices = []
OGEE_removing_indices = []

for i in range (0, n):
    flag = False
    for  j in range(0, m):
        if (DEG_genes[j] == OGEE_genes[i] and OGEE_essentiality[i] == 'E'):
            intersection += 1
            flag = True # to remove the i index from OGEE (Due to redundancy)
        if (DEG_genes[j] == OGEE_genes[i] and OGEE_essentiality[i] == 'NE'):
            conflict += 1
            DEG_removing_indices.append(j)
            flag = True
    if (flag):
        OGEE_removing_indices.append(i)

print(len(DEG_removing_indices))
print(len(OGEE_removing_indices))


# ######################################################################################
# ######################################################################################
# ######################################################################################

# removing genes with different results in the two experiments.
# removing the redundant data of genes having the same results in the two experiments.

for indx in sorted(OGEE_removing_indices, reverse = True):  
    del OGEE_genes[indx]
    del OGEE_essentiality[indx]

for indx in sorted(DEG_removing_indices, reverse = True):  
    del DEG_genes[indx]


# ######################################################################################
# ######################################################################################
# ######################################################################################


DEG_OGEE_combined_data_File = open("DEG_OGEE_combined_data.txt", "w")
n = len(OGEE_genes)
essential_counter = 0
non_essential_counter = 0
for i in range (0, n):
    DEG_OGEE_combined_data_File.write(OGEE_genes[i] + '\t' + OGEE_essentiality[i] + '\n')
    if (OGEE_essentiality[i] == 'E'):
        essential_counter += 1
    else:
        non_essential_counter += 1

m = len(DEG_genes)
for i in range(0, m):
    DEG_OGEE_combined_data_File.write(DEG_genes[i] + '\t' + 'E' + '\n')
    essential_counter += 1


# ######################################################################################
# ######################################################################################
# ######################################################################################

DEG_new_genes_counter = 0
for  j in range(0, m):
    if (DEG_genes[j] not in OGEE_genes):
        DEG_new_genes_counter += 1

print('###################\n###################')
print('Combination Data:')
print('essential genes in DEG while not in the OGEE gene list: ' + str(DEG_new_genes_counter))
print('intersection between essential genes of OGEE and DEG: ' + str(intersection))
print('conflict between essential genes of DEG and non-essential genes of OGEE: ' + str(conflict))
print('# of all final genes: ', str(essential_counter + non_essential_counter))
print('# of essential genes: ', str(essential_counter))
print('# of non-essential genes: ', str(non_essential_counter))

print('###################\n###################')



# OGEE_conflict_File = open("OGEE/genes_with_conflict.txt", "r")

# OGEE_conflict_genes = []

# for line in OGEE_conflict_File:
#     OGEE_conflict_genes.append(line.split()[0])
# print('###################\n###################')
# print('OGEE Conflict Data:')
# print('\t# of unique genes: ', len(list(set(OGEE_conflict_genes))))

# intersection = 0
# n = len(OGEE_conflict_genes)
# for i in range (0, n):
#     for  j in range(0, m):
#         if (DEG_genes[j] == OGEE_conflict_genes[i]):
#             intersection += 1
# print('\tintersection between conflicting genes of OGEE and essential genes of DEG: ' + str(intersection))