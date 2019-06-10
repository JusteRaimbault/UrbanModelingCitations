
##############################################################################################
# -*- coding: utf-8 -*-
# Script to test some community detection on the urbanmodeling citations
# Data was provided by Juste Raimbault: https://github.com/JusteRaimbault/UrbanModelingCitations/processed
# Written by Maarten Vanhoof, may 2019
# Python 2.7
#
##############################################################################################

print("The script is starting")


########################################################
#0. Setup environment
########################################################

############################
#0.1 Import dependencies
############################

import community #For Louvain la neuve algorithm. Be aware though, in pypi this module is called: python-louvain
import networkx as nx #For Network handling
import matplotlib.pyplot as plt  #For interactive plotting
import pandas as pd #For data handling


############################
#0.2 Setup in and output paths
############################
#Where inputdata lives and output will be put
foldername_input ='/Users/Metti_Hoof/Desktop' 
foldername_output ='/Users/Metti_Hoof/Desktop' 


########################################################
#1. Read in inputfiles
########################################################
############################
#1.1 Set names of inputfiles
############################

#inputfiles for edges
inputfile_edges= foldername_input + '/UrbanModelingCitations-master/processed/core_hdepth400_filtered_edges_without_headers.csv' 

#inputfiles for edges sample
inputfile_edges_sample= foldername_input + '/UrbanModelingCitations-master/processed/core_hdepth400_filtered_edges_sample.csv' 

#inputfiles for nodes
inputfile_nodes= foldername_input + '/UrbanModelingCitations-master/processed/core_hdepth400_filtered_nodes.csv' 

#inputfiles for full directed graph created bu Juste
#inputfile_directed_graph= foldername_input + '/UrbanModelingCitations-master/processed/core_hdepth100.gml' 


########################################################
#2. Setup graphs
########################################################

############################
#2.1 Load in graphs based on edges list
############################

print 'Loading in the graphs'

# Random Erdos Renyi Graph 
#F = nx.erdos_renyi_graph(30, 0.05)

# Graph based on the inputfile_edges(sample). 
G=nx.read_edgelist(inputfile_edges,delimiter=',', nodetype=str)#inputfile_edges_sample.


############################
#2.1 Attach nodes with information from the inputfile for nodes (such as data and depth)
############################

#To attach information to nodes, we need to feed the set_node_attributes function with a dictionary, 
#or a dict of dict in which the upper key is the identifier of the node. 

#Read in in pandas
df_nodes=pd.read_csv(inputfile_nodes)

#Get only the columns we need and convert years to int and 
df_nodes_attr=df_nodes.copy()#df_nodes_ten=df_nodes.head(10).copy()

df_nodes_attr['year']=df_nodes_attr['year'].fillna(0).astype(int)
df_nodes_attr['id']=df_nodes_attr['id'].astype(str)
#Set id as index, create a dict of dicts where main key is id en subkeys are colums names
df_nodes_attr=df_nodes_attr.set_index('id')
dict_nodes_attr=df_nodes_attr.to_dict(orient='index')

#Attache dict with attr. to nodes in the networkx graph
if isinstance (dict_nodes_attr, dict):
	print 'We are now setting the node attributes'
	nx.set_node_attributes(G, dict_nodes_attr)

#Print nodes and attribute data in graph G
#for node, data in G.nodes(data=True): #data=True is the argument to print attribute data
	#print node
	#print data

############################
#2.2 Investigate properties of the graph
############################
print 'The number of nodes for our entire graph G:' 
print G.number_of_nodes()

print 'The number of edges for our entire graph G:' 
print G.number_of_edges()

#List of all neighbours for node with id 3647790169908411033
#list(G.adj['3647790169908411033'])  # or list(G.neighbors(3647790169908411033))

#Get the degree of the node with id 3647790169908411033. Remark that for directed graphs, the degree is the sum of in and out degrees.
#G.degree['3647790169908411033']  


############################
#2.4 Plot a bar chart indicating the amount of papers per year.
############################
'''
list_filter_years=[2019,2018,2017,2016,2015,2014,2013,2012,2011,2010,2009,2008,2007,2006,2005,2004,2003,2002,2001,2000,1999,1998,1997,1996,1995,
1994,1993,1992,1991,1990,1989,1988,1987,1986,1985,1984,1983,1982,1981,1980,1979,1978,1977,1976,1975,1974,1973,1972,1971,1970,1969,1968,1967,1966,1965,1964,1963,
1962,1961,1960,1959,1958,1957,1956,1955,1954,1953,1952,1951,1950,1949,1948,1947,1946,1945,1944,1943,1942,1941,1940]

dict_year_count={}

for filter_year in list_filter_years:
	G_sub_year = (node for node in G if G.node[node]['year']==filter_year)
	dict_year_count[filter_year]=len(list(G_sub_year))

plt.bar(*zip(*dict_year_count.items()))
plt.show()
plt.close('ALL')
'''

############################
#2.4 Plot a bar chart indicating the amount of papers published up untill that year.
############################
'''
list_filter_years=[2019,2018,2017,2016,2015,2014,2013,2012,2011,2010,2009,2008,2007,2006,2005,2004,2003,2002,2001,2000,1999,1998,1997,1996,1995,
1994,1993,1992,1991,1990,1989,1988,1987,1986,1985,1984,1983,1982,1981,1980,1979,1978,1977,1976,1975,1974,1973,1972,1971,1970,1969,1968,1967,1966,1965,1964,1963,
1962,1961,1960,1959,1958,1957,1956,1955,1954,1953,1952,1951,1950,1949,1948,1947,1946,1945,1944,1943,1942,1941,1940]

dict_year_count={}

for filter_year in list_filter_years:
	# Some of the nodes have year=0 because of preprocessing before
	G_sub_year = (node for node in G if G.node[node]['year']<=filter_year and G.node[node]['year']!=0)
	dict_year_count[filter_year]=len(list(G_sub_year))

plt.bar(*zip(*dict_year_count.items()))
plt.title("Accumulative number of published papers until that year")
figure_name='/test_number_of_papers.png'
output_figure=foldername_output+figure_name
plt.savefig(output_figure)
#plt.show()
plt.close('all')
'''
############################
#2.5 Save and load the full graph with attributes as a gml.
#This doesn't work yet because of unicode problems.
############################
'''
inbetween_outputname='/test.gml'
inbetween_output=foldername_output+inbetween_outputname

#Store graph as GML
nx.write_gml(G, inbetween_output)

#Read in graph from GML
H=nx.read_gml(inbetween_output)

'''

########################################################
#3. Filter graph based on attributes 
########################################################

############################
#3.1 Filter graph by one year, plot filtered out elements.
############################
'''
list_node = list(node for node in G if G.node[node]['year']==2018)
G_sub_year=G.subgraph(list_node).copy()


pos = nx.spring_layout(G)  #setting the positions with respect to G, not G_sub_year.

plt.figure()
nx.draw_networkx(G, pos=pos, node_color = 'b',node_size = 2, with_labels=False)
nx.draw_networkx(G_sub_year, pos=pos, node_color= 'r',node_size = 2, with_labels=False)

plt.show()
plt.close('ALL')
'''

############################
#3.2 Filter graphs by all years and by years accumulatively
############################

list_filter_years=[2019,2018,2017,2016,2015,2014,2013,2012,2011,2010,2009,2008,2007,2006,2005,2004,2003,2002,2001,2000,1999,1998,1997,1996,1995,
1994,1993,1992,1991,1990,1989,1988,1987,1986,1985,1984,1983,1982,1981,1980,1979,1978,1977,1976,1975,1974,1973,1972,1971,1970,1969,1968,1967,1966,1965,1964,1963,
1962,1961,1960,1959,1958,1957,1956,1955,1954,1953,1952,1951,1950,1949,1948,1947,1946,1945,1944,1943,1942,1941,1940]


list_filter_years=[2019,2018,2017,2016,2015,2014,2013,2012,2011,2010,2009,2008,2007,2006,2005,2004,2003,2002,2001,2000,1999,1998,1997,1996,1995,
1994,1993,1992,1991,1990,1989,1988,1987]

list_filter_years=[2006,2005,2004]



dict_year_subgraph_accumulative={}
for filter_year in list_filter_years:
	print 'We are treating filter year for the accumulative subgraph: ', filter_year
	# Some of the nodes have year=0 because of preprocessing before
	list_node = list(node for node in G if G.node[node]['year']<=filter_year and G.node[node]['year']!=0)
	G_sub_year=G.subgraph(list_node).copy()
	print 'The number of nodes in this graph is: ', G_sub_year.number_of_nodes()
	
	dict_year_subgraph_accumulative[filter_year]=G_sub_year

'''
dict_year_subgraph={}
for filter_year in list_filter_years:
	print 'We are treating filter year: ', filter_year
	
	list_node = list(node for node in G if G.node[node]['year']==filter_year)
	G_sub_year=G.subgraph(list_node).copy()
	print 'The number of nodes in this graph is: ', G_sub_year.number_of_nodes()
	
	dict_year_subgraph[filter_year]=G_sub_year
'''

############################
#3.3 Explore some basic properties for the accumulative year subgraphs
############################

#Helpfunction: Get top 10 nodes of centrality measures
def get_top_keys(dictionary, top):
	items = dictionary.items()
	items.sort(reverse=True, key=lambda x: x[1])
	return map(lambda x: x[0], items[:top])


dict_year_subgraph_accumulative_properties={}
for year in dict_year_subgraph_accumulative.keys():
	print 'We are calculating the basic properties for the accumulative network until year: ', year
	dict_year_subgraph_accumulative_properties[year]={}

	dict_year_subgraph_accumulative_properties[year]['number_of_nodes']=dict_year_subgraph_accumulative[year].number_of_nodes()
	dict_year_subgraph_accumulative_properties[year]['number_of_edges']=dict_year_subgraph_accumulative[year].number_of_edges()
	dict_year_subgraph_accumulative_properties[year]['average_clustering']=nx.average_clustering(dict_year_subgraph_accumulative[year])

	'''
	dict_year_subgraph_accumulative_properties[year]['betweenness_centrality']=nx.betweenness_centrality(dict_year_subgraph_accumulative[year])
	dict_year_subgraph_accumulative_properties[year]['closeness_centrality']=nx.closeness_centrality(dict_year_subgraph_accumulative[year])
	dict_year_subgraph_accumulative_properties[year]['eigenvector_centrality']=nx.eigenvector_centrality(dict_year_subgraph_accumulative[year])

	dict_year_subgraph_accumulative_properties[year]['top10_nodes_betweenness_centrality']=get_top_keys(dict_year_subgraph_accumulative_properties[year]['betweenness_centrality'],10)
	dict_year_subgraph_accumulative_properties[year]['top10_nodes_closeness_centrality']=get_top_keys(dict_year_subgraph_accumulative_properties[year]['closeness_centrality'],10)
	dict_year_subgraph_accumulative_properties[year]['top10_nodes_eigenvector_centrality']=get_top_keys(dict_year_subgraph_accumulative_properties[year]['eigenvector_centrality'],10)
	'''

############################
#3.4. Plot some calculated attributes of the subgraphs
############################

#Plot bar chart of variable per year in the dict_year_subgraph_accumulative_properties
variables_to_plot=['average_clustering',
					'number_of_edges',
					'number_of_nodes'
					]

for variable in variables_to_plot:
	print 'We are plotting a bar chart for variable: ', variable
	list_year=[]
	list_variable=[]

	for year in dict_year_subgraph_accumulative_properties.keys():
		list_year.append(year)
		list_variable.append(dict_year_subgraph_accumulative_properties[year][variable])

	plt.bar(list_year,list_variable)

	if variable=='number_of_communities':
		title="Number of communities by Louvain methods \n for the accumulative subgraph of each year"
	elif variable=='louvain_modularity':
		title="Modularity of communities by Louvain methods  \n for the accumulative subgraph of each year"
	elif variable=='number_of_nodes':
		title="Accumulative number of published papers until that year"
	else:
		title="%s for the accumulative subgraph of each year" %(variable)
	
	plt.title(title) 
	figure_name='/%s_bar_chart_accumulative_years.png' %(variable)
	output_figure=foldername_output+figure_name
	plt.savefig(output_figure)
	plt.close('all')


########################################################
#3. Create Louvain La Neuve communities based on filtered graphs
########################################################

############################
#3.1 Calculate basic properties of the Louvain la-neuve partition per accumulative subgraphs over the years 
# It is not worth investigating for single years as they do not city each other a lot and so the graph has too little edges
############################

print 'We are calciultating the Louvain-La-Neuve partition'

for year in dict_year_subgraph_accumulative.keys():
	#calculate Louvain partition
	partition = community.best_partition(dict_year_subgraph_accumulative[year])
	number_of_communities=len(set(partition.values()))
	print year, " number of communities: ", number_of_communities
	
	#Write away
	dict_year_subgraph_accumulative_properties[year]['number_of_communities']=number_of_communities

	if dict_year_subgraph_accumulative[year].number_of_edges()>0: #You can only calculate the modularity if there are nodes in the graph
		#Calculate modularity when possible
		modularity=community.modularity(partition, dict_year_subgraph_accumulative[year])
		print year, "Louvain Modularity: ", modularity
		
		#Write away
		dict_year_subgraph_accumulative_properties[year]['louvain_modularity']=modularity

	else:
		#Write away a zero
		dict_year_subgraph_accumulative_properties[year]['louvain_modularity']=0
		print ' There are no edges in the graph of the year ', year


############################
#3.2. Plot louvain modularity of the subgraphs per accumulated year
############################
'''
#Plot bar chart of variable per year in the dict_year_subgraph_accumulative_properties
variables_to_plot=['louvain_modularity',
					'number_of_communities'
					]

for variable in variables_to_plot:
	print 'We are plotting a bar chart for variable: ', variable
	list_year=[]
	list_variable=[]

	for year in dict_year_subgraph_accumulative_properties.keys():
		list_year.append(year)
		list_variable.append(dict_year_subgraph_accumulative_properties[year][variable])

	plt.bar(list_year,list_variable)

	if variable=='number_of_communities':
		title="Number of communities by Louvain methods \n for the accumulative subgraph of each year"
	elif variable=='louvain_modularity':
		title="Modularity of communities by Louvain methods  \n for the accumulative subgraph of each year"
	elif variable=='number_of_nodes':
		title="Accumulative number of published papers until that year"
	else:
		title="%s for the accumulative subgraph of each year" %(variable)
	
	plt.title(title) 
	figure_name='/%s_bar_chart_accumulative_years.png' %(variable)
	output_figure=foldername_output+figure_name
	plt.savefig(output_figure)
	plt.close('all')

'''

########################################################
#4. Investigate the louvain communities over time 
########################################################

############################
#4.1. Create a dict that gives you: dict[year][community]=[list of all nodes in this community]
############################
####### Note that we redo the louvain la neuve algo here, this is time consuming but easier to organise the code. 

print 'We are investigating the communities of the Louvain-La-Neuve partition'

dict_year_subgraph_accumulative_communities={}

#Structure of dict_year_subgraph_accumulative_communities is:
#dict_year_subgraph_accumulative_communities[year][community]=[list of all nodes in this community]

for year in dict_year_subgraph_accumulative.keys():
	print 'Calculating the partition for a second time for year', year
	#calculate Louvain partition
	partition = community.best_partition(dict_year_subgraph_accumulative[year])

	#initiate a dict tussen that will have community number as key and a list as values (which will be filled up later with the list of nodes that belong to it)
	dict_tussen={}
	for com in set(partition.values()): #values are the accorded communities, set takes the uniques of those
		dict_tussen[com]=[]
 	#fill up dict tussen with nodes that belong to a community.
	for node,com in partition.iteritems():
		#print node,com
 		dict_tussen[com].append(node)

	#Write away
	dict_year_subgraph_accumulative_communities[year]=dict_tussen


############################
#4.2. Get the top 20 communities of each year, perform some basic analysis on them.
############################

#dict_year_subgraph_accumulative_communities_top20[year]=list of lists with the names of the top 20 communities and their nodes
dict_year_subgraph_accumulative_communities_top20={}

#dict_year_subgraph_accumulative_communities_top20_df_attributes[year][community]=df featuring the top 20 communities with several attributes
dict_year_subgraph_accumulative_communities_top20_df_attributes={}


for year in dict_year_subgraph_accumulative_communities.keys():
	print 'We are investigating the top 20 communities in terms of number of nodes for the year', year

	#Load results of louvain partition per year, this is a dict with 
	dict_tussen=dict_year_subgraph_accumulative_communities[year]
	
	#Sort communities by number of nodes and create a ranked top 20. 
	list_of_com_sorted_by_number_of_nodes=sorted(dict_tussen.items(), key=lambda (k, v): len(v), reverse=True) 
	top20_com=list_of_com_sorted_by_number_of_nodes[:20]

	#Write away list of lists of top20 with com number and list of nodes
	dict_year_subgraph_accumulative_communities_top20[year]=top20_com

	#Gather information about the top 20 communities store them in a dataframe
	df_top20_com=pd.DataFrame()

	#add a rank number with 1 being the biggest and 20 being the 20th biggest
	rank_count=1

	for com,list_of_nodes in top20_com:
		#Calculate somne characteristics of the community & Write away in dataframe
		df_nodes_tussen=df_nodes[df_nodes['id'].isin(list_of_nodes)]

		df_top20_com=df_top20_com.append({
						'com': com,
						'rank_com':rank_count,
						'number_of_nodes':len(list_of_nodes),
						'average_year':df_nodes_tussen['year'].mean(skipna = True),
						'sum_horizontalDepth':df_nodes_tussen['horizontalDepth'].sum(skipna = True),
						'sum_microsim':df_nodes_tussen['microsim'].sum(skipna = True),
						'sum_transportmicrosimmode':df_nodes_tussen['transportmicrosimmodel'].sum(skipna = True),
						'sum_microsimmodel':df_nodes_tussen['microsimmodel'].sum(skipna = True),
						'sum_urbanmicrosimmodel':df_nodes_tussen['urbanmicrosimmodel'].sum(skipna = True),
						'sum_spatialmicrosimmodel':df_nodes_tussen['spatialmicrosimmodel'].sum(skipna = True),
						'sum_lutimodel':df_nodes_tussen['lutimodel'].sum(skipna = True),
						'sum_spatialmicrosim':df_nodes_tussen['spatialmicrosim'].sum(skipna = True),
						#'language_count_English':df_nodes_tussen['lang'].value_counts()['English'],
						#'language_count_English_relative':df_nodes_tussen['lang'].value_counts()['English']/float(len(list_of_nodes))*100
						#'language_count_Chinese':df_nodes_tussen['lang'].value_counts()['Chinese'],
						#'language_count_Chinese_relative':df_nodes_tussen['lang'].value_counts()['Chinese']/float(len(list_of_nodes))*100
						},ignore_index=True)

		######### Note that if the sum of keywords horizontaldepths equals 0 this means that all nodes have a NaN for this keyword. ############

		#Write away
		dict_year_subgraph_accumulative_communities_top20_df_attributes[year]=df_top20_com

		#Update rank_count
		rank_count=rank_count+1







###################################### Developing ######################################

'''
df_nodes_tussen['lang'].value_counts(),




	df_top20_com.append({'com': com,
					'rank_com':rank_count,
					'number_of_nodes':len(list_of_nodes)
					},ignore_index=True)




df_top20_com.append({
					'com': com,
					'rank_com':rank_count,
					'number_of_nodes':len(list_of_nodes)
					}
					,ignore_index=True)

df_top20_com.append({'com': 23}, ignore_index=True)
df_top20_com.append({'com': 24}, ignore_index=True)




	#Store in dataframe
	dict_top20_com[rank_count]={}
	dict_top20_com[rank_count]['number_of_nodes']=len(list_of_nodes)
	dict_top20_com[rank_count]['average_year']=df_nodes_tussen['year'].mean(skipna = True)
	dict_top20_com[rank_count]['sum_horizontalDepth']=df_nodes_tussen['horizontalDepth'].sum(skipna = True) #horizontalDepth is the minimum of the different keyword scores.
	dict_top20_com[rank_count]['sum_horizontalDepth']=df_nodes_tussen['horizontalDepth'].sum(skipna = True)
	dict_top20_com[rank_count]['sum_horizontalDepth']=df_nodes_tussen['horizontalDepth'].sum(skipna = True)
	dict_top20_com[rank_count]['sum_horizontalDepth']=df_nodes_tussen['horizontalDepth'].sum(skipna = True)





u'id', u'title', u'lang', u'year', u'depth', u'horizontalDepth',
       u'microsim', u'transportmicrosimmodel', u'microsimmodel',
       u'urbanmicrosimmodel', u'spatialmicrosimmodel', u'lutimodel',
       u'spatialmicrosim'


#drawing
size = float(len(set(partition.values())))
pos = nx.spring_layout(G)
count = 0.
for com in set(partition.values()) :
    count = count + 1.
    list_nodes = [nodes for nodes in partition.keys()
                                if partition[nodes] == com]
    nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20,
                                node_color = str(count / size))


nx.draw_networkx_edges(G, pos, alpha=0.5)
plt.show()


'''




'''
plt.title("Number of communities by Louvain methods \n for the accumulative subgraph of each year")
plt.bar(*zip(*dict_year_subgraph_accumulative_communities.items()))
figure_name='/test_communities.png'
output_figure=foldername_output+figure_name
plt.savefig(output_figure)
#plt.show()
plt.close('ALL')



plt.title("Modularity of communities by Louvain methods  \n for the accumulative subgraph of each year")
plt.bar(*zip(*dict_year_subgraph_accumulative_communities_modularity.items()))
figure_name='/test_modularity.png'
output_figure=foldername_output+figure_name
plt.savefig(output_figure)
#plt.show()
plt.close('ALL')
'''


'''
	if dict_year_subgraph_accumulative[year].number_of_edges()>100: #You can only calculate the modularity if there are nodes in the graph
		#Calculate modularity when possible
		modularity=community.modularity(partition, dict_year_subgraph[year])
		#Write away
		dict_year_subgraph_accumulative_communities[year]["modularity"]=len(set(partition.values()))

		 "Louvain Modularity: ", modularity
	elif dict_year_subgraph_accumulative[year].number_of_edges()==0:
		print year, "no edges in this graph"

	


plt.show()
plt.close('ALL')

plt.title("Number of communities by Louvain methods for the accumulative subgraph of each year")
plt.bar(*zip(*dict_year_subgraph_communities.items()))
plt.show()
plt.close('ALL')



	G_sub_year = (node for node in G if G.node[node]['year']==filter_year)
	partition = community.best_partition(G)
	print filter_year,len(set(partition.values())),"Louvain Modularity: ", community.modularity(partition, dict_year_subgraph[year])
	dict_year_subgraph_communities[filter_year]=len(set(partition.values()))


plt.bar(*zip(*dict_year_subgraph_communities.items()))
plt.show()
plt.close('ALL')
'''

########################################################
#3. Compute communities
########################################################

############################
#3.1 Partition by Louvain-La-Neuve
############################
'''
#Compute the best partition based on the community module which uses the Louvan la neuve algorithm.
partition = community.best_partition(G)
print "Louvain Modularity: ", community.modularity(partition, G)	
'''
############################
#3.2 Draw the partitioned graph
############################
'''
#drawing
size = float(len(set(partition.values())))
pos = nx.spring_layout(G)
count = 0.
for com in set(partition.values()) :
    count = count + 1.
    list_nodes = [nodes for nodes in partition.keys()
                                if partition[nodes] == com]
    nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20,
                                node_color = str(count / size))

nx.draw_networkx_edges(G, pos, alpha=0.5)
plt.show()


figure_name='/test.png'
output_figure=foldername+figure_name
plt.savefig(output_figure)
plt.close('ALL')
'''

