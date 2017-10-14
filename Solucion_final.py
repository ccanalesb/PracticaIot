#!/usr/bin/env python
import pdb
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import time
from random import randint
import math

G=nx.Graph()

distance = {}
best_nodes = {}
power_level = [15, 25, 55, 100]
nodes = 0
max_nodes = 10

plt.gca().invert_yaxis()
position = ""
def add_graphical_edge(G,i,k,peso):
	G.add_edge(i,k,weight=peso)
	G.add_edge(k,i)
	plt.clf()
	position = nx.get_node_attributes(G, 'pos')
	nx.draw(G,position,arrows=True)
	labels = nx.get_edge_attributes(G, 'weight')
	nx.draw_networkx_edge_labels(G, position, edge_labels=labels)
	nx.draw_networkx_labels(G, position, labels=None)
	plt.draw()	

for i in range(0,max_nodes):
	if nodes < max_nodes:
		G.add_node(nodes, pos=(randint(0, 50), randint(0, 50) ))
		nodes = nodes + 1
		position = nx.get_node_attributes(G, 'pos')
		nx.draw(G,position,with_labels=True)
		plt.figure(1)
		plt.draw()
		

for i in range(0,len(G)):
	for j in range(0, len(G)):
		node_dist = math.hypot(G.node[j]['pos'][0] - G.node[i]['pos'][0], G.node[j]['pos'][1] - G.node[i]['pos'][1])
		node_dist = round(node_dist,1)
		node_dist = (j,node_dist)
		distance.setdefault(i, [])
		distance[i].append(node_dist)
		distance[i].sort(key=lambda tup: tup[1])
		if j == len(G)-1: 
			i_is_connected = False
			i_level_conected = 0
			print "**************************************"	
			print "REVISANDO NODO " + str(i)
			for k in range(0, len(distance[i])): 
				print " con nodo "+str(distance[i][k][0])+ " y peso "+str(distance[i][k][1])
				if i != k:
					peso = distance[i][k][1]
					if peso > 0 and peso <= power_level[0]:
						print "\tMi distancia esta en nivel 1 y mi ultimo conectado es "+ str(i_level_conected)
						add_graphical_edge(G,i,distance[i][k][0],peso)						
						i_is_connected = True
						i_level_conected = power_level[0]
					if peso > power_level[0] and peso <= power_level[1]:	
						print "\tMi distancia esta en nivel 2 y mi ultimo conectado es "+ str(i_level_conected)
						if i_is_connected and i_level_conected == power_level[1]:	
							print "\t-->encontre en mi mismo nivel"
							add_graphical_edge(G,i,distance[i][k][0],peso)									
							i_is_connected = True					
							i_level_conected = power_level[1]			
						elif i_is_connected == False and i_level_conected == 0:
							print "\t->Primera conexion en nivel 2"
							add_graphical_edge(G,i,distance[i][k][0],peso)									
							i_is_connected = True
							i_level_conected = power_level[1]
					if peso > power_level[1] and peso <= power_level[2]:	
						print "\tMi distancia esta en nivel 3 y mi ultimo conectado es "+ str(i_level_conected)
						if i_is_connected and i_level_conected == power_level[2]:	
							print "\t-->encontre en mi mismo nivel"
							add_graphical_edge(G,i,distance[i][k][0],peso)									
							i_is_connected = True					
							i_level_conected = power_level[2]			
						elif i_is_connected == False and i_level_conected == 0:
							print "\t->Primera conexion en nivel 3"
							add_graphical_edge(G,i,distance[i][k][0],peso)								
							i_is_connected = True
							i_level_conected = power_level[2]			
					if peso > power_level[2] and peso <= power_level[3]:
						print "\tMi distancia esta en nivel 4 y mi ultimo conectado es "+ str(i_level_conected)
						if i_is_connected == False and i_is_connected <= power_level[3]:
							print "\t->Primera conexion en nivel 4"
							add_graphical_edge(G,i,distance[i][k][0],peso)										
							i_is_connected = True
							i_level_conected = power_level[3]																		
	print distance[i]
	distance = {}		


print "calculando T"

# T=nx.minimum_spanning_tree(G)
position = nx.get_node_attributes(G, 'pos')
plt.gca().invert_yaxis()
# plt.figure(2)
# nx.draw(T,position,arrows=True,edge_color='r')
# labels = nx.get_edge_attributes(T, 'weight')
# nx.draw_networkx_edge_labels(T, position, edge_labels=labels)
nx.draw_networkx_labels(G, position, labels=None)
plt.draw()
plt.savefig("solemne2.png")

number_of_edges = 0
# for i in T.edges():
# 	best_nodes.setdefault(i[0], [])
# 	best_nodes[i[0]].append(i[1])
# print best_nodes
# print max(x, value=x.get)	
# best_node = ()
# for i in best_nodes:
# 	if best_node <= len(best_nodes[i]):
# 		best_node.append(i,len(best_nodes[i]))
# print best_node		
# 	for j in range(0, len(T)):
# 		print "Para el nodo "+str(i)
# 		print T.edges()
# print(sorted(T.edges(data=True)))

# plt.draw()
# plt.pause(0.2)
plt.savefig("solemne.png")
plt.show()