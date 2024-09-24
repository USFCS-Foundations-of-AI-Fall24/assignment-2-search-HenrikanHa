from collections import deque


## We will append tuples (state, "action") in the search queue
def breadth_first_search(startState, action_list, goal_test, use_closed_list=True):
    search_queue = deque()
    closed_list = {}
    state_generated = 0

    search_queue.append((startState, ""))
    state_generated += 1
    if use_closed_list:
        closed_list[startState] = True
    while len(search_queue) > 0:
        ## this is a (state, "action") tuple
        next_state = search_queue.popleft()
        if goal_test(next_state[0]):
            print("Goal found")
            print(next_state)
            ptr = next_state[0]
            while ptr is not None:
                ptr = ptr.prev
                print(ptr)
            print(f"Total states generated: {state_generated}")

            return next_state
        else:
            successors = next_state[0].successors(action_list)
            state_generated += len(successors)
            if use_closed_list:
                successors = [item for item in successors
                              if item[0] not in closed_list]
                for s in successors:
                    closed_list[s[0]] = True
            search_queue.extend(successors)

    print(f"Total states generated: {state_generated}")


### Note the similarity to BFS - the only difference is the search queue

## use the limit parameter to implement depth-limited search
def depth_first_search(startState, action_list, goal_test, use_closed_list=True, limit=float('inf')):
    search_queue = deque()
    closed_list = {}
    state_generated = 0

    search_queue.append((startState, "", 0))
    state_generated += 1
    if use_closed_list:
        closed_list[startState] = True
    while len(search_queue) > 0:
        ## this is a (state, "action") tuple
        next_state = search_queue.pop()
        if goal_test(next_state[0]):
            print("Goal found")
            print(next_state)
            ptr = next_state[0]
            while ptr is not None:
                ptr = ptr.prev
                print(ptr)
            print(f"Total states generated: {state_generated}")

            return next_state

        if next_state[2] <= limit:
            successors = next_state[0].successors(action_list)
            state_generated += len(successors)
            if use_closed_list:
                successors = [item for item in successors
                              if item[0] not in closed_list]
                for s in successors:
                    closed_list[s[0]] = True
            search_queue.extend([(s[0], s[1], next_state[2] + 1) for s in successors])

    print(f"Total states generated: {state_generated}")