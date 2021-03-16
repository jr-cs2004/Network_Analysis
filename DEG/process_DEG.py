
# ######################################################################################
# ######################################################################################
# ######################################################################################

# In this part of the program, we process the downloaded raw file from DEG
# to get the list of essential genes of E. coli, S. cerevisiae, and D. melanogaster (flybase).
# It seems that columns #2, #3 and #4 of the data are related to IDs in different databases. 
# Therefore, we save those columns for each of the species above.

print('reading interaction file...\n')

deg_File = open("eukaryotes/degannotation-e.dat", "r", encoding='utf8')
s_cerevisiae_File = open("S.Cerevisiae.Essential.Genes.txt", "w")
d_melanogaster_File = open("D.Melanogaster.Essential.Genes.txt", "w")
cerevisiae_counter = 0
melanogaster_counter = 0
line_num = 0
for line in deg_File:
    line_num += 1
    if (line.split('\t')[7] == 'Saccharomyces cerevisiae'):
        s_cerevisiae_File.write(line.split()[1] + '\t' + line.split()[2] + '\t' + line.split()[3] + '\n')
        cerevisiae_counter += 1
    if (line.split('\t')[7] == 'Drosophila melanogaster'):
        d_melanogaster_File.write(line.split()[1] + '\t' + line.split()[2] + '\t' + line.split()[3] + '\n')
        melanogaster_counter += 1
print('cerevisiae_counter: ', cerevisiae_counter)
print('melanogaster_counter: ', melanogaster_counter)
deg_File.close()
s_cerevisiae_File.close()
d_melanogaster_File.close()

deg_File = open("bacteria/degannotation-p.dat", "r", encoding='utf8')
e_coli_File = open("E.Coli.MG1655.II.Essential.Genes.txt", "w")
e_coli_counter = 0
for line in deg_File:
    if (line.split('\t')[7] == 'Escherichia coli MG1655 II'):
        e_coli_File.write(line.split()[1] + '\t' + line.split()[2] + '\t' + line.split()[3] + '\n')
        e_coli_counter += 1
print('e_coli_counter: ', e_coli_counter)

# ######################################################################################
# ######################################################################################
# ######################################################################################
