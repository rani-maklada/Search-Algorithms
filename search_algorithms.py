from copy import deepcopy

import time

class search_algorithms:
    visited_states = None
    active_states = None
    ID_MAX_DEPTH = 20

    def __init__(self):
        self.visited_states = {}
        self.active_states = {}

    def pop_state(self, state, with_heuristic):
        next_states = self.successor_funcion(state['content'])
        # Calculate states details -> 1) key state 2) score state 3) parent state key 
        return self.calc_state_details(next_states, self.state_to_key(state['content']), \
        state['depth'] + 1, with_heuristic)


    def successor_funcion(self, state):
        # for 3X3 - 12 next states
        # for 4X4 - 18 next states
        next_states = []
        for i in range(len(state) - 1):
            for j in range(len(state[0])):
                new_state = deepcopy(state) # Copy array
                temp = new_state[i][j]
                new_state[i][j] = new_state[i+1][j]
                new_state[i+1][j] = temp

                next_states.append(new_state)

        for i in range(len(state)):
            for j in range(len(state[0])-1):
                new_state = deepcopy(state) # Copy array
                temp = new_state[i][j]
                new_state[i][j] = new_state[i][j+1]
                new_state[i][j+1] = temp

                next_states.append(new_state)

        return next_states
    
    def calc_heurestic(self, state):
        dic_3 = {1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1],9:[2,2]}
        dic_4 = {1:[0,0], 2:[0,1], 3:[0,2], 4:[0,3], 5:[1,0], 6:[1,1], 7:[1,2], 8:[1,3],9:[2,0], 10:[2,1], 11: [2,2],12:[2,3], 13:[3,0], 14:[3,1], 15:[3,2], 16:[3,3]}

        dic = dic_3 if len(state) == 3 else dic_4

        score = 0
        for i in range(len(state)):
            for j in range(len(state[0])):
                [x,y] = dic[state[i][j]]
                score += (abs(i - x) + abs(j-y))
        return (score / 2)

    def isGoal(self, state):
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] != (j + 1) + (i * len(state)):
                    return False
        return True   

    def get_next_state_key(self, active_states, callback_fun):
        return callback_fun(active_states, key = lambda key: active_states[key]['score'])

    def merge_states(self, states1, states2):
        for key in states2:
            if key in states1:
                if states1[key]['score'] > states2[key]['score']:
                    states1[key]['score'] = states2[key]['score']
            else:
                states1[key] = states2[key]
        return states1

    def state_to_key(self, state):
        a = 1
        sum = 0
        for i in range(len(state)):
            for j in range(len(state[0])):
                sum = sum + state[i][j] * a
                a = a * 10
        return sum

        

    def get_full_path(self, state, visited_states):
        path = []
        while state != None:
            path.insert(0, state['content'])
            state = visited_states[state['parent_state']] if state['parent_state'] else None

        return path        

    def calc_state_details(self, states, parent_key, depth, withHeurestic):
        states_scores = {}
        for i in range(len(states)):
            states_scores[self.state_to_key(states[i])] = {'content': states[i], \
                'score': depth + (self.calc_heurestic(states[i]) if withHeurestic else 0),\
                'depth': depth, 'parent_state': parent_key}
        return states_scores
    
    def insert_popped_states(self, popped_states, visited_states, active_states):
        popped_states_to_del = []
        for key in popped_states:
            if key in visited_states:
                if popped_states[key]['score'] > visited_states[key]['score']:
                    popped_states_to_del.append(key)
                else:
                    del visited_states[key]

            elif key in active_states:
                if popped_states[key]['score'] > active_states[key]['score']:
                    popped_states_to_del.append(key)
                else:
                    del active_states[key]

        for state_key in popped_states_to_del:
            del popped_states[state_key]
        
        active_states.update(popped_states)


        return [active_states, visited_states]        


    def remove_states(self, popped_states, visited_states):
        popped_states_to_del = []
        visited_states_to_del = []
        for key in popped_states:
            if key in visited_states:
                if popped_states[key]['score'] < visited_states[key]['score']:
                    visited_states_to_del.append(key)
                else:
                    popped_states_to_del.append(key)
        
        for state_key in visited_states_to_del:
            del visited_states[state_key]

        for state_key in popped_states_to_del:
            del popped_states[state_key]

        return [popped_states, visited_states]
        
    def print_state(self, state):
        for row in state:  # Inner loop  
            for number in row:
                if number > 9: # Another space for one digit numbers
                    end = ' '
                else:
                    end = '  '
                print(number, end = end) # print the elements  
            print()
        print()

    def print_result(self, path_found, expansions_number, visited_states_number):             
        for index in range(len(path_found)):
            print('State #' + str(index + 1))
            self.print_state(path_found[index])

        print('Visited state number - ' + str(visited_states_number) + '\n')

        print('Expansion states - ' + str(expansions_number) + '\n')

    def run_a_star(self, init_state, withHeurestic = False):
        start_time = time.time()
        expansions_number = 0
        visited_states = {}
        active_states = {}
        # Initial goal is the first current goal 
        current_state = {'content': init_state, 'score': 0 + (self.calc_heurestic(init_state) if withHeurestic else 0), \
            'depth': 0, 'parent_state': None}
        visited_states[self.state_to_key(current_state['content'])] = current_state

        while not self.isGoal(current_state['content']):
            expansions_number += 1
            popped_states = self.pop_state(current_state, withHeurestic)

            [active_states, visited_states] = self.insert_popped_states(popped_states, visited_states, active_states)
            # Choose a new current state with best score
            key = self.get_next_state_key(active_states, min)
            current_state = active_states[key]
            del active_states[key] 
            # Add current state into visited states
            visited_states[self.state_to_key(current_state['content'])] = current_state 
            
        
        path_found = self.get_full_path(current_state, visited_states)
        self.print_result(path_found, expansions_number, len(visited_states))

        print("--- %s seconds ---" % (time.time() - start_time))

    
    def run_iteration_deepening(self, init_state):
        start_time = time.time()
        expansions_number = 0
        visited_counter = 0
        iteration_depth = 0
        
        goal_found = False
        while iteration_depth < self.ID_MAX_DEPTH and not goal_found:
            active_states = { self.state_to_key(init_state): {'content': init_state, 'score': 0, 'depth': 0, 'parent_state': None} }
            visited_states = {}
            current_state = {}
            while len(active_states):
                # Add current state into visited states
                if current_state:
                    visited_states[self.state_to_key(current_state['content'])] = current_state 
                # Choose a new current state with best score
                key = self.get_next_state_key(active_states, max)
                current_state = active_states[key]
                del active_states[key]


                if self.isGoal(current_state['content']):
                    goal_found = True
                    break

                if current_state['depth'] < iteration_depth:
                    expansions_number = expansions_number + 1
                    popped_states = self.pop_state(current_state, False)
                    # 1) Undoing popped states which are visited with less score
                    # 2) Undoing already visited states which have better score in next state 
                    [popped_states, visited_states] = self.remove_states(popped_states, visited_states)                    
                    # Union ative states with new next states
                    active_states = self.merge_states(active_states, popped_states)

            iteration_depth = iteration_depth + 1
            visited_counter = visited_counter + len(visited_states)
        
        if not goal_found:
            print('Running with depth ' + str(self.ID_MAX_DEPTH) + ' - goal not found')
            exit()

        path_found = self.get_full_path(current_state, visited_states)
        
        self.print_result(path_found, expansions_number, visited_counter)

        print("--- %s seconds ---" % (time.time() - start_time))