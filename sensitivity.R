setwd(paste0(Sys.getenv('CS_HOME'),'/UrbanDynamics/Models/QuantEpistemo'))

library(dplyr)
library(igraph)
library(glue)
library(ggplot2)


source('functions.R')
source(paste0(Sys.getenv('CS_HOME'),'/Organisation/Models/Utils/R/plots.R'))

resdir = 'results/sensitivity/'

load('processed/citation_kws_tmp.RData')

####
# sensitivity analysis of network properties to horizontal (and vertical ?) depth


nwProperties <- function(citnw){
  A=as_adjacency_matrix(citnw,sparse = T)
  M = A+t(A)
  undir_citnw = graph_from_adjacency_matrix(M,mode="undirected")
  coms = cluster_louvain(undir_citnw)
  return(c(
    modularity = modularity(coms),
    #directedModularity = directedmodularity(membership(coms),A), # long to compute and very close to undir
    communitiesnumber = length(unique(membership(coms))),
    avgDegree = mean(degree(citnw,mode = 'all')),
    avgInDegree = mean(degree(citnw,mode = 'in')),
    avgOutDegree = mean(degree(citnw,mode = 'in')),
    alphaDegree = hierarchy(degree(citnw,mode = 'all')),
    alphaInDegree = hierarchy(degree(citnw,mode = 'in')),
    alphaOutDegree = hierarchy(degree(citnw,mode = 'out')),
    ecount = ecount(citnw),
    vcount = vcount(citnw)
  ))
}

####
# sensitivity both for full and depth 100 nw
# rq: do the same for subnws for each req

edges <- read.csv('processed/core_full_edges.csv',colClasses = c('character','character'))
nodes <- as.tbl(read.csv('processed/core_full_nodes.csv',stringsAsFactors = F,colClasses = rep('character',12)))
for(j in 3:ncol(nodes)){nodes[,j]<-as.numeric(unlist(nodes[,j]))}
citnw <- graph_from_data_frame(edges,vertices = nodes)

#nwProperties(citnw)

res = data.frame()
for(hd in 
    c(1:10,seq(20,150,10),seq(200,950,50))
    #seq(1,100,1)
    ){
  show(hd)
  currentcitnw = induced_subgraph(citnw,which(V(citnw)$horizontalDepth<=hd))
  currentProperties=nwProperties(currentcitnw)
  res=rbind(res,c(currentProperties,horizontalDepth=hd,kw=length(kws)+1))
  for(i in 1:length(kws)){
    show(kws[i])
    currentcitnw = induced_subgraph(citnw,which(get.vertex.attribute(citnw,kws[i])<=hd))
    currentProperties=nwProperties(currentcitnw)
    res=rbind(res,c(currentProperties,horizontalDepth=hd,kw=i))
  }
}
kwstr = c(kws,'all')
names(res)<-c(names(currentProperties),"horizontalDepth","kwid")
res[['kw']]<-kwstr[res$kwid]
save(res,file='processed/sensitivity.RData')

indics = names(res)[1:(ncol(res)-3)]

for(indic in indics){
  g=ggplot(res,aes_string(x='horizontalDepth',y=indic,group='kw',color='kw'))
  g+geom_point()+geom_line()+xlab('Horizontal depth')+scale_color_discrete()+stdtheme
  #ggsave(file=paste0(resdir,'sensitivity_fullnw_hdmax100_',indic,'.png'),width=20,height=18,units='cm')
  ggsave(file=paste0(resdir,'sensitivity_fullnw_subnws_',indic,'.png'),width=30,height=20,units='cm')
}





