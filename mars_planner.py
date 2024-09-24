## Thanh Cong Nguyen
## actions:
## pick up tool
## move_to_sample
## use_tool
## move_to_station
## drop_tool
## drop_sample
## move_to_battery
## charge

## locations: battery, sample, station
## holding_sample can be True or False
## holding_tool can be True or False
## Charged can be True or False

from copy import deepcopy
from search_algorithms import breadth_first_search, depth_first_search

class RoverState :
    def __init__(self, loc="station", sample_extracted=False, holding_sample=False, holding_tool=False, sample_picked_up=False, charged=False):
        self.loc = loc
        self.sample_extracted = sample_extracted
        self.holding_sample = holding_sample
        self.holding_tool = holding_tool
        self.sample_picked_up = sample_picked_up
        self.charged = charged
        self.prev = None

    ## you do this.
    def __eq__(self, other):
        return (self.loc == other.loc and
               self.sample_extracted == other.sample_extracted and
               self.holding_sample == other.holding_sample and
               self.holding_tool == other.holding_tool and
               self.sample_picked_up == other.sample_picked_up and
               self.charged == other.charged)


    def __repr__(self):
        return (f"Location: {self.loc}, " +
                f"Sample Extracted?: {self.sample_extracted}, "+
                f"Holding Tool?: {self.holding_tool}, " +
                f"Holding Sample?: {self.holding_sample}, " +
                f"Sample Picked Up?: {self.sample_picked_up}, " +
                f"Charged? {self.charged}")

    def __hash__(self):
        return self.__repr__().__hash__()

    def successors(self, list_of_actions):

        ## apply each function in the list of actions to the current state to get
        ## a new state.
        ## add the name of the function also
        succ = [(item(self), item.__name__) for item in list_of_actions]
        ## remove actions that have no effect

        succ = [item for item in succ if not item[0] == self]
        return succ

## our actions will be functions that return a new state.

def move_to_sample(state) :
    r2 = deepcopy(state)
    r2.loc = "sample"
    r2.prev=state
    return r2

def move_to_station(state) :
    r2 = deepcopy(state)
    r2.loc = "station"
    r2.prev = state
    return r2

def move_to_battery(state) :
    r2 = deepcopy(state)
    r2.loc = "battery"
    r2.prev = state
    return r2
# add tool functions here

def pick_up_tool(state) :
    r2 = deepcopy(state)
    if not state.sample_extracted and state.loc == "station":
        r2.holding_tool = True
    r2.prev = state
    return r2

def drop_tool(state) :
    r2 = deepcopy(state)
    if state.sample_extracted and state.loc == "station":
        r2.holding_tool = False
    r2.prev = state
    return r2

def use_tool(state):
    r2 = deepcopy(state)
    if state.holding_tool and state.loc == "sample":
        r2.sample_extracted = True
    r2.prev = state
    return r2

def pick_up_sample(state) :
    r2 = deepcopy(state)
    if state.sample_extracted and state.loc == "sample" and state.holding_tool:
        r2.holding_sample = True
        r2.sample_picked_up = True
    r2.prev = state
    return r2

def drop_sample(state) :
    r2 = deepcopy(state)
    if state.sample_extracted and state.loc == "station" and state.holding_sample:
        r2.holding_sample = False
    r2.prev = state
    return r2

def charge(state) :
    r2 = deepcopy(state)
    if state.sample_extracted and state.loc == "battery" and state.sample_picked_up:
        r2.charged = True
    r2.prev = state
    return r2

action_list = [charge, drop_sample, pick_up_sample,
               pick_up_tool, drop_tool, use_tool,
               move_to_sample, move_to_battery, move_to_station]

def battery_goal(state) :
    return state.loc == "battery"
## add your goals here.

def move_to_sample(state) :
    return (state.loc == "sample"
            and state.holding_tool == True
            and state.holding_sample == False
            and state.sample_extracted == False
            and state.sample_picked_up == False
            and state.charged == False)

def remove_sample(state) :
    return (state.loc == "sample"
            and state.holding_tool == True
            and state.holding_sample == True
            and state.sample_extracted == True
            and state.sample_picked_up == True
            and state.charged == False)

def mission_complete(state) :
    return (battery_goal(state)
            and state.charged == True
            and state.holding_sample == False
            and state.holding_tool == False
            and state.sample_extracted == True
            and state.sample_picked_up == True)

def main():
    print("Part 3 and part 4")
    print("Breadth first search")
    s = RoverState(sample_extracted=True)
    result = breadth_first_search(s, action_list, mission_complete)
    print(result)
    print("\n")

    print("Depth first search")
    s = RoverState(sample_extracted=True)
    result = depth_first_search(s, action_list, mission_complete)
    print(result)
    print("\n")

    print("Depth first search limit=10")
    s = RoverState(sample_extracted=True)
    result = depth_first_search(s, action_list, mission_complete, 10)
    print(result)

    print("Part 5")
    print("Breadth first search")
    s = RoverState()
    result = breadth_first_search(s, action_list, mission_complete)
    print(result)
    print("\n")

    print("Depth first search")
    s = RoverState()
    result = depth_first_search(s, action_list, mission_complete)
    print(result)
    print("\n")

    print("Depth limited search limit=10")
    s = RoverState()
    result = depth_first_search(s, action_list, mission_complete, 10)
    print(result)

    print("Part 6")
    print("Breadth first search")
    s = RoverState()
    result_1 = breadth_first_search(s, action_list, move_to_sample)
    result_2 = breadth_first_search(result_1[0], action_list, remove_sample)
    result_3 = breadth_first_search(result_2[0], action_list, mission_complete)

    print("Depth first search")
    s1 = RoverState()
    result_1 = depth_first_search(s1, action_list, move_to_sample)
    result_2 = depth_first_search(result_1[0], action_list, remove_sample)
    result_3 = depth_first_search(result_2[0], action_list, mission_complete)

    print("Depth limit search limit=10")
    s2 = RoverState()
    result_1 = depth_first_search(s2, action_list, move_to_sample, 10)
    result_2 = depth_first_search(result_1[0], action_list, remove_sample, 10)
    result_3 = depth_first_search(result_2[0], action_list, mission_complete, 10)


if __name__=="__main__" :
    main()