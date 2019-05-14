setwd(paste0(Sys.getenv('CS_HOME'),'/UrbanDynamics/Models/QuantEpistemo'))

library(dplyr)
library(igraph)
library(ggplot2)

source('functions.R')

lang <- as.tbl(read.csv('language/lang_urbmod.csv',sep=';',header = F,colClasses = c('character','character')))
names(lang) = c('id','lang')

# TODO print failed
# + do not get lang if low confidence


table(lang$lang)

lang %>% filter(lang=='Latin')
# errors ?
 

#g = ggplot(lang%>%group_by(lang) %>% summarize(count=n()) %>% filter(count > 500) ,aes(x = lang,y = count,fill=lang))
#g+geom_bar()

g = ggplot(lang,aes(x=lang,fill=lang))
#g+geom_bar()

lang%>%group_by(lang) %>% summarize(count=n()) %>% filter(count > 500)



