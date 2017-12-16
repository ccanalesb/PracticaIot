from networkx.algorithms import traversal as tr
from networkx.algorithms import tree as tree

def generate_tree(H, G, root):
	print "CREANDO ARBOL"
	# print sorted(G[root])
	H.add_node(root)
	first_iteration = True
	compare_list = [root]
	edges = tr.bfs_edges(G, root)
	item = [root] + [v for u, v in edges]
	while len(H.nodes()) < len(item):
		if first_iteration:
			# print "In first level"
			for key, value in sorted(G[root].iteritems(), key=lambda (k, v): (v, k)):
				H.add_node(key)
				H.add_edge(root, key)
				compare_list.append(key)
				print "%s: %s" % (key, value)
			# print len(compare_list)
			first_iteration = False
		else:
			# print "In other level"
			# print len(compare_list)
			for i in range(0, len(compare_list)):
				# print G[i]
				for child_key, child_value in sorted(G[compare_list[i]].iteritems(), key=lambda (k, v): (v, k)):
					if child_key not in compare_list:
						H.add_node(child_key)
						H.add_edge(compare_list[i], child_key)
						compare_list.append(child_key)
						# print "%s: %s" % (child_key, child_value)
		# count += 1
	edges = tr.bfs_edges(H, root)
	item = [root] + [v for u, v in edges]

	# print item
	# print "DFS"
	# T = nx.dfs_tree(H, root)
	# print(T.edges())
	# print tree.is_tree(H)
	print "Terminando arbol"
	
