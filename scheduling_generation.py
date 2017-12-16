def find_root(G, node, root_path):
	if list(G.predecessors(node)) != []:  # True if there is a predecessor, False otherwise
		# print list(G.predecessors(node))
		root_path += 1
		(root, root_path) = find_root(G, list(G.predecessors(node))[0], root_path)
	else:
		root = node
		root_path = root_path
	return root, root_path


def scheduling(H, root, bfs, n_ch):
	pending = []
	sche = {}
	for i in range(n_ch):
		sche[i] = []
	level = 0
	for item in bfs:
		level = 0
		if int(item[0]) == int(root):
			sche[0].append(item)
			level = 0
		else:
			root_path = 0
			level = find_root(H, item[0], root_path)
			current_level = level[1] % n_ch
			if current_level == 0:
				current_level = n_ch
			timeslot = len(sche[current_level])
			can_push = False
			timeslot_2, can_push = can_push_sche(sche, timeslot, item, n_ch)
			if can_push:
				while len(sche[current_level]) < timeslot_2:
					sche[current_level].append((None, None))
				sche[current_level].append(item)
			else:
				pending.append(item)
			# level = check_parent(H, bfs[i][0], root)
	print "MATRIZ"
	for i in range(len(sche)):
		print sche[i]
	print "PENDIENTES"
	print pending
	# max = 0
	# for i in range(len(sche)):
	# 	if len(sche[i]) > max:
	# 		max = len(sche[i])
	# for i in range(len(sche)):
	# 	if len(sche[i]) < max:
	# 		for i in range(abs(len(sche[i])-max)):
	# 			sche[i].append((None,None))
	# import pandas
	# df = pandas.DataFrame(sche)
	# print df


def can_push_sche(scheduling, timeslot, item, n_ch):
	can_save = True
	for i in range(0, n_ch):
		channel = scheduling[i]
		if timeslot < len(channel):
			if item[0] in channel[timeslot] or item[1] in channel[timeslot]:
				timeslot = timeslot + 1
				can_push_sche(scheduling, timeslot, item, n_ch)
	return timeslot, can_save

# Permite encontrar nodos no vecinos
def non_neighbors_nodes(G, root):
	edges = tr.bfs_edges(G, root)
	item = [root] + [v for u, v in edges]
	result = {}
	print item
	for i in item:
		print "nodo ", i, " = ", list(nx.non_neighbors(G, i))
		result[i] = list(nx.non_neighbors(G, i))
	return (item, result)
