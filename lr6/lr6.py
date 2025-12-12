from collections import defaultdict, deque

def mark_method(graph, start, end, parent):
    visited = set()
    queue = deque([start])
    visited.add(start)
    parent[start] = None

    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if v not in visited:
                visited.add(v)
                parent[v] = u
                if v == end:
                    return True
                queue.append(v)
    return False


def find_max(V1, V2, edges):
    graph = defaultdict(list)

    for u, v in edges:
        graph[u].append(v)

    s = 's'
    t = 't'

    for u in V1:
        graph[s].append(u)

    for v in V2:
        graph[v].append(t)

    while True:
        parent = {}
        if not mark_method(graph, s, t, parent):
            break

        path = []
        current = t
        while current != s:
            path.append(current)
            current = parent[current]
        path.append(s)
        path.reverse()

        if path[1] in graph[s]:
            graph[s].remove(path[1])
        if t in graph[path[-2]]:
            graph[path[-2]].remove(t)

        for i in range(1, len(path)-2):
            u, v = path[i], path[i+1]
            if v in graph[u]:
                graph[u].remove(v)
            graph[v].append(u)

    M = []
    for v in V2:
        for u in graph.get(v, []):
            if u in V1:
                M.append((u, v))

    return M, graph


if __name__ == "__main__":
    V1 = ['a', 'b', 'c']
    V2 = ['x', 'y', 'z']
    transitions = [('a', 'x'),('b', 'x'),('c', 'x'),('b', 'y'),('c', 'y'), ('c', 'z')]
    # V1 = ['u1', 'u2', 'u3', 'u4', 'u5']
    # V2 = ['v1', 'v2', 'v3', 'v4', 'v5']
    # transitions = [('u1', 'v2'),('u1', 'v3'),('u3', 'v1'),('u3', 'v4'),('u4', 'v5')]
    # V1 = ['u1', 'u2', 'u3', 'u4', 'u5']
    # V2 = ['v1', 'v2', 'v3', 'v4', 'v5']
    # transitions = [('u1', 'v2'),('u1', 'v3'),('u2', 'v5'), ('u1', 'v3'),('u3', 'v1'),('u3', 'v4'),('u4', 'v4'),('u4', 'v5'),('u5', 'v2')]

    M, graph = find_max(V1, V2, transitions)
    print("Максимальное паросочетание:", M)
    print("Размер паросочетания:", len(M))
