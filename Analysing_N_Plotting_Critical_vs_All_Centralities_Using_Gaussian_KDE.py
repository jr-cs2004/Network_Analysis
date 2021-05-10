import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

 
_lambda = 0.6
def get_essential_proteins_info(species):
    Essentiality_File = open(".\\" + species + "\\DIP\\output\\DIP_IDs_N_Essentiality.txt", "r") 
    _IDs = []
    _Essentiality = []
    essential_IDs = []
    unknown_essential_IDs = []
    for line in Essentiality_File:
        _IDs.append(line.split()[0])
        _Essentiality.append(line.split()[1])

    n = len(_IDs)
    for i in range(0, n):
        if (_Essentiality[i] == 'E'):
            essential_IDs.append(_IDs[i])
        if (_Essentiality[i] == 'U'):
            unknown_essential_IDs.append(_IDs[i])

    print(len(_IDs))
    print(len(essential_IDs))
    print(len(unknown_essential_IDs))
    print('###################')
    return [_IDs, _Essentiality, essential_IDs, unknown_essential_IDs]


# species = "Escherichia coli"
species = "Saccharomyces cerevisiae"


essential_IDs = get_essential_proteins_info(species)[2]

centrality_list = ['Degree', 'Betweenness', 'Closeness', 'Eigenvector'] # 
centraliy_labels = {'Degree': 'DC', 'Betweenness': 'BC', 'Closeness': 'CC', 'Eigenvector': 'EC'}
centraliy_colors = {'Degree': '#ff7f0e', 'Betweenness': '#2ca02c', 'Closeness': '#9467bd', 'Eigenvector': '#1f77b4'}
centrality = centrality_list[0]
file_name = ".\\" + species + "\\DIP\\output\\global_centrality_analysis\\all_proteins_" + centrality.lower() + "_centrality.txt"
all_proteins_centrality = []
all_proteins_centrality_dictionary = {}
with open (file_name, 'r') as nodes_centrality_file:
    _index = 0
    for line in nodes_centrality_file:
        if (_index >= 1): # for the header
            all_proteins_centrality.append(float(line.split()[1]))
            all_proteins_centrality_dictionary[line.split()[0]] = float(line.split()[1])
        _index += 1

print(max(all_proteins_centrality))

all_proteins_centrality = np.array(all_proteins_centrality)

# density = gaussian_kde(all_proteins_centrality)
# x_vals = np.linspace(0, max(all_proteins_centrality), 200) # Specifying the limits of our all_proteins_centrality
# density.covariance_factor = lambda : _lambda #Smoothing parameter 
# density._compute_covariance()
# plt.plot(x_vals,density(x_vals))

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

# density = gaussian_kde(all_essential_proteins_centrality)
# x_vals = np.linspace(0, max(all_essential_proteins_centrality), 200) # Specifying the limits of our all_essential_proteins_centrality
# density.covariance_factor = lambda : _lambda #Smoothing parameter 
# density._compute_covariance()
# plt.plot(x_vals,density(x_vals))
# plt.legend(["All_Proteins", "Essential_Proteins"])
# plt.xlabel(centrality)
# plt.ylabel('Frequency')
# plt.show()

# data = [all_proteins_centrality, all_essential_proteins_centrality]
# fig = plt.figure(figsize =(10, 7))
  
# # Creating axes instance
# ax = fig.add_axes([0, 0, 1, 1])
  
# # Creating plot
# bp = ax.boxplot(data)
  
# # show plot
# plt.show()




all_proteins_centrality_dictionary = {}
centralities_maximum_value = {}
for centrality in centrality_list:
    file_name = ".\\" + species + "\\DIP\\output\\global_centrality_analysis\\all_proteins_" + centrality.lower() + "_centrality.txt"
    _dictionary = {}
    _maximum_value = 0
    with open (file_name, 'r') as centrality_file:
        _index = 0
        for line in centrality_file:
            if (_index >= 1): # for the header
                _dictionary[line.split()[0]] = float(line.split()[1])
                if (float(line.split()[1]) > _maximum_value):
                    _maximum_value = float(line.split()[1])
            _index += 1
    all_proteins_centrality_dictionary[centrality] = _dictionary
    centralities_maximum_value[centrality] = _maximum_value
 

all_top_centrality_based_nodes = {}
for centrality in centrality_list:
    file_name = ".\\" + species + "\\DIP\\output\\global_centrality_analysis\\removed_nodes_based_on_" + centrality.lower() + "_centrality.budget_950.txt"
    with open (file_name, 'r') as centrality_based_nodes_file:
        _list = []
        _index = 0
        for line in centrality_based_nodes_file:
            if (_index >= 1): # for the header
                _list.append(line.split()[0])
            _index += 1
        all_top_centrality_based_nodes[centrality] = _list




for centrality in centrality_list:
    figs, axs = plt.subplots(2, 2)
    for i in range(50, 201, 50):

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
        density = gaussian_kde(all_essential_proteins_centrality)
        x_vals = np.linspace(0, max(all_essential_proteins_centrality), 200) # Specifying the limits of our all_essential_proteins_centrality
        density.covariance_factor = lambda : _lambda #Smoothing parameter        
        density._compute_covariance()
        if (i == 50):
            axs[0, 0].set_title('B = ' + str(i))
            axs[0, 0].plot(x_vals, density(x_vals), color='#111DD8', label = "All_Essential_Proteins")
        if (i == 100):
            axs[0, 1].set_title('B = ' + str(i))
            axs[0, 1].plot(x_vals, density(x_vals), color='#111DD8', label = "All_Essential_Proteins")
        if (i == 150):
            axs[1, 0].set_title('B = ' + str(i))
            axs[1, 0].plot(x_vals, density(x_vals), color='#111DD8', label = "All_Essential_Proteins")
        if (i == 200):
            axs[1, 1].set_title('B = ' + str(i))
            axs[1, 1].plot(x_vals, density(x_vals), color='#111DD8', label = "All_Essential_Proteins")

        file_name = ".\\" + species + "\\DIP\\output\\Boost\\Result\\critical.nodes.found.by.GA." + str(i) + ".txt"
        with open (file_name, 'r') as critical_nodes_file:
            critical_nodes = []
            _index = 0
            for line in critical_nodes_file:
                if (_index >= 2): # for the header
                    critical_nodes.append(line.split()[1])
                _index += 1

        critical_nodes = [value for value in critical_nodes if value in essential_IDs]
        print('critical_nodes: ', len(critical_nodes))
        critical_nodes_centrality = []
        for node in critical_nodes:
            critical_nodes_centrality.append(all_proteins_centrality_dictionary[centrality][node])


        critical_nodes_centrality = np.array(critical_nodes_centrality)

        density = gaussian_kde(critical_nodes_centrality)
        x_vals = np.linspace(0, centralities_maximum_value[centrality], 200) # Specifying the limits of our critical_nodes_centrality
        density.covariance_factor = lambda : _lambda #Smoothing parameter
        
        density._compute_covariance()
        # plt.plot(x_vals,density(x_vals), label = "Genetic_Algorithm")
        if (i == 50):
            axs[0, 0].set_title('B = ' + str(i))
            axs[0, 0].plot(x_vals, density(x_vals), color='#d62728', label = "GA")
        if (i == 100):
            axs[0, 1].set_title('B = ' + str(i))
            axs[0, 1].plot(x_vals, density(x_vals), color='#d62728', label = "GA")
        if (i == 150):
            axs[1, 0].set_title('B = ' + str(i))
            axs[1, 0].plot(x_vals, density(x_vals), color='#d62728', label = "GA")
        if (i == 200):
            axs[1, 1].set_title('B = ' + str(i))
            axs[1, 1].plot(x_vals, density(x_vals), color='#d62728', label = "GA")

        for ___centrality in centrality_list:
            top_centrality_based_nodes_centralities = []

            top_centrality_based_nodes = all_top_centrality_based_nodes[___centrality][0:i]
            top_centrality_based_nodes = [value for value in top_centrality_based_nodes if value in essential_IDs]
            print(___centrality + '_baed_nodes: ', len(top_centrality_based_nodes))
            for node in top_centrality_based_nodes:
                top_centrality_based_nodes_centralities.append(all_proteins_centrality_dictionary[centrality][node])
            top_centrality_based_nodes_centralities = np.array(top_centrality_based_nodes_centralities)
            density = gaussian_kde(top_centrality_based_nodes_centralities)
            x_vals = np.linspace(0, centralities_maximum_value[centrality], 200) # Specifying the limits of our top_centrality_based_nodes_centralities
            density.covariance_factor = lambda : _lambda #Smoothing parameter
            
            density._compute_covariance()
            # plt.plot(x_vals,density(x_vals), label = ___centrality + "_Centrality")
            if (i == 50):
                axs[0, 0].set_title('B = ' + str(i))
                axs[0, 0].plot(x_vals, density(x_vals), color = centraliy_colors[___centrality], label = centraliy_labels[___centrality])
            if (i == 100):
                axs[0, 1].set_title('B = ' + str(i))
                axs[0, 1].plot(x_vals, density(x_vals), color = centraliy_colors[___centrality], label = centraliy_labels[___centrality])
            if (i == 150):
                axs[1, 0].set_title('B = ' + str(i))
                axs[1, 0].plot(x_vals, density(x_vals), color = centraliy_colors[___centrality], label = centraliy_labels[___centrality])
            if (i == 200):
                axs[1, 1].set_title('B = ' + str(i))
                axs[1, 1].plot(x_vals, density(x_vals), color = centraliy_colors[___centrality], label = centraliy_labels[___centrality])

        # plt.xlabel(centrality)   
        # plt.title('top ' + str(i) + ' nodes and critical nodes')
        # plt.legend()
        # show plot
    if (centrality == 'Degree'):
        handles, labels = axs[0, 0].get_legend_handles_labels()
        figs.legend(handles, labels, loc='upper center', ncol=6)
    # plt.legend()
    for ax in axs.flat:
        ax.set(xlabel=centrality)            
    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()
    # plt.show()
    plt.savefig(".\\" + species + "\\DIP\\output\\images\\gaussian_kde\\" + centrality +".png")

