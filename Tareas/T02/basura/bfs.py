graph = {
        '1': ['2', '3', '4'],
        '2': ['5', '6'],
        '5': ['9', '10'],
        '4': ['7', '8'],
        '7': ['11', '12']
        }


def bfs(graph, start, end):
    # maintain a queue of paths
    queue = []
    # push the first path into the queue
    queue.append([start])
    while queue:
        # get the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        # path found
        if node == end:
            return path
        # enumerate all adjacent nodes, construct a new path and push it into the queue
        print(graph.get(node, []))
        for adjacent in graph.get(node, []):
            new_path = list(path)
            print('npath', new_path)
            new_path.append(adjacent)
            print('npath+adj', new_path)
            queue.append(new_path)
            print('queue', queue)

print(bfs(graph, '1', '11'))
