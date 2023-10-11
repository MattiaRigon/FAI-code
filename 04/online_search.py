
manhattan = lambda maze, s : abs(maze.goal[0] - s[0]) + abs(maze.goal[1] - s[1])

def odfs_printer(it, maze, s_curr, s_prev, a, result, untried, unbacktracked):

    restr = result[s_curr] if s_curr in result else '-'
    restr2 = result[s_prev] if s_prev is not None and s_prev in result else '-'
    unstr = untried[s_curr] if s_curr in untried else '-'
    ubstr = unbacktracked[s_curr] if s_curr in unbacktracked else '-'
    print("---")
    print("s':", s_curr, "s:", s_prev, "a:", a)
    print("result[s']:", restr)
    print("result[s]:", restr2)
    print("untried[s']:", unstr)
    print("unbacktracked[s']:", ubstr)
    print()

    maze.plot(s_curr)


def lrtastar_printer(it, maze, s_curr, s_prev, a, result, H):
    
    restr = result[s_curr] if s_curr in result else '-'
    restr2 = result[s_prev] if s_prev is not None and s_prev in result else '-'
    hstr = H[s_curr] if s_curr in H else '-'
    print("---")
    print("s':", s_curr, "s:", s_prev, "a:", a)
    print("result[s']:", restr)
    print("result[s]:", restr2)
    print("H[s']:", hstr)
    print()

    maze.plot(s_curr)



def online_dfs(maze, printer=None):

    s_prev, a = None, None
    result = dict()
    untried = dict()
    unbacktracked = dict()

    s_curr = maze.init
    it = 0

    if printer is not None:
        printer(it, maze, s_curr, s_prev, a, result,
                untried, unbacktracked)

    while True:

        it += 1

        if s_curr == maze.goal:
            if printer is not None:
                printer(it, maze, s_curr, s_prev, a, result,
                        untried, unbacktracked)
            return True

        if s_curr not in untried:
            # s_curr explored for the first time
            # aux data structures are initialized
            untried[s_curr] = maze.actions(s_curr)
            unbacktracked[s_curr] = []

        if s_prev is not None:
            # neither first step
            # nor a backtrack
            
            if s_prev not in result:
                result[s_prev] = {a : s_curr}
            else:
                result[s_prev][a] = s_curr

            unbacktracked[s_curr].append(s_prev)

        if printer is not None:

            printer(it, maze, s_curr, s_prev, a, result,
                    untried, unbacktracked)

        if len(untried[s_curr]) == 0:

            if len(unbacktracked[s_curr]) == 0:
                return False

            s_next = unbacktracked[s_curr].pop()
            a = None            
            for b in result[s_curr]:
                if result[s_curr][b] == s_next:
                    a = b
                    break

            s_prev = None # that dreaded line

        else:
            a = untried[s_curr].pop(0)
            s_prev = s_curr

        # execute
        s_curr = maze.execute(s_curr, a)


def lrtastar(maze, h, printer=None):

    def lrtas_cost(maze, s, a, result, H, h):

        s_next = None
        if s in result and a in result[s]:
            # uniform c(s, a, s') = 1 in our mazes
            return H[result[s][a]] + 1        
        else:
            return h(maze, s)


        

    s_prev, a = None, None
    result = dict()
    H = dict()

    s_curr = maze.init
    it = 0

    if printer is not None:
        printer(it, maze, s_curr, s_prev, a, result, H)

    while True:

        it += 1

        if s_curr == maze.goal:
            if printer is not None:
                printer(it, maze, s_curr, s_prev, a, result, H)

            return True

        if s_curr not in H:
            # s_curr explored for the first time
            # aux data structures are initialized
            H[s_curr] = h(maze, s_curr)

        if s_prev is not None:
            if s_prev not in result:
                result[s_prev] = {a : s_curr}
            else:
                result[s_prev][a] = s_curr

            H[s_prev] = min(lrtas_cost(maze, s_prev, b, result, H, h)
                            for b in maze.actions(s_prev))

            
        if printer is not None:
            printer(it, maze, s_curr, s_prev, a, result, H)


        a_costs = [(a, lrtas_cost(maze, s_curr, a, result, H, h))
                   for a in maze.actions(s_curr)]
        a_costs.sort(key=lambda x : (x[1], 'NESW'.index(x[0])))
        a = a_costs[0][0] # lower estimated cost action

        s_prev = s_curr
        s_curr = maze.execute(s_curr, a)
        


if __name__ == '__main__':

    from maze import Maze
    test_maze = Maze(2)
    test_maze.random(666)
    # uncomment this for ODFS
    #online_dfs(test_maze, printer=odfs_printer)
    lrtastar(test_maze, manhattan, printer=lrtastar_printer)

            
            

    
    
    
