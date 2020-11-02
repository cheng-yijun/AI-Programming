import os
import sys

lists = []  # the global variable to store states


def swap(swap_list, i, j):
    """ This is a helper function that can swap two element in a list
        according to the given indices.
    """
    new_list = swap_list.copy()  # copy the content of the original list
    temp = new_list[i];  # store an element into a temporary variable
    new_list[i] = new_list[j]  # assign value in index j to index i
    new_list[j] = temp  # assign value from i to j
    return new_list


def calc_h(succ):
    """ This is a helper function to calculate the h for given states
    """
    h = 0  # initialize a value h to 0
    for i in range(1, 9):  # find the number of wrong tile position
        if succ[i - 1] != i:
            h = h + 1  # increase h if find the wrong position of tiles
    return h


def print_succ(state):
    """this function can find all of the successor state of given state and print it out
    """
    global lists  # global lists to store the four successor states
    lists = []  # initialize the global lists to empty
    # make four copy of the original states
    succ1 = state.copy()
    succ2 = state.copy()
    succ3 = state.copy()
    succ4 = state.copy()

    # nine situation for 0 to put
    # each situation has 4 successors
    # swap to get the 4 successors
    if state[0] == 0:
        succ1 = swap(succ1, 0, 1)
        succ2 = swap(succ2, 0, 2)
        succ3 = swap(succ3, 0, 3)
        succ4 = swap(succ4, 0, 6)
    if state[1] == 0:
        succ1 = swap(succ1, 1, 0)
        succ2 = swap(succ2, 1, 2)
        succ3 = swap(succ3, 1, 4)
        succ4 = swap(succ4, 1, 7)
    if state[2] == 0:
        succ1 = swap(succ1, 2, 1)
        succ2 = swap(succ2, 2, 5)
        succ3 = swap(succ3, 2, 0)
        succ4 = swap(succ4, 2, 8)
    if state[3] == 0:
        succ1 = swap(succ1, 3, 0)
        succ2 = swap(succ2, 3, 4)
        succ3 = swap(succ3, 3, 5)
        succ4 = swap(succ4, 3, 6)
    if state[4] == 0:
        succ1 = swap(succ1, 4, 1)
        succ2 = swap(succ2, 4, 3)
        succ3 = swap(succ3, 4, 5)
        succ4 = swap(succ4, 4, 7)
    if state[5] == 0:
        succ1 = swap(succ1, 5, 3)
        succ2 = swap(succ2, 5, 4)
        succ3 = swap(succ3, 5, 2)
        succ4 = swap(succ4, 5, 8)
    if state[6] == 0:
        succ1 = swap(succ1, 6, 3)
        succ2 = swap(succ2, 6, 7)
        succ3 = swap(succ3, 6, 0)
        succ4 = swap(succ4, 6, 8)
    if state[7] == 0:
        succ1 = swap(succ1, 7, 1)
        succ2 = swap(succ2, 7, 4)
        succ3 = swap(succ3, 7, 6)
        succ4 = swap(succ4, 7, 8)
    if state[8] == 0:
        succ1 = swap(succ1, 8, 5)
        succ2 = swap(succ2, 8, 7)
        succ3 = swap(succ3, 8, 2)
        succ4 = swap(succ4, 8, 6)

    # get the sorted list of successors
    lists = sorted([succ1, succ2, succ3, succ4])
    # get each of the sorted successor
    succ1 = lists[0]
    succ2 = lists[1]
    succ3 = lists[2]
    succ4 = lists[3]
    h1 = h2 = h3 = h4 = 0  # initialize the heuristic
    # calculate the heuristic for each successor
    for i in range(1, 9):
        if succ1[i - 1] != i:
            h1 = h1 + 1
        if succ2[i - 1] != i:
            h2 = h2 + 1
        if succ3[i - 1] != i:
            h3 = h3 + 1
        if succ4[i - 1] != i:
            h4 = h4 + 1

    # print the four successors
    print(succ1, 'h=' + str(h1))
    print(succ2, 'h=' + str(h2))
    print(succ3, 'h=' + str(h3))
    print(succ4, 'h=' + str(h4))


''' author: hobbes
    source: cs540 canvas
    
'''


class PriorityQueue(object):

    def __init__(self):
        self.queue = []
        self.max_len = 0

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    def is_empty(self):
        return len(self.queue) == 0

    def enqueue(self, state_dict):
        """ Items in the priority queue are dictionaries:
             -  'state': the current state of the puzzle
             -      'h': the heuristic value for this state
             - 'parent': a reference to the item containing the parent state
             -      'g': the number of moves to get from the initial state to
                         this state, the "cost" of this state
             -      'f': the total estimated cost of this state, g(n)+h(n)

            For example, an item in the queue might look like this:
             {'state':[1,2,3,4,5,6,7,8,0], 'parent':[1,2,3,4,5,6,7,0,8],
              'h':0, 'g':14, 'f':14}

            Please be careful to use these keys exactly so we can test your
            queue, and so that the pop() method will work correctly.



        """

        in_open = False  # check if the dictionary is already in the queue
        index = 0  # initialize an index to find the dictionary
        for i in range(0, len(self.queue)):
            if self.queue[i]['state'] == state_dict['state']:
                in_open = True  # find the dictionary
                index = i  # record thei index
                break

        # find the dictionary and need to replace
        if in_open and state_dict['g'] < self.queue[index]['g']:
            self.queue[index] = state_dict

        # does not find the dictionary in the queue, add it to queue directly
        if not in_open:
            self.queue.append(state_dict)

        # track the maximum queue length
        if len(self.queue) > self.max_len:
            self.max_len = len(self.queue)

    def requeue(self, from_closed):
        """ Re-queue a dictionary from the closed list (see lecture slide 21)
        """
        self.queue.append(from_closed)

        # track the maximum queue length
        if len(self.queue) > self.max_len:
            self.max_len = len(self.queue)

    def pop(self):
        """ Remove and return the dictionary with the smallest f(n)=g(n)+h(n)
        """
        minf = 0
        for i in range(1, len(self.queue)):
            if self.queue[i]['f'] < self.queue[minf]['f']:
                minf = i
        state = self.queue[minf]
        del self.queue[minf]
        return state


def blockPrint():
    sys.stdout = open(os.devnull, 'w')


# Restore
def enablePrint():
    sys.stdout = sys.__stdout__


def solve(state):
    """ This function can find the shortest path to solve the torus problem
    """
    global lists  # empty the list variable for new storing
    lists = []
    cur_state = state.copy()  # get the copy of the original state
    h = calc_h(cur_state)  # compute the heuristic
    # create two priority queue open and close
    opened = PriorityQueue()
    closed = PriorityQueue()
    # enqueue the original state
    opened.enqueue({'state': state, 'h': h, 'g': 0, 'parent': None, 'f': 0 + h})
    goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]  # the goal state
    find_goal = False  # check if it is the goal
    while not opened.is_empty():  # loop the queue to find the path
        # pop the state to close
        cur_dict = opened.pop()
        closed.enqueue(cur_dict)
        # if the pooped state is the goal, finish loop
        if cur_dict['state'] == goal:
            # print(goal, 'h=0 moves: ', cur_dict['g'])
            find_goal = True
            break
        # get the successors of pooped state without printing anything
        blockPrint()
        print_succ(cur_dict['state'])
        succs = lists  # get the four successors
        enablePrint()  # allow print now
        for cur_state in succs:  # for each successor state
            g = cur_dict['g'] + 1  # update the g value
            if_close = False
            for closed_dict in closed.queue:  # check if this state is in close
                if cur_state == closed_dict['state']:
                    if_close = True  # find the state in close queue
                    break
            if if_close and closed_dict['g'] < g:  # in close but do not need to requeue it
                continue  # skip this loop
            # compute the keys of the state
            h = calc_h(cur_state)
            f = g + h
            parent = cur_dict['state']
            # need to requeue this state
            if if_close and closed_dict['g'] > g:
                opened.requeue({'state': cur_state, 'h': h, 'g': g, 'parent': parent, 'f': f})
                # closed.queue.remove(closed_dict)
                continue
            # add this state into the queue
            opened.enqueue({'state': cur_state, 'h': h, 'g': g, 'parent': parent, 'f': f})

    # print the steps from s0 to goal
    if find_goal:
        result = []
        for ds in closed.queue:  # loop to find the goal dictionary in closed
            if ds['state'] == goal:
                goal_dict = ds  # fing the goal in closed
                break
        result.append(goal_dict)  # add the goal to list
        path_parent = goal_dict['parent']  # record the parent state
        while path_parent is not None:  # loop to find the parent dictionary back to origin
            for ds in closed.queue:
                if ds['state'] == path_parent:
                    result.append(ds)
                    path_parent = ds['parent']
                    break

        for i in range(len(result)):  # print the path
            index = len(result) - i - 1
            print(result[index]['state'], ' h=' + str(result[index]['h']), ' moves: ' + str(result[index]['g']))
    # print the max queue length
    print('Max queue length:', opened.max_len)

