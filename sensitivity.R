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

exportGraph <- function(citnw,exportfile){
  citation = citnw
  V(citation)$reduced_title = sapply(V(citation)$title,function(s){paste0(substr(s,1,50),"...")})
  V(citation)$reduced_title = ifelse(degree(citation)>20,V(citation)$reduced_title,rep("",vcount(citation)))
  write_graph(citation,file=exportfile,format = 'gml')
}

####
# sensitivity both for full and depth 100 nw ? not needed as full includes 100
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
indicnames = c('modularity'='Modularity','communitiesnumber'='Number of communities','avgDegree'='Average degree',
               'avgInDegree'='Average in-degree','avgOutDegree'='Average out-degree',
               'alphaDegree.rank'='Degree hierarchy','alphaInDegree.rank'='In-degree hierarchy','alphaOutDegree.rank'='Out-degree hierarchy',
               'ecount'='Links','vcount'='Nodes'
               )

for(indic in indics){
  g=ggplot(res,aes_string(x='horizontalDepth',y=indic,group='kw',color='kw'))
  g+geom_point()+geom_line()+xlab('Horizontal depth')+ylab(indicnames[indic])+scale_color_discrete(name='Subgraph')+stdtheme
  ggsave(file=paste0(resdir,'sensitivity_fullnw_subnws_',indic,'.png'),width=30,height=20,units='cm')
}

for(indic in indics){
  g=ggplot(res[res$horizontalDepth<=100,],aes_string(x='horizontalDepth',y=indic,group='kw',color='kw'))
  g+geom_point()+geom_line()+xlab('Horizontal depth')+ylab(indicnames[indic])+scale_color_discrete(name='Subgraph')+stdtheme
  ggsave(file=paste0(resdir,'sensitivity_fullnw_hdmax100_subnws_',indic,'.png'),width=30,height=20,units='cm')
}


# absolute optimum is not clear - low difference and varies accross subnetworks
# try Pareto ?

# vcount / modularity
g=ggplot(res,aes(x=vcount,y=modularity,color=kw,group=kw))
g+geom_point()+xlab('Nodes')+ylab('Modularity')+scale_color_discrete(name='Subgraph')+stdtheme
ggsave(file=paste0(resdir,'pareto_vcount-modularity_subnws.png'),width=25,height=18,units='cm')

g=ggplot(res[res$kw=='all',],aes(x=vcount,y=modularity,color=horizontalDepth))
g+geom_point()+xlab('Nodes')+ylab('Modularity')+scale_color_continuous(name='Depth')+stdtheme
ggsave(file=paste0(resdir,'pareto_vcount-modularity.png'),width=20,height=18,units='cm')
# -> two 'type of networks' seem emerge : few nodes-higher mod ; more nodes-lower mod
# test viz / com description on the two ?

# other Pareto ? seems ok

# export the two in gml for viz
res[res$kw=='all'&res$modularity==max(res$modularity[res$kw=='all']),]
# -> hd = 3
exportGraph(induced_subgraph(citnw,which(V(citnw)$horizontalDepth<=3)),'processed/core_hdepth3.gml')

res[res$kw=='all'&res$modularity>0.748&res$vcount>1.25e5,]
# -> hd = 400
exportGraph(induced_subgraph(citnw,which(V(citnw)$horizontalDepth<=400)),'processed/core_hdepth400.gml')


######
### overlap between sub-networks









