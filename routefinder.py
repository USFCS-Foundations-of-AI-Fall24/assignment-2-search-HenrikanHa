## Thanh Cong Nguyen
from queue import PriorityQueue
from Graph import Graph, Node, Edge
import math

class map_state():
    ## f = total estimated cost
    ## g = cost so far
    ## h = estimated cost to goal
    def __init__(self, location="", mars_graph=None,
                 prev_state=None, g=0, h=0):
        self.location = location
        self.mars_graph = mars_graph
        self.prev_state = prev_state
        self.g = g
        self.h = h
        self.f = self.g + self.h

    def __eq__(self, other):
        return self.location == other.location

    def __hash__(self):
        return hash(self.location)

    def __repr__(self):
        return "(%s)" % (self.location)

    def __lt__(self, other):
        return self.f < other.f

    def __le__(self, other):
        return self.f <= other.f

    def is_goal(self):
        return self.location == '1,1'


def a_star(start_state, heuristic_fn, goal_test, use_closed_list=True):
    search_queue = PriorityQueue()
    closed_list = {}
    state_generated = 0
    search_queue.put(start_state)
    start_state.h = heuristic_fn(start_state)
    start_state.f = start_state.g + start_state.h
    ## you do the rest.
    print(f"Enqueue: {start_state.location} (f={start_state.g}+{start_state.h}={start_state.f})")
    state_generated += 1

    while not search_queue.empty():
        current_state = search_queue.get()

        if use_closed_list:
            if current_state in closed_list and closed_list[current_state] is True:
                print(f"Skipping: {current_state.location} (f={current_state.f})")
                continue
            closed_list[current_state] = True
        print(f"Dequeue: {current_state.location} (f={current_state.f})")

        if goal_test(current_state):
            print("Goal found")
            print(current_state)
            ptr = current_state
            while ptr is not None:
                ptr = ptr.prev_state
                print(ptr)
            print(f"Total states generated: {state_generated}")
            return current_state

        current_node = Node(current_state.location)
        edges = current_state.mars_graph.get_edges(current_node)
        if edges:
            for edge in edges:
                neighbor_state = map_state(edge.dest.value, current_state.mars_graph, current_state,
                                           current_state.g + edge.val)
                neighbor_state.h = heuristic_fn(neighbor_state)
                neighbor_state.f = neighbor_state.g + neighbor_state.h
                state_generated += 1
                # if use close list, only add into queue when it is not in the close list
                if use_closed_list:
                    if neighbor_state in closed_list and closed_list[neighbor_state] is True:
                        continue
                    # has not fully explored, can be or not be in the queue
                    if neighbor_state in closed_list and closed_list[neighbor_state] is False:
                        search_queue.put(neighbor_state)
                        print(f"Enqueue: {neighbor_state.location} (f={neighbor_state.g}+{neighbor_state.h}={neighbor_state.f})")
                    if neighbor_state not in closed_list:
                        closed_list[neighbor_state] = False
                        search_queue.put(neighbor_state)
                        print(f"Enqueue: {neighbor_state.location} (f={neighbor_state.g}+{neighbor_state.h}={neighbor_state.f})")
                else:
                    search_queue.put(neighbor_state)
                    print(f"Enqueue: {neighbor_state.location} (f={neighbor_state.g}+{neighbor_state.h}={neighbor_state.f})")
    print('There is no path to goal')


## default heuristic - we can use this to implement uniform cost search
def h1(state):
    return 0

## you do this - return the straight-line distance between the state and (1,1)
def sld(state):
    x, y = map(int, state.location.strip().split(','))
    return math.sqrt((x - 1) ** 2 + (y - 1) ** 2)


## you implement this. Open the file filename, read in each line,
## construct a Graph object and assign it to self.mars_graph().
def read_mars_graph(filename):
    mars_graph = Graph()
    with open(filename, 'r') as f:
        lines = f.readlines()
        for l in lines:
            l = l.strip()
            start, neighbors = l.split(':')
            neighbors_string = neighbors.strip().split(' ')
            start_node = Node(start.strip())
            mars_graph.add_node(start_node)
            # create edge to add into graph
            for neighbor in neighbors_string:
                neighbor_node = Node(neighbor.strip())
                mars_graph.add_edge(Edge(start_node, neighbor_node, 1))
    return mars_graph

def main():
    # Run USC algorithm
    start_state = map_state("8,8")
    start_state.mars_graph = read_mars_graph("MarsMap.txt")
    a_star(start_state, h1, map_state.is_goal)
    # Run A* algorithm
    start_state = map_state("8,8")
    start_state.mars_graph = read_mars_graph("MarsMap.txt")
    a_star(start_state, sld, map_state.is_goal)

if __name__ == "__main__":
    main()