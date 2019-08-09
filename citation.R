setwd(paste0(Sys.getenv('CS_HOME'),'/Perspectivism/Models/QuantEpistemo'))

library(dplyr)
library(igraph)
library(glue)
library(reshape2)
library(ggplot2)

source(paste0(Sys.getenv('CS_HOME'),'/Organisation/Models/Utils/R/plots.R'))
source('functions.R')

citation <- read_graph('processed/core_hdepth3_filtered.gml',format='gml')

###
# communities

set.seed(0)

A=as_adjacency_matrix(citation,sparse = T)
com = communities_louvain(citation)
directedmodularity(com$membership,A)

d=degree(citation,mode='in')
for(c in unique(com$membership)){
  show(paste0("Community ",c, " ; corpus prop ",100*length(which(com$membership==c))/vcount(citation)))
  currentd=d[com$membership==c];dth=sort(currentd,decreasing = T)[10]
  show(data.frame(titles=V(citation)$title[com$membership==c&d>dth],degree=d[com$membership==c&d>dth]))
}

