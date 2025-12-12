from collections import deque
import sys

def mark_method(graph_Gf, start, end, parent):
    visited = set()
    queue = deque([start])
    visited.add(start)
    parent[start] = None

    while queue:
        u = queue.popleft()
        for v, capacity in graph_Gf[u].items():
            if v not in visited and capacity > 0:
                visited.add(v)
                parent[v] = u
                if v == end:
                    return True
                queue.append(v)
    return False

def ford_falkerson(graph, start, end):
    graph_Gf = {u: {} for u in graph}
    flow = {u: {} for u in graph}

    for u in graph:
        for v, cap in graph[u].items():
            graph_Gf[u][v] = cap
            if v not in graph_Gf:
                graph_Gf[v] = {}
            graph_Gf[v].setdefault(u, 0)
            flow[u][v] = 0

    parent = {}
    max_flow = 0

    while mark_method(graph_Gf, start, end, parent):
        path_flow = float('Inf')
        s = end
        while s != start:
            path_flow = min(path_flow, graph_Gf[parent[s]][s])
            s = parent[s]

        max_flow += path_flow
        v = end
        while v != start:
            u = parent[v]

            graph_Gf[u][v] -= path_flow
            graph_Gf[v][u] += path_flow

            if v in graph and u in graph[v] and graph[v][u] > 0:
                flow[v][u] = max(0, flow[v][u] - path_flow)
            else:
                flow[u][v] = flow[u].get(v, 0) + path_flow

            v = u

    return max_flow, flow

def main():
    if len(sys.argv) != 2:
        print("Использование: python lr5.py <input_file>")
        return

    input_file = sys.argv[1]
    graph = {}
    start = end = None

    with open(input_file, 'r') as f:
        start = f.readline().strip()
        end = f.readline().strip()
        for line in f:
            parts = line.strip().split()
            if len(parts) == 3:
                u, v, cap = parts
                cap = int(cap)
                if u not in graph:
                    graph[u] = {}
                graph[u][v] = cap

    max_flow, flows = ford_falkerson(graph, start, end)

    print(f"Максимальный поток: {max_flow}")
    print("Потоки по дугам (поток/пропускная_способность):")

    with open(input_file, 'r') as f:
        f.readline()
        f.readline()
        for line in f:
            parts = line.strip().split()
            if len(parts) == 3:
                u, v, cap = parts
                cap = int(cap)
                current_flow = flows[u].get(v, 0)
                print(f"{u} -> {v}: {current_flow}/{cap}")

if __name__ == "__main__":
    main()
