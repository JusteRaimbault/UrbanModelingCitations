setwd(paste0(Sys.getenv('CS_HOME'),'/UrbanDynamics/Models/QuantEpistemo'))

library(dplyr)
library(igraph)
library(ggplot2)
library(glue)

source(paste0(Sys.getenv('CS_HOME'),'/Organisation/Models/Utils/R/plots.R'))

source('functions.R')

lang <- as.tbl(read.csv('language/lang_urbmod.csv',sep=';',header = T,colClasses = c('character','character','numeric','character')))
lang2 <- as.tbl(read.csv('language/lang_spatialmicrosim.csv',sep=';',header = T,colClasses = c('character','character','numeric','character')))
lang$id = trim(lang$id);lang2$id = trim(lang2$id)

lang = rbind(lang,lang2)
lang=lang[!duplicated(lang$id),]

# filter unreliable

# check some middle confidence results
lang %>% filter(confidence>40&confidence<80&reliable=='False') # some missclassified, some bilingual -> remove
lang %>% filter(confidence>40&confidence<80&reliable=='True') # bof - eng words in korean title, etc
lang %>% filter(confidence>80&confidence<90&reliable=='True') # ok 
# => arbitrary confidence threshold of 0.8

lang <- lang %>% filter(reliable=='True'&confidence>80)

table(lang$lang)

lang %>% filter(lang=='Latin')
# errors ? - still errors - 96% confidence e.g.
lang %>% filter(lang=='Breton') # people names !

lcount = lang%>%group_by(lang) %>% summarize(count=n()) %>% filter(count > 500)

lang <- lang %>% filter(lang %in% lcount$lang)

#g = ggplot(lang%>%group_by(lang) %>% summarize(count=n()) %>% filter(count > 500) ,aes(x = lang,y = count,fill=lang))
#g+geom_bar()

g = ggplot(lang%>%group_by(lang) %>% summarize(count=n()),aes(x="",y=count,fill=lang))
g+geom_bar(stat='identity')+coord_polar("y", start=0)+xlab("")+ylab("")+scale_fill_discrete(name='Language')+stdtheme
ggsave('results/languages.png',width=17,height = 15,units='cm')




