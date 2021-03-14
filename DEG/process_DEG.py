
   
# ######################################################################################
# ######################################################################################
# ######################################################################################


# First we must read the list of all interactions from a DroID dataset
# All intercations are stored in two lists each containing one end of each interaction.

print('reading interaction file...\n')

deg_File = open("eukaryotes/degannotation-e.dat", "r")
s_cerevisiae_File = open("S.Cerevisiae.Essential.Genes", "w")
# e_coli_File = open("E.Coli.Essential.Genes", "w")
d_melanogaster_File = open("D.Melanogaster.Essential.Genes", "w")

cerevisiae_counter = 0
melanogaster_counter = 0

for line in deg_File:
    print(line)
    if (line.split()[7] == 'Saccharomyces cerevisiae'):
        s_cerevisiae_File.write(line.split()[1] + '\t' + line.split()[2] + '\t' + line.split()[3])
        cerevisiae_counter += 1
    if (line.split()[7] == 'Drosophila melanogaster'):
        d_melanogaster_File.write(line.split()[1] + '\t' + line.split()[2] + '\t' + line.split()[3])
        melanogaster_counter += 1


print('cerevisiae_counter: ', cerevisiae_counter)
print('melanogaster_counter: ', melanogaster_counter)


# ######################################################################################
# ######################################################################################
# ######################################################################################