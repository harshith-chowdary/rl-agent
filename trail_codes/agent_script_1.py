import gridworld
import numpy

def is_valid_block(state):
    if state in world.obstacles:
        return 0
    if state[0] in range(10) and state[1] in range(15):
        return 1
    return 0

def value_update(state):
    #updates the value of a block into the values 2D array
    global values
    for i in range(4):
        next_state, reward = world.step(state,i)
        vs_next=values[next_state[0]][next_state[1]]
        if vs_next!='X':
            vs=reward+vs_next
            #print(vs)
            vs=vs+(0.01)*(reward+vs_next-vs)
            #print(vs)
            if values[state[0]][state[1]]=='X':
                values[state[0]][state[1]]=vs
            else:
                if vs>values[state[0]][state[1]]:
                    values[state[0]][state[1]]=vs
    #print(values[state[0]][state[1]])
    #return values[state[0]][state[1]]

def linked_blocks(state):
    global value_update_list
    global count
    #global xtracount
    if count==max_count: 
        return
    linked_list=[]
    for i in [-1,1]:
        linked_list.append([state[0]+i,state[1]])
        linked_list.append([state[0],state[1]+i])
    for block in linked_list:
        if is_valid_block(block):
            if block not in [world.START,world.GOAL]:
                if block not in value_update_list:
                    count+=1
                    value_update_list.append(block)
                    linked_blocks(block)
                else:
                    if state[0] in [4,5,6]:
                        #xtracount+=1
                        value_update_list.append(block)

world=gridworld.GridWorld()
values=[['X']*world.WORLD_WIDTH for i in range(world.WORLD_HEIGHT)]
values[world.GOAL[0]][world.GOAL[1]]=0
value_update_list=[]
count=0
#xtracount=0
max_count=(world.WORLD_WIDTH*world.WORLD_HEIGHT)-len(world.obstacles)-2
linked_blocks(world.GOAL)
#print(value_update_list)
for block in value_update_list:
    value_update(block)
for ch in values:
    print(ch, end=":\n")
