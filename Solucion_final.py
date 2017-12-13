#!/usr/bin/env python
import pdb
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import time
from random import randint
import math
from networkx.algorithms import approximation as approx
from networkx.algorithms import traversal as tr
from networkx.algorithms import tree as tree
from networkx.drawing.nx_agraph import graphviz_layout

G = nx.Graph()

distance = {}
best_nodes = {}
power_level = [15, 25, 55, 75]
nodes = 0
max_nodes = 15

plt.gca().invert_yaxis()
position = ""


'''
ESTA ES LA EXPLICACION DEL ALGORITMO DE REUTILIZACION DE CANALES

Se convierte el grafo en un arbol, donde la cantidad de hijos de 
cada nodo son los nodos existentes en el primer nivel de conexion que tenga el nodo.
Luego, se recorre dicho arbol en BFS y se reserva un timeslot por cada nodo
hijo en el orden del BFS.

'''

def hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, 
				  pos = None, parent = None):
	'''If there is a cycle that is reachable from root, then this will see infinite recursion.
	   G: the graph
	   root: the root node of current branch
	   width: horizontal space allocated for this branch - avoids overlap with other branches
	   vert_gap: gap between levels of hierarchy
	   vert_loc: vertical location of root
	   xcenter: horizontal location of root
	   pos: a dict saying where all nodes go if they have been assigned
	   parent: parent of this branch.'''
	if pos == None:
		pos = {root:(xcenter,vert_loc)}
	else:
		pos[root] = (xcenter, vert_loc)
	neighbors = G[root]
	# if parent != None:   #this should be removed for directed graphs.
	#     neighbors.remove(parent)  #if directed, then parent not in neighbors.
	if len(neighbors)!=0:
		dx = width/len(neighbors) 
		nextx = xcenter - width/2 - dx/2
		for neighbor in neighbors:
			nextx += dx
			pos = hierarchy_pos(G,neighbor, width = dx, vert_gap = vert_gap, 
								vert_loc = vert_loc-vert_gap, xcenter=nextx, pos=pos, 
								parent = root)
	return pos

def add_graphical_edge(G, i,k , peso):
	G.add_edge(i, k, weight=peso)
	G.add_edge(k, i)
	plt.clf()
	position = nx.get_node_attributes(G, 'pos')
	nx.draw(G,position,arrows=True)
	labels = nx.get_edge_attributes(G, 'weight')
	nx.draw_networkx_edge_labels(G, position, edge_labels=labels)
	nx.draw_networkx_labels(G, position, labels=None)
	plt.draw()	

# Permite encontrar nodos no vecinos
def non_neighbors_nodes(G,root):
	edges = tr.bfs_edges(G,root)
	item = [root] + [v for u, v in edges]
	result = {}
	print item
	for i in item:
		print "nodo ", i, " = ",list(nx.non_neighbors(G,i))
		result[i] = list(nx.non_neighbors(G,i))
	return (item,result)

def calculate_matrix(bfs,non_neighbors):
	the_matrix = [None] * 4
	for i in range(0,4):
		the_matrix[i]= []
	matrix_index = 0
	matrix_position = 0
	for i in range(0,len(bfs)):
		neighbors = list(set(bfs)-set(non_neighbors[bfs[i]]))
		print neighbors
		for j in range(0,len(neighbors)):
			if bfs[i] == neighbors[j]:
				continue
			if matrix_index < 4:
				the_matrix[matrix_index].append( (str(bfs[i]) + '->' + str(neighbors[j]), (str(matrix_position))+' in '+ str(matrix_index) ))
				matrix_position += 1
			else:
				matrix_index = 0
			matrix_index += 1
		
	print the_matrix


for i in range(0,max_nodes):
	if nodes < max_nodes:
		G.add_node(nodes, pos=(randint(0, 200), randint(0, 200) ))
		nodes = nodes + 1
		position = nx.get_node_attributes(G, 'pos')
		nx.draw(G,position,with_labels=True)
		plt.figure(1)
		plt.draw()


for i in range(0, len(G)):
	for j in range(0, len(G)):
		node_dist = math.hypot(G.node[j]['pos'][0] - G.node[i]['pos'][0], G.node[j]['pos'][1] - G.node[i]['pos'][1])
		node_dist = round(node_dist,1)
		node_dist = (j,node_dist)
		distance.setdefault(i, [])
		distance[i].append(node_dist)
		distance[i].sort(key=lambda tup: tup[1])
		if j == len(G)-1:
			print "**************************************"	
			print "REVISANDO NODO " + str(i)
			for k in range(0, len(distance[i])): 
				print " con nodo "+str(distance[i][k][0])+ " y peso "+str(distance[i][k][1])
				if i != k:
					peso = distance[i][k][1]
					if peso > 0 and peso <= power_level[0]:
						add_graphical_edge(G,i,distance[i][k][0],power_level[0])					
					if peso > power_level[0] and peso <= power_level[1]:	
						add_graphical_edge(G,i,distance[i][k][0],power_level[1])
					if peso > power_level[1] and peso <= power_level[2]:	
						add_graphical_edge(G,i,distance[i][k][0],power_level[2])	
					if peso > power_level[2] and peso <= power_level[3]:
						add_graphical_edge(G,i,distance[i][k][0],power_level[3])																	
	print distance[i]
	distance = {}		

result = non_neighbors_nodes(G, 5)
calculate_matrix(result[0], result[1])
position = nx.get_node_attributes(G, 'pos')
plt.gca().invert_yaxis()
nx.draw_networkx_labels(G, position, labels=None)
plt.draw()
plt.savefig("iot.png")
# Asignando grafo al que sera el nuevo arbol

H = nx.DiGraph()

# def check_parent(H, child, root):
# 	if H.predecessors(child):
# 		root
# 	# print parent
# 	return parent


def find_root(G, node, root_path):
	if list(G.predecessors(node)) != []:  # True if there is a predecessor, False otherwise
		# print list(G.predecessors(node))
		root_path += 1
		(root, root_path) = find_root(G, list(G.predecessors(node))[0], root_path )
	else:
		root = node
		root_path = root_path
	return root, root_path

def scheduling(H, root, bfs, n_ch):
	sche = {}
	for i in range(n_ch):
		sche[i] = []
	level = 0
	print bfs
	print len(bfs)
	for item in bfs:
		level = 0
		if int(item[0]) == int(root):
			print item[0]
			print item
			sche[0].append(item)
			# bfs.remove(item)
			level = 0
		else:
			root_path = 0
			level = find_root(H, item[0], root_path)
			current_level = level[1]%n_ch
			if current_level == 0:
				current_level = n_ch
			print "CURRENT LEVEL" + str(current_level)
			timeslot = len(sche[current_level])
			print "TIMESLOT " + str(timeslot)
			can_push = False
			print sche
			# for ch in sche:
			# 	print ch
			if sche[current_level] == []:
				can_push = True
				# 	continue
			if sche[current_level] != []:
				if not (item[0] in sche[timeslot] or item[1] in sche[timeslot]):
					can_push = True
			if can_push:
				print "ITEEEM"
				print item
				sche[current_level].append(item)
			# level = check_parent(H, bfs[i][0], root)
			print level
		# else:
		# 	ch
		
	for i in range(len(sche)):
		print sche[i]
	# print sche




def create_tree(H,G,root):
	print "CREANDO ARBOL"
	print sorted(G[root])
	H.add_node(root)
	first_iteration = True
	compare_list = [root]
	edges = tr.bfs_edges(G, root)
	item = [root] + [v for u, v in edges]
	while len(H.nodes()) < len(item):
		if first_iteration:
			print "In first level"
			for key, value in sorted(G[root].iteritems(), key=lambda (k, v): (v, k)):
				H.add_node(key)
				H.add_edge(root,key)
				compare_list.append(key)
				print "%s: %s" % (key, value)
			print len(compare_list)
			first_iteration = False
		else:
			print "In other level"
			print len(compare_list)
			for i in range(0,len(compare_list)):
				print G[i]
				for child_key, child_value in sorted(G[compare_list[i]].iteritems(), key=lambda (k, v): (v, k)):
					if child_key not in compare_list:
						H.add_node(child_key)
						H.add_edge(compare_list[i], child_key)
						compare_list.append(child_key)
						print "%s: %s" % (child_key, child_value)
		# count += 1
	edges = tr.bfs_edges(H, root)
	item = [root] + [v for u, v in edges]
	print "BFS"
	bfs = list(nx.bfs_edges(H, root))
	print(bfs)
	# print item 
	print "DFS"
	T = nx.dfs_tree(H, root)
	print(T.edges())
	print tree.is_tree(H)
	print "Terminando arbol"
	scheduling(H,root,bfs,4)

create_tree(H,G,5)

plt.show()

# nx.write_dot(H, 'test.dot')
# plt.title('draw_networkx')
# pos = nx.graphviz_layout(H, prog='dot')
# nx.draw(H, pos, with_labels=False, arrows=False)
# plt.savefig('nx_test.png')
pos = hierarchy_pos(H, 5)
nx.draw(H, pos=pos, with_labels=True)
# nx.draw(H, pos=graphviz_layout(H), node_size=1600, cmap=plt.cm.Blues,
#         node_color=range(len(H)),
#         prog='dot')
plt.show()
