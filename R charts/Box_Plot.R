
species = "Escherichia coli"
# species = "Saccharomyces cerevisiae"

centralities = c('degree', 'betweenness', 'closeness', 'eigenvector') #

Budgets = c(50, 100, 150, 200, 250, 300, 350, 400) # "Escherichia coli"
# Budgets = c(50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950) # "Saccharomyces cerevisiae"


for (centrality in centralities) {
  for (B in Budgets) {
    file_name = paste("../", species, "/DIP/output/Boost/Result/intersection_statistics/", centrality, "/budget_", B, ".csv", sep="")
    file_name
    file = read.csv(file_name,header = T)
    attach(file)
    head(file)
    library(ggplot2)
    ggplot(file, aes(x=factor(P), y=x,fill=factor(P))) + geom_boxplot() + 
      theme(axis.title.x=element_blank(),
            axis.text.x=element_blank(),
            axis.ticks.x=element_blank()) + 
      ylab(paste(centrality, "of essential proteins"))
    output_file_name = paste("charts/", species, "/", centrality, "/budget_", B, ".png", sep="")
    output_file_name
    ggsave(output_file_name) 
  }
}