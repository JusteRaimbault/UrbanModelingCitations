setwd(paste0(Sys.getenv('CS_HOME'),'/Perspectivism/Models/QuantEpistemo'))

library(dplyr)
library(igraph)
library(glue)
library(reshape2)
library(ggplot2)

source(paste0(Sys.getenv('CS_HOME'),'/Organisation/Models/Utils/R/plots.R'))
source('functions.R')

citation <- read_graph('processed/core_hdepth3_filtered.gml',format='gml')

resdir <- 'results/analysis/'

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


citcomnames = list('5'='Hydrology','32'='Junk1','29'='Junk2','14'='Planning/urban form','30'='Labour market',
                   '13'='Retirement','12'='Traffic','33'='Landscape genetics','15'='Transportation statistics',
                   '26'='Spatial epidemiology','28'='Transportation physics','9'='Critical infrastructures',
                   '3'='Ethics','18'='Transportation economics','8'='Transport optimization','23'='Spatial statistics',
                   '7'='Mobility simulation','4'='Logistics simulation','25'='Population microsimulation',
                   '19'='Social networks','17'='Transportation microsimulation','36'='Complexity',
                   '11'='Built environment','21'='Traffic noise','2'='Pedestrian microsimulation',
                   '35'='Urban growth modeling','34'='Accessibility','24'='Spatial interactions',
                   '31'='Urban modeling/Luti','1'='Evacuation modeling','6'='Demographics',
                   '27'='Route choice','10'='Energy','22'='Congestion','20'='Urban metabolism',
                   '16'='Geosimulation'
                   )


# community sizes
comsizes=list()
for(k in names(citcomnames)){comsizes[k]=length(which(com$membership==as.numeric(k)))}
comsizes=unlist(comsizes)

plot(log(1:length(comsizes)),log(sort(comsizes,decreasing = T)))
cumsum(sort(comsizes/sum(comsizes)))
summary(lm(data=data.frame(y=log(sort(comsizes[100*comsizes/vcount(citation)>1],decreasing = T)),x=log(1:length(comsizes[100*comsizes/vcount(citation)>1]))),y~x))
summary(lm(data=data.frame(y=log(sort(comsizes[100*comsizes/vcount(citation)<1],decreasing = T)),x=log(1:length(comsizes[100*comsizes/vcount(citation)<1]))),y~x))


## communities with a size larger than 1%
d=degree(citation,mode='in')
for(k in names(sort(comsizes[100*comsizes/vcount(citation)>2],decreasing = T))){
  show(paste0(k," ; ",citcomnames[k]," ; ",100*length(which(com$membership==k))/vcount(citation)))
  currentd=d[com$membership==k];dth=sort(currentd,decreasing = T)[3]
  show(data.frame(titles=V(citation)$title[com$membership==k&d>dth],degree=d[com$membership==k&d>dth]))
}

for(k in names(sort(comsizes[100*comsizes/vcount(citation)>1],decreasing = T))){
  show(paste0(k," ; ",citcomnames[k]," ; ",100*length(which(com$membership==k))/vcount(citation)))
}

###
# largest communities
# -> take 10 largest
largestcoms = c(35,11,31,17,36,2,16,1,34,25) 


###
# inter community citation links : proportion of out-citation links


A=as_adjacency_matrix(citation,sparse = T)
citprops = matrix(0,length(largestcoms),length(largestcoms))
for(i in 1:length(largestcoms)){
  alloutcits = sum(A[com$membership==largestcoms[i],])
  for(j in 1:length(largestcoms)){
    show(paste0(i,",",j))
    citprops[i,j] = sum(A[com$membership==largestcoms[i],com$membership==largestcoms[j]])/alloutcits
  }
}
rownames(citprops)<-unlist(citcomnames[as.character(largestcoms)]);colnames(citprops)<-unlist(citcomnames[as.character(largestcoms)])
diag(citprops)<-NA

g = ggplot(melt(citprops[,]),aes(x=Var1,y=Var2,fill=value))
g+geom_raster()+xlab("")+ylab("")+scale_fill_continuous(name="Out-citation\nProportion")+
  theme(axis.text.x = element_text(angle = 90,hjust=1))+stdtheme
ggsave(file=paste0(resdir,'com_intercit_proportion.png'),width=30,height=28,units='cm')












