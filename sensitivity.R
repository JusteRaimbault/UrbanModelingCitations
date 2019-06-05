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


####
# sensitivity both for full and depth 100 nw ? not needed as full includes 100
# rq: do the same for subnws for each req

edges <- read.csv('processed/core_full_edges.csv',colClasses = c('character','character'))
nodes <- as.tbl(read.csv('processed/core_full_nodes.csv',stringsAsFactors = F,colClasses = rep('character',12)))
for(j in 4:ncol(nodes)){nodes[,j]<-as.numeric(unlist(nodes[,j]))}
citnw <- graph_from_data_frame(edges,vertices = nodes)

#nwProperties(citnw)

hdvals = c(1:10,seq(20,150,10),seq(200,950,50))

res = data.frame()
for(hd in hdvals
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
currentcitnw=induced_subgraph(citnw,which(V(citnw)$horizontalDepth<=3))
exportGraph(currentcitnw,'processed/core_hdepth3.gml')
# IGRAPH a89a25b DN-- 33342 78921
# also export filtered version without "far communities" (finance and taxes) for better viz
set.seed(0)
coms = communities_louvain(currentcitnw)
degs=degree(currentcitnw,mode='in')
for(com in unique(coms$membership)){currentv = coms$membership==com;currentt=V(currentcitnw)$title[currentv];
show(paste0(com,' ; N=',length(which(currentv))," ; ",currentt[which(degs[currentv]==max(degs[currentv]))]))
}
# remove : 4 Finance (N=2911) ; 22 taxes (N=1645) ; rest are anecdotic
# IGRAPH 55d06a7 DN-- 28786 66603 
export_gml(induced_subgraph(currentcitnw,which(coms$membership!=4&coms$membership!=22)),'processed/core_hdepth3_filtered.gml')
#vcount(currentfiltered)/vcount(currentcitnw)

res[res$kw=='all'&res$modularity>0.748&res$vcount>1.25e5,]
# -> hd = 400
currentcitnw=induced_subgraph(citnw,which(V(citnw)$horizontalDepth<=400))
export_gml(currentcitnw,'processed/core_hdepth400.gml')
set.seed(0)
coms = communities_louvain(currentcitnw)
degs=degree(currentcitnw,mode='in')
for(com in unique(coms$membership)){currentv = coms$membership==com;currentt=V(currentcitnw)$title[currentv];
show(paste0(com,' ; N=',length(which(currentv))," ; ",currentt[which(degs[currentv]==max(degs[currentv]))]))
}
# remove : 32 (N=3774 breast cancer) ; 3 (N=12238 taxes) ; 17 (N=3551 finance) ; 23 (N=1892 HIV) ;
# 38 (N=555 epilepsy) ; 15 (N=267) solute transport ; 1 (N=82 tubercolosis) ; 39 (N=373 dividends) ;
# 16 (N=897 heart) ; 13 (N=218 resuscitation) ; 2 ( N=134 medical savings) ; 9 (N=27 rainfall) ;
# 24 (N=98 CO2) ; 37 (N=198 chemistry) ; 33 (N=17 dentistry) ; 21 N=8 aoelian transport 
# rq : could also remove automatically "too far communities ?"
#  decide if work on filtered ? YES
filtered=c(32,3,17,23,38,15,1,39,16,13,2,9,24,37,33,21)
currentfiltered = induced_subgraph(currentcitnw,which(!coms$membership%in%filtered))
vcount(currentfiltered)/vcount(currentcitnw) # 0.8116309 -> only 19% of unrelated !
export_gml(currentfiltered,'processed/core_hdepth400_filtered.gml')
export_csv(currentfiltered,'processed/core_hdepth400_filtered_edges.csv','processed/core_hdepth400_filtered_nodes.csv',V(currentfiltered)$horizontalDepth)


######
### overlap between sub-networks ?

# - % of full nw covered for each kw as function of hdepth
# - 2-by-2 overlaps ? (heatmap ~ proximity matrix) ! =f(depth) -> do for the two exported networks

N = vcount(citnw)

g=ggplot(res[res$kw!='all',],aes(x=horizontalDepth,y=vcount/N,group=kw,color=kw))
g+geom_point()+geom_line()+xlab('Horizontal depth')+ylab('Full network coverage')+scale_color_discrete(name='Subgraph')+stdtheme
ggsave(file=paste0(resdir,'coverage_subnws.png'),width=30,height=20,units='cm')
# -> luti has a high coverage, comparable to 'spatial microsim model'


# overlap heatmaps at d = 3,10,100,400
currenthdepths=c(3,10,100,400)

#overlaps=data.frame()

ckws1=c();ckws2=c();chds=c();crelovs=c();cabsovs=c()
for(hd in currenthdepths){
  currentcitnw = induced_subgraph(citnw,which(V(citnw)$horizontalDepth<=hd))
  for(kw1 in kws){
    show(kw1)
    for(kw2 in kws){
      show(kw2)
      # overlap in % of the full nw ? (normalized)
      ids1=V(currentcitnw)$name[!is.na(get.vertex.attribute(currentcitnw,kw1))]
      ids2=V(currentcitnw)$name[!is.na(get.vertex.attribute(currentcitnw,kw2))]
      relov = 2*length(intersect(ids1,ids2))/(length(ids1)+length(ids2))
      absov = length(intersect(ids1,ids2))/N
      crelovs=append(crelovs,relov);cabsovs=append(cabsovs,absov);chds=append(chds,hd);ckws1=append(ckws1,kw1);ckws2=append(ckws2,kw2)
    }
  }
}

overlaps=data.frame(kw1=ckws1,kw2=ckws2,horizontalDepth=chds,relov=crelovs,absov=cabsovs)

g=ggplot(overlaps,aes(x=kw1,y=kw2,fill=relov))
g+geom_raster()+facet_wrap(~horizontalDepth)+xlab('')+ylab('')+stdtheme+
  scale_fill_continuous(name='Relative overlap')+theme(axis.text.x = element_text(angle = 90,hjust=1))
ggsave(file=paste0(resdir,'overlaps_relative.png'),width=35,height=30,units='cm')

g=ggplot(overlaps,aes(x=kw1,y=kw2,fill=absov))
g+geom_raster()+facet_wrap(~horizontalDepth)+xlab('')+ylab('')+stdtheme+
  scale_fill_continuous(name='Absolute overlap')+theme(axis.text.x = element_text(angle = 90,hjust=1))
ggsave(file=paste0(resdir,'overlaps_absolute.png'),width=35,height=30,units='cm')




