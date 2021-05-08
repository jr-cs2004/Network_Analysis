import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
 
species = "Escherichia coli"
# species = "Saccharomyces cerevisiae"

centrality_list = ['Degree', 'Betweenness', 'Closeness', 'Eigenvector'] # 
centrality = centrality_list[3]
file_name = ".\\" + species + "\\DIP\\output\\global_centrality_analysis\\all_proteins_" + centrality.lower() + "_centrality.txt"
all_proteins_centrality = []
with open (file_name, 'r') as nodes_centrality_file:
    _index = 0
    for line in nodes_centrality_file:
        if (_index >= 1): # for the header
            all_proteins_centrality.append(float(line.split()[1]))
        _index += 1

print(max(all_proteins_centrality))

all_proteins_centrality = np.array(all_proteins_centrality)

all_proteins_centrality = np.array([152, 146, 138, 131, 124, 119, 118, 112, 111, 107, 101, 101, 96, 96, 95, 89, 85, 84, 84, 84, 81, 81, 75, 75, 75, 75, 74, 72, 71, 69, 69, 69, 68, 67, 67, 65, 64, 64, 63, 63, 61, 59, 58, 58, 57, 57, 56, 53, 52, 51, 51, 51, 50, 50])

density = gaussian_kde(all_proteins_centrality)
x_vals = np.linspace(0, max(all_proteins_centrality), 200) # Specifying the limits of our all_proteins_centrality
density.covariance_factor = lambda : .5 #Smoothing parameter
 
density._compute_covariance()
plt.plot(x_vals,density(x_vals))

file_name = ".\\" + species + "\\DIP\\output\\global_centrality_analysis\\all_essential_proteins_" + centrality.lower() + "_centrality.txt"
all_essential_proteins_centrality = []
with open (file_name, 'r') as nodes_centrality_file:
    _index = 0
    for line in nodes_centrality_file:
        if (_index >= 1): # for the header
            all_essential_proteins_centrality.append(float(line.split()[1]))
        _index += 1

print(max(all_essential_proteins_centrality))

all_essential_proteins_centrality = np.array(all_essential_proteins_centrality)

all_essential_proteins_centrality = np.array([11, 16, 17, 18, 19, 22, 24, 26, 26, 30, 34, 36, 38, 39, 40, 42, 50, 50, 51, 53, 57, 68, 72, 74, 75, 95, 96, 107, 111, 112, 138, 146])

density = gaussian_kde(all_essential_proteins_centrality)
x_vals = np.linspace(0, max(all_essential_proteins_centrality), 200) # Specifying the limits of our all_essential_proteins_centrality
density.covariance_factor = lambda : .5 #Smoothing parameter
 
density._compute_covariance()
plt.plot(x_vals,density(x_vals))

plt.legend(["All_Proteins", "Essential_Proteins"])
plt.xlabel(centrality)
plt.ylabel('Frequency')
plt.show()

data = [all_proteins_centrality, all_essential_proteins_centrality]
fig = plt.figure(figsize =(10, 7))
  
# Creating axes instance
ax = fig.add_axes([0, 0, 1, 1])
  
# Creating plot
bp = ax.boxplot(data)
  
# show plot
plt.show()