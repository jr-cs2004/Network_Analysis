OGEE_File = open("OGEE/7227_processed.txt", "r")

OGEE_genes = []
OGEE_essentiality = []
for line in OGEE_File:
    OGEE_genes.append(line.split()[0])
    OGEE_essentiality.append(line.split()[1])

print('# of genes: ', len(OGEE_genes))
print('# of unique genes: ', len(list(set(OGEE_genes))))


DEG_File = open("DEG/FlyBase_IDs_Extracted_Using_flybase.org_website.txt", "r")

DEG_genes = []

for line in DEG_File:
    DEG_genes.append(line.split()[0])

print('# of genes: ', len(DEG_genes))
print('# of unique genes: ', len(list(set(DEG_genes))))

n = len(OGEE_genes)
m = len(DEG_genes)
intersection = 0
conflict = 0

for i in range (0, n):
    for  j in range(0, m):
        if (DEG_genes[j] == OGEE_genes[i] and OGEE_essentiality[i] == 'E'):
            intersection += 1
        if (DEG_genes[j] == OGEE_genes[i] and OGEE_essentiality[i] == 'NE'):
            conflict += 1

print('intersection: ' + str(intersection) + '\t' + 'conflict: ' + str(conflict))