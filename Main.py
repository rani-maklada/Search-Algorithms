import sys

from search_algorithms import search_algorithms

def main():          
    init_state = []
    # Read initial state from txt file
    with open("./3x3_1.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            init_state.append([int(x) for x in line.split(" ")])
    
    if sys.argv[1] == 'id':
        sa = search_algorithms()
        sa.run_iteration_deepening(init_state)
    elif sys.argv[1] == 'bfs':
        sa = search_algorithms()
        sa.run_a_star(init_state, withHeurestic = False)
    elif sys.argv[1] == 'astar':
        sa = search_algorithms()
        sa.run_a_star(init_state, withHeurestic = True)
        

if __name__ == "__main__":
    main()