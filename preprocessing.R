setwd(paste0(Sys.getenv('CS_HOME'),'/UrbanDynamics/Models/QuantEpistemo'))

library(dplyr)
library(igraph)
library(glue)

source('functions.R')

#edges <- read.csv('data/spatialmicrosim_depth2_links.csv',sep=";",header=F,colClasses = c('character','character'))
#nodes <- as.tbl(read.csv('data/spatialmicrosim_depth2.csv',sep=";",header=F,stringsAsFactors = F,colClasses = c('character','character','character')))

edges <- read.csv('exports/corpus_conso-urbmod-spatialmicrosim_all_20190516_links.csv',sep=";",header=F,colClasses = c('character','character'))
nodes <- as.tbl(read.csv('exports/corpus_conso-urbmod-spatialmicrosim_all_20190516.csv',sep=";",stringsAsFactors = F,colClasses = c('character','character','character','character','character','character','character')))

# grep("spatialmicrosim",nodes$horizontalDepth,fixed=T)

names(nodes)<-c("id","title","year","depth","priority","horizontalDepth","citingFilled")
nodes$priority = as.numeric(nodes$priority)
nodes$depth = as.numeric(nodes$depth)

# nchar(c(nodes[nodes$depth==2,"horizontalDepth"]))

elabels = unique(c(edges$V1,edges$V2))
empty=rep("",length(which(!elabels%in%nodes$id)))
nodes=rbind(nodes,data.frame(title=empty,id=elabels[!elabels%in%nodes$id],year=empty))#,abstract=empty,authors=empty))

##
# join languages
lang <- as.tbl(read.csv('language/lang_urbmod.csv',sep=';',header = T,colClasses = c('character','character','numeric','character')))
lang2 <- as.tbl(read.csv('language/lang_spatialmicrosim.csv',sep=';',header = T,colClasses = c('character','character','numeric','character')))
lang$id = trim(lang$id);lang2$id = trim(lang2$id)
lang = rbind(lang,lang2)
lang=lang[!duplicated(lang$id),]
lang$lang[lang$reliable=='False'] = NA
lang$lang[lang$confidence<50] = NA
nodes <- left_join(nodes,lang[,c('id','lang')])

citation <- graph_from_data_frame(edges,vertices = nodes) #nodes[,c(2,1,3)])#3:7)])

#components(citation)$csize

citation = induced_subgraph(citation,which(components(citation)$membership==1))


#grep("spatialmicrosim",V(citation)$horizontalDepth,fixed=T)
# ensure hdepth are consistent
#summary(nchar(V(citation)$horizontalDepth[V(citation)$depth==2]))
#newprio = sapply(V(citation)$horizontalDepth[V(citation)$depth==2],function(s){min(as.numeric(sapply(strsplit(s,",")[[1]],function(ss){strsplit(ss,":")[[1]][2]})))})
#V(citation)$priority[V(citation)$depth==2]=newprio
#summary(V(citation)$priority[V(citation)$depth==2])
#V(citation)$priority[V(citation)$depth<2]=NA
#V(citation)$horizontalDepth[V(citation)$depth<2]=NA

# propagate priority for easier sensitivity analysis ?
#for(d in 1:0){
#  prios = c()
#  for(v in V(citation)[V(citation)$depth==d]){prios[V(citation)$name[v]]=min(neighbors(citation,v,"out")$priority)}
#}

# construct attributes for each hdepth kws
splitted = sapply(unique(V(citation)$horizontalDepth[!is.na(V(citation)$horizontalDepth)]),function(s){
  sapply(strsplit(s,",")[[1]],
         function(ss){strsplit(ss,":")[[1]][1]})
})
kws = unique(unlist(splitted))

depths =sapply(V(citation)$horizontalDepth,function(s){
  if (is.na(s)){return(NA)}else{
  res = sapply(strsplit(s,",")[[1]],
         function(ss){
           spl = strsplit(ss,":")[[1]]
           res = c()
           res[[spl[1]]]=as.numeric(spl[2])
           return(res)
           })
  return(res)
  }
})

prios = sapply(depths,function(l){if(length(l)==0){return(NA)}else{return(min(unlist(l)))}})

V(citation)$priority <- prios

for(kw in kws){
  #sapply(depths,function(d){grep(paste0('.',kw),names(d),fixed=T)})
  vertex_attr(citation,kw) <- sapply(depths,function(d){
    if(length(d)==0){return(NA)}else{
    inclkw =sapply(strsplit(names(d),".",fixed = T),function(s){s[2]})#[[1]][2]
    return(ifelse(kw %in% inclkw,d[kw==inclkw],NA))
    }
  })
}


# work on core only
citationcore = induced_subgraph(citation,which(degree(citation)>1))
citationcorehigher = citationcore
while(length(which(degree(citationcorehigher)==1))>0){citationcorehigher = induced_subgraph(citationcorehigher,which(degree(citationcorehigher)>1))}

citation = citationcorehigher

#propagate the horizdepth attributes
adjacency = get.adjacency(citation,sparse=T)

for(kw in kws){
  show(kw)
  #show(length(which(!is.na(get.vertex.attribute(citation,kw))&V(citation)$depth==2)))
  #show(length(which(!is.na(get.vertex.attribute(citation,kw)))))
  stop = F
  while(!stop){
    tofill = is.na(get.vertex.attribute(citation,kw))
    a = adjacency[tofill,!tofill]
    inds = rowSums(a)>0
    a = a[inds,]
    show(nrow(a))
    if(nrow(a)==0){stop=T}else {
      #apply(a,1,function(r){min(r*get.vertex.attribute(citation,kw)[!tofill])})
      a = a%*%Diagonal(x=get.vertex.attribute(citation,kw)[!tofill])
      a[a==0]=Inf
      citation = set.vertex.attribute(citation,kw,V(citation)[which(inds)],apply(a,1,min))
      # if in the end the min is inf, means that horzdepth was zero -> shall replace Inf by zeros
    }
  }
}

# recompute numerical hdepth
# Note JR 20190529 : done with the saved citation graph - similar to execute after remote computation of clean graph 

# replace infty by 0
for(kw in kws){v=get.vertex.attribute(citation,kw);v[v==Inf]=0;citation=set.vertex.attribute(citation,kw,V(citation),v)}
# construct :
# data.frame(V(citation)$microsim,V(citation)$transportmicrosimmodel,V(citation)$microsimmodel,V(citation)$urbanmicrosimmodel,V(citation)$spatialmicrosimmodel)
hdepthdf = data.frame(get.vertex.attribute(citation,kws[1]))
for(kw in kws[2:length(kws)]){hdepthdf = cbind(hdepthdf,get.vertex.attribute(citation,kw))}
#summary(apply(hdepthdf,1,function(r){min(r,na.rm = T)}))
V(citation)$numHorizontalDepth = apply(hdepthdf,1,function(r){min(r,na.rm = T)})

save(citation,file='processed/citation_tmp.RData')
save(kws,file='processed/citation_kws_tmp.RData')

####-- Export -- ####

load('processed/citation_tmp.RData')
load('processed/citation_kws_tmp.RData')

# csv export
export_csv(citation,'processed/core_full_edges.csv','processed/core_full_nodes.csv',V(citation)$numHorizontalDepth)
 
#### filter graph h depth 100
# in filtered graph if exists one attribute such that d <= 100 <=> min(d_attrs) <= 100
# -> can filter on horizontalDepth
citfiltered = induced_subgraph(citation,which(V(citation)$numHorizontalDepth<=100))
export_csv(citfiltered,'processed/core_hdepth100_edges.csv','processed/core_hdepth100_nodes.csv',V(citfiltered)$numHorizontalDepth)



#' 
#' # depth 100
#' d0names=V(citation)$name[V(citation)$depth==2&V(citation)$priority<=100]
#' d1 = adjacent_vertices(citation,V(citation)[V(citation)$depth==2&V(citation)$priority<=100])
#' d1names = unique(unlist(sapply(d1,function(l){l$name})))
#' d2 = adjacent_vertices(citation,V(citation)[d1names],mode='in')
#' d2names = unique(unlist(sapply(d2,function(l){l$name})))
#' 
#' d100 = induced_subgraph(citation,V(citation)[unique(c(d0names,d1names,d2names))])
#' 
#' citationcore = induced_subgraph(d100,which(degree(d100)>1))
#' citationcorehigher = citationcore
#' while(length(which(degree(citationcorehigher)==1))>0){citationcorehigher = induced_subgraph(citationcorehigher,which(degree(citationcorehigher)>1))}
#' 
#' # % missing ? ~ 500 remaining
#' length(which(V(citation)$depth>0)) # 500/140454
#' length(which(V(citationcorehigher)$depth>0)) #500/39537 -> around 1%
#' 
#' # % with year ?
#' length(which(!is.na(V(citationcorehigher)$year)))/vcount(citationcorehigher)
#' 
#' 
#' 
#' 
#' 
#' ##### old stuff
#' 
#' # get network at level 1
#' initialcorpus = read.csv('data/spatialmicrosim_corpus_spatial+microsimulation.csv',sep=";",colClasses = c('character','character','character'))
#' V(citation)$initial = V(citation)$name%in%initialcorpus$id
#' vdepth1=V(citation)[rep(FALSE,length(V(citation)))]
#' for(id in V(citation)$name[V(citation)$initial]){show(id);vdepth1=append(vdepth1,neighbors(citation,V(citation)$name==id,mode="in"))}
#' citationd1 =induced_subgraph(citation,vids = V(citation)$name%in%vdepth1$name)
#' # adjust reduced title degree
#' V(citationd1)$reduced_title = ifelse(degree(citationd1)>40,V(citationd1)$reduced_title,rep("",vcount(citationd1)))
#' 
#' mean(degree(citationd1,mode = 'in'))
#' 
#' write_graph(citationd1,file='data/spatialmicrosim_depth1.gml',format = 'gml')
#' 
#' vdepth0=V(citation)[V(citation)$initial]
#' citationd0 = induced_subgraph(citation,vids = vdepth0)
#' citationd0giant = induced_subgraph(citationd0,which(components(citationd0)$membership==1))
#' 
#' write_graph(citationd0,file='data/spatialmicrosim_depth0.gml',format = 'gml')
#' write_graph(citationd0giant,file='data/spatialmicrosim_depth0giantcomp.gml',format = 'gml')
#' 
#' mean(degree(citationd0giant,mode = 'in'))
#' 
#' # TODO :
#' # : separate two graphs ; see communities within each
#' # : check higher order core (while deg = 1)
#' 
#' ##
#' # size of two subgraphs / export for viz
#' #id = ""
#' #V(citation)[V(citation)$name==id]
#' #incid1=c(V(citation)[V(citation)$name==id],neighbors(citation,V(citation)$name==id,mode="in"))
#' #for(i in neighbors(citation,V(citation)$name==id,mode="in")){incid1=append(incid1,neighbors(citation,i,mode="in"))}
#' #write_graph(induced_subgraph(citation,incid1$name),file=paste0('data/',id,'.gml'),format = 'gml')
#' 
#' 
#' # density
#' ecount(citationcore)/(vcount(citationcore)*(vcount(citationcore)-1))
#' 
#' # mean degrees
#' mean(degree(citation))
#' mean(degree(citation,mode = 'in'))
#' mean(degree(citationcore,mode = 'in'))
#' mean(degree(citationcorehigher,mode = 'in'))
#' 
#' 
#' # modularity / vs null model
#' A=as_adjacency_matrix(citationcore,sparse = T)
#' M = A+t(A)
#' undirected_rawcore = graph_from_adjacency_matrix(M,mode="undirected")
#' 
#' # communities
#' com = cluster_louvain(undirected_rawcore)
#' 
#' directedmodularity(com$membership,A)
#' 
#' nreps = 100
#' mods = c()
#' for(i in 1:nreps){
#'   show(i)
#'   mods=append(mods,directedmodularity(com$membership,A[sample.int(nrow(A),nrow(A),replace = F),sample.int(ncol(A),ncol(A),replace = F)]))
#' }
#' 
#' show(paste0(mean(mods)," +- ",sd(mods)))
#' 
#' 
#' d=degree(citationcore,mode='in')
#' for(c in unique(com$membership)){
#'   show(paste0("Community ",c, " ; corpus prop ",length(which(com$membership==c))/vcount(undirected_rawcore)))
#'   #show(paste0("Size ",length(which(com$membership==c))))
#'   currentd=d[com$membership==c];dth=sort(currentd,decreasing = T)[10]
#'   show(data.frame(titles=V(citationcore)$title[com$membership==c&d>dth],degree=d[com$membership==c&d>dth]))
#'   #show(V(rawcore)$title[com$membership==c])
#' }
#' 
#' 
