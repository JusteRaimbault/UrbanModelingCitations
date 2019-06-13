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
import math #For mathematical expressions
import numpy as np #For fast array handling


############################
#0.2 Setup in and output paths
############################
#Where inputdata lives and output will be put
foldername_input ='/Users/Metti_Hoof/Desktop' 
foldername_output ='/Users/Metti_Hoof/Desktop/test_figures' 


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
'''
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
'''

########################################################
#3. Create Louvain La Neuve communities based on filtered graphs
########################################################

############################
#3.1 Calculate basic properties of the Louvain la-neuve partition per accumulative subgraphs over the years 
# It is not worth investigating for single years as they do not city each other a lot and so the graph has too little edges
############################

print 'We are calculating the Louvain-La-Neuve partition'

dict_year_subgraph_accumulative_partitions={}


for year in dict_year_subgraph_accumulative.keys():
	#calculate Louvain partition
	partition = community.best_partition(dict_year_subgraph_accumulative[year])

	#Write away partitions
	dict_year_subgraph_accumulative_partitions[year]=partition

	#Write away some properties
	dict_year_subgraph_accumulative_properties[year]['number_of_communities']=len(set(partition.values()))
	print year, " number of communities: ", len(set(partition.values()))

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
	print 'Loading the partition for year', year
	   
	#load Louvain partition
	partition = dict_year_subgraph_accumulative_partitions[year]

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

#dict_year_subgraph_accumulative_communities_top20_df_attributes[year]=df featuring the top 20 communities with several attributes
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
						'mean_horizontalDepth':df_nodes_tussen['horizontalDepth'].mean(skipna = True),
						'mean_microsim':df_nodes_tussen['microsim'].mean(skipna = True),
						'mean_transportmicrosimmode':df_nodes_tussen['transportmicrosimmodel'].mean(skipna = True),
						'mean_microsimmodel':df_nodes_tussen['microsimmodel'].mean(skipna = True),
						'mean_urbanmicrosimmodel':df_nodes_tussen['urbanmicrosimmodel'].mean(skipna = True),
						'mean_spatialmicrosimmodel':df_nodes_tussen['spatialmicrosimmodel'].mean(skipna = True),
						'mean_lutimodel':df_nodes_tussen['lutimodel'].mean(skipna = True),
						'mean_spatialmicrosim':df_nodes_tussen['spatialmicrosim'].mean(skipna = True),
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

##############
#4.2.1. Plot some characteristics of top 20 communities for each year
##############
'''
#Number of nodes bar charts
for year in dict_year_subgraph_accumulative_communities_top20_df_attributes.keys():
	print 'We are plotting the bar chart of the number of nodes for the top 20 communities of year', year
	df_top20_com=dict_year_subgraph_accumulative_communities_top20_df_attributes[year]
	
	ax = df_top20_com.plot.bar(y='number_of_nodes', rot=0)
	ax.set_ylim(0,1500) #limits based on 2019 max data
	
	# create a list to collect the plt.patches data
	totals = []

	# find the values and append to list
	for i in ax.patches:
		   totals.append(i.get_height())

	# set individual bar labels using above list
	total = sum(totals)

	# set individual bar labels using above list
	for i in ax.patches:
		   # get_x pulls left or right; get_height pushes up or down
		      ax.text(i.get_x()-.03, i.get_height()+10, \
				         str(int(i.get_height())), fontsize=9,color='dimgrey')
				       
	
	title ='Number of nodes for top 20 communities in year %s'%(year)
	plt.title(title)
	
	figure_name='/bar_chart_accumulative_years_top20_com_number_of_nodes_%s.png' %(year)
	output_figure=foldername_output+figure_name
	plt.savefig(output_figure)
	plt.close('all')




#Number of nodes bar charts
for year in dict_year_subgraph_accumulative_communities_top20_df_attributes.keys():
	print 'We are plotting the bar chart of mean horizontal depth for the top 20 communities of year', year
	df_top20_com=dict_year_subgraph_accumulative_communities_top20_df_attributes[year]
	
	ax = df_top20_com.plot.bar(y='mean_horizontalDepth', rot=0)
	ax.set_ylim(0,500) #limits based on data collection reality
	
	# create a list to collect the plt.patches data
	totals = []

	# find the values and append to list
	for i in ax.patches:
		   totals.append(i.get_height())

	# set individual bar lables using above list
	total = sum(totals)

	# set individual bar lables using above list
	for i in ax.patches:
		   # get_x pulls left or right; get_height pushes up or down
		      ax.text(i.get_x()-.03, i.get_height()+10, \
				         str(int(i.get_height())), fontsize=9,color='dimgrey')
				       
	
	title ='Mean horizontal depth (minimum per paper for all keywords) \n for top 20 communities in year %s'%(year)
	plt.title(title)
	
	figure_name='/bar_chart_accumulative_years_top20_com_mean_horizontal_depth_%s.png' %(year)
	output_figure=foldername_output+figure_name
	plt.savefig(output_figure)
	plt.close('all')



#Combinations of average horizontaldepths of keywords of the communities
for year in dict_year_subgraph_accumulative_communities_top20_df_attributes.keys():
	print 'We are plotting the bar chart of the average horizonatal depths for all keywords of the top 20 communities of year', year
	
	df_top20_com=dict_year_subgraph_accumulative_communities_top20_df_attributes[year]
	df_top20_com_avg_horizontaldepths=df_top20_com[['mean_microsim','mean_transportmicrosimmode','mean_microsimmodel',
												 'mean_urbanmicrosimmodel','mean_spatialmicrosimmodel',
												 'mean_lutimodel','mean_spatialmicrosim']]
	print year, df_top20_com_avg_horizontaldepths
	
	ax = df_top20_com_avg_horizontaldepths.plot.bar(rot=0)
	ax.set_ylim(0,500) #limit based on max horizontaldepth=400
	
	title ='Mean horizontal depths for different keywords \n for top 20 communities in year %s'%(year)
	plt.title(title)
	
	figure_name='/bar_chart_accumulative_years_top20_com_mean_horizontaldepths_for_all_keywords_%s.png' %(year)
	output_figure=foldername_output+figure_name
	plt.savefig(output_figure)
	plt.close('all')

'''

############################
#4.3. Investigate the top 20 communities.
############################

##############
#4.3.1. Create subgraph for all top 20 communities for each year
##############

#Create dict[year][communitynumber]=subgraph with only the nodes of this community
dict_year_subgraph_accumulative_communities_top20_subgraphs_per_year_per_com={}

for year in dict_year_subgraph_accumulative_communities_top20.keys():
	dict_year_subgraph_accumulative_communities_top20_subgraphs_per_year_per_com[year]={}
	
	dictee=dict_year_subgraph_accumulative_communities_top20[year]
	for com, list_of_nodes_in_com in dictee:
		print com, len(list_of_nodes_in_com)
		G_sub_com=G.subgraph(list_of_nodes_in_com).copy()
		print 'The number of nodes in this graph is: ', G_sub_com.number_of_nodes()
		dict_year_subgraph_accumulative_communities_top20_subgraphs_per_year_per_com[year][com]=G_sub_com
	

##############
#4.3.2. Visualise degree rank and subgraph for all top 20 communities for each year
##############
'''
for year in dict_year_subgraph_accumulative_communities_top20_subgraphs_per_year_per_com.keys():
		for com in dict_year_subgraph_accumulative_communities_top20_subgraphs_per_year_per_com[year]:
			G_sub_com=dict_year_subgraph_accumulative_communities_top20_subgraphs_per_year_per_com[year][com]
			
			degree_sequence = sorted([d for n, d in G_sub_com.degree()], reverse=True)
			# print "Degree sequence", degree_sequence
			dmax = max(degree_sequence)
			
			plt.loglog(degree_sequence, 'b-', marker='o')
			title ='Degree rank plot for nodes in top 20 communities no %s in year %s'%(com,year)
			plt.title(title)
			plt.ylabel("degree")
			plt.ylim(pow(10,0),pow(10,3))
			plt.xlabel("rank")
			plt.xlim(pow(10,0),pow(10,3))
			
			# draw graph in inset
			plt.axes([0.45, 0.45, 0.45, 0.45])
			Gcc = sorted(nx.connected_component_subgraphs(G_sub_com), key=len, reverse=True)[0]
			pos = nx.spring_layout(Gcc)
			plt.axis('off')
			nx.draw_networkx_nodes(Gcc, pos, node_size=10)
			nx.draw_networkx_edges(Gcc, pos, alpha=0.4)
			
			

			figure_name='/degree_rank_plot/degree_rank_plot_accumulative_years_top20_com_%s_%s.png' %(year,com)
			output_figure=foldername_output+figure_name
			plt.savefig(output_figure)
			plt.close('all')
			
			#plt.show()

'''

############################
#4.4. Investigating the consistency of the communities over time.
############################


##############
#4.1.1. Store membership to com per year + expand the original df_nodes dataset with information on membership to communities for each year
##############


#Create a dict that will hold dfs with nodes and community information per year
dict_year_subgraph_accumulative_communities_df_nodes_and_com={}

#Expand the original df_nodes dataset with information on membership to communities for each year 
df_nodes_com=df_nodes.copy()

for year in dict_year_subgraph_accumulative_communities.keys():
	print '\n We are investigating the membership of nodes in communities for', year

	#Load results of louvain partition per year, this is a dict with the different communities and community numbers.
	dict_tussen=dict_year_subgraph_accumulative_communities[year]
	
	#Create dataframe expressing the relation between nodes and community number in that year 
	#Rename column to have the year incorporated
	com_year='com_%s'%(year)
	
	df_louvain_nodes_com=pd.DataFrame([(com, node) for (com, list_of_nodes_in_com) in dict_tussen.items() for node in list_of_nodes_in_com], 
                 columns=[com_year, 'id'])
	
	#write away membershio for one year	
	dict_year_subgraph_accumulative_communities_df_nodes_and_com[year]=df_louvain_nodes_com
		
	
	
	#Expand the original df_nodes dataset with information on membership to communities for each year
	#by merging dataframe of nodes attributes with the information on community membership.
	
	df_louvain_nodes_com['id']=df_louvain_nodes_com['id'].astype(str) #set id as a string as we did in df_nodes. Otherwise the merge that follows throws an error
	df_nodes['id']=df_nodes['id'].astype(str)
	
	df_nodes_com = df_nodes_com.merge(df_louvain_nodes_com, on='id',how='left')
	

	#Check whether dimensions are still the same after the merge. 
	if df_nodes_com.shape[0] != df_nodes_com.shape[0]:
		print 'The merge we just performed has reduced the dimensions of your inputdata on employment and population. The shapes now are:'
		print df_nodes_com.shape
		print df_nodes.shape
	else:
		nodes_without_com=df_nodes_com[com_year].isna().sum()
		print 'The merge has not reduced our nodes dataframe. For the year', year, 'there are' , nodes_without_com, 'nodes without a community' 
		

	
# The df_nodes_com dataet now holds information on all the nodes and their membership to different communities over the years.
#print df_nodes_com.columns	
	
	
##############
#4.1.2. Create a df_nodes_com_top20 dataframe holding the community, whether this community is in the top 20 and the top20 rank for all nodes
##############

#create a df_nodes_com_top20 that stores membership to top20 or not for each year and each node.
df_nodes_com_top20=df_nodes_com.copy()

rank_com_year_list=[]
for year in dict_year_subgraph_accumulative_communities_top20_df_attributes.keys(): #dict_year_subgraph_accumulative_communities_top20_df_attributes[year]=df featuring the top 20 communities with several attributes
	df_of_top20_communities_for_that_year=dict_year_subgraph_accumulative_communities_top20_df_attributes[year][['com','rank_com']]
	print df_of_top20_communities_for_that_year
	
	com_year='com_%s'%(year)
	rank_com_year='rank_com_%s'%(year)
	rank_com_year_list.append(rank_com_year)
	top20_membership_year='top20_membership_%s'%(year)
	
	# Add a column to df_nodes_com_top20, expressing whether this node was in or out top 20
	df_nodes_com_top20[top20_membership_year]=np.where(df_nodes_com_top20[com_year].isin(df_of_top20_communities_for_that_year['com']), 'True', 'False')
	
	# Add a column to df_nodes_com_top20, expressing in which rank_com he was (rank_com is the rank of the biggest community in the top 20, ranging from 1 to 20)
	df_nodes_com_top20 = df_nodes_com_top20.merge(df_of_top20_communities_for_that_year, left_on=com_year, right_on='com',how='left')
	
	df_nodes_com_top20 = df_nodes_com_top20.rename(columns={'rank_com':rank_com_year}) #Change rank_com to rank_com_year
	df_nodes_com_top20 = df_nodes_com_top20.drop('com', axis=1) #Drop redundant 'com' column
	

##############
#4.1.3. Filter out nodes that are not in top20 communities for any of the years investigated
##############
#Create list of  the rank_com_year column names we have been using to indicate whether nodes are in top20 or not	
rank_com_year_list=[]
for year in dict_year_subgraph_accumulative_communities_top20_df_attributes.keys(): #dict_year_subgraph_accumulative_communities_top20_df_attributes[year]=df featuring the top 20 communities with several attributes
	
	rank_com_year='rank_com_%s'%(year)
	rank_com_year_list.append(rank_com_year)
	
#Drop all rows that have all NaN values in the subset columns. 
#So in our case we drop all rows that have a NaN for each rank_com_year columns, meaning that they were never in the top 20 . 
df_nodes_com_top20_filter=df_nodes_com_top20.dropna(subset=rank_com_year_list,how='all').copy() 

	
############Developing filter nodes of the per year top 20 communities ######################################


'''	
	#Sort communities by number of nodes and create a ranked top 20. 
	list_of_com_sorted_by_number_of_nodes=sorted(dict_tussen.items(), key=lambda (k, v): len(v), reverse=True) 
	top20_com=list_of_com_sorted_by_number_of_nodes[:20]
	
	#Create dataframe expressing the relation between nodes and community number in that year 
	#Rename column to have the year incorporated
	com_year='com_%s'%(year)
	
	df_louvain_top20_node_com=pd.DataFrame([(com, node) for (com, list_of_nodes_in_com) in top20_com for node in list_of_nodes_in_com], 
                 columns=[com_year, 'id'])
	
	
	#Get dataframe of all nodes that are in top 20 communities.
	full_list_of_nodes_in_top_20=[]
	for com,list_of_nodes_in_com in top20_com:
		
		full_list_of_nodes_in_top_20.extend(list_of_nodes_in_com)
		
	
	df_nodes_top20=df_nodes[df_nodes['id'].isin(full_list_of_nodes_in_top_20)].copy()
	
	#Merge dataframe of all nodes that are in top 20 communities with information on which community-year they are in.

	
	
	
	#write away
	dict_year_subgraph_accumulative_communities_top20_df_nodes[year]=df_nodes_top20

'''



###################################### Developing ######################################



'''

degree_sequence = sorted([d for n, d in G_sub_com.degree()], reverse=True)
# print "Degree sequence", degree_sequence
dmax = max(degree_sequence)

plt.loglog(degree_sequence, 'b-', marker='o')
plt.title("Degree rank plot")
plt.ylabel("degree")
plt.xlabel("rank")

# draw graph in inset
plt.axes([0.45, 0.45, 0.45, 0.45])
Gcc = sorted(nx.connected_component_subgraphs(G_sub_com), key=len, reverse=True)[0]
pos = nx.spring_layout(Gcc)
plt.axis('off')
nx.draw_networkx_nodes(Gcc, pos, node_size=20)
nx.draw_networkx_edges(Gcc, pos, alpha=0.4)

plt.show()
'''

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

