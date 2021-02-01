
   
# ######################################################################################
# ######################################################################################
# ######################################################################################


# First we must read the list of all interactions from a DroID dataset
# All intercations are stored in two lists each containing one end of each interaction.

print('reading interaction file...\n')

droid_File = open("finley_yth_without_headers.txt", "r")
droid_source_protein_IDs = []
droid_target_protein_IDs = []
for line in droid_File:
   droid_source_protein_IDs.append(line.split()[0])
   droid_target_protein_IDs.append(line.split()[1])

print('the interaction file was read:\n')
print(len(droid_source_protein_IDs))
print(len(droid_target_protein_IDs))
print(len(list(set(droid_source_protein_IDs))))
print(len(list(set(droid_target_protein_IDs))))


# ######################################################################################
# ######################################################################################
# ######################################################################################

# to check if some PPIs are repeated or no,
# if so, to check how many times each PPI is repeated.

temp_counter = 0
counter_1 = 0
counter_2 = 0
counter_3 = 0
counter_4 = 0
counter_5 = 0
removing_indices = []
n = len(droid_source_protein_IDs)
for i in range(0, n):
   source_i = droid_source_protein_IDs[i]
   target_i = droid_target_protein_IDs[i]
   temp_counter = 0
   for j in range(0,n):
      source_j = droid_source_protein_IDs[j]
      target_j = droid_target_protein_IDs[j]
      if (j > i):
         if ( (source_i == source_j and target_i == target_j) or (source_i == target_j and source_j == target_i)):
            removing_indices.append(j)
            temp_counter += 1
   if (temp_counter == 1):
      counter_1 += 1
   if (temp_counter == 2):
      counter_2 += 1
   if (temp_counter == 3):
      counter_3 += 1
   if (temp_counter == 4):
      counter_4 += 1
print(counter_1, '   ',counter_2, '   ',counter_3, '   ',counter_4)

print(len(removing_indices))
print(len(list(set(removing_indices))))


# ######################################################################################
# ######################################################################################
# ######################################################################################

# removing the redundant data of PPIs.

for indx in sorted(removing_indices, reverse = True):  
    del droid_source_protein_IDs[indx] 
    del droid_target_protein_IDs[indx] 

all_unique_proteins_in_droid = []
all_unique_proteins_in_droid.extend(droid_source_protein_IDs)
all_unique_proteins_in_droid.extend(droid_target_protein_IDs)
print('# of unique genes in DroID:     ' + str(len(list(set(all_unique_proteins_in_droid)))))
print('# of interactions in the proccessed PPIs: ', len(droid_source_protein_IDs))

# ######################################################################################
# ######################################################################################
# ######################################################################################

# we only use the PPIs of which both source and target genes are presented in the OGEE
# and DEG data
OGEE_File = open("../DEG_OGEE_combined_data.txt", "r")
list_of_valid_genes = []
for line in OGEE_File:
    list_of_valid_genes.append(line.split()[0])
print(len(list(set(list_of_valid_genes))))

removing_indices = []
n = len(droid_source_protein_IDs)
for i in range(0, n):
   source_i = droid_source_protein_IDs[i]
   target_i = droid_target_protein_IDs[i]
   if ( not((source_i in list_of_valid_genes) or (target_i in list_of_valid_genes)) ):
      removing_indices.append(i)
print(len(removing_indices))
print('# of invalid PPIs: ', len(list(set(removing_indices))))

n = len(droid_source_protein_IDs)
with open('DroID.GGIs.txt', 'w') as _file:
   for i in range(0, n):
      source_i = droid_source_protein_IDs[i]
      target_i = droid_target_protein_IDs[i]      
      _file.write(source_i + '\t' + target_i + '\n')

for indx in sorted(removing_indices, reverse = True):  
    del droid_source_protein_IDs[indx] 
    del droid_target_protein_IDs[indx] 

n = len(droid_source_protein_IDs)
with open('DroID.GGIs.Filtered.By.Essentiality.Information.txt', 'w') as _file:
   for i in range(0, n):
      source_i = droid_source_protein_IDs[i]
      target_i = droid_target_protein_IDs[i]      
      _file.write(source_i + '\t' + target_i + '\n')

all_unique_proteins_in_droid = []
all_unique_proteins_in_droid.extend(droid_source_protein_IDs)
all_unique_proteins_in_droid.extend(droid_target_protein_IDs)
print('# of unique genes in DroID:     ' + str(len(list(set(all_unique_proteins_in_droid)))))
print('# of interactions in the proccessed PPIs: ', len(droid_source_protein_IDs))

# ######################################################################################
# ######################################################################################
# ######################################################################################

