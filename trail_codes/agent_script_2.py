import gridworld
import numpy

world=gridworld.GridWorld()
values=[['X']*world.WORLD_WIDTH for i in range(world.WORLD_HEIGHT)]
values[world.GOAL[0]][world.GOAL[1]]=0
max_count=(world.WORLD_WIDTH*world.WORLD_HEIGHT)-len(world.obstacles)-2

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

def linked_blocks_list(state):
    linked_list=[]
    for i in [-1,1]:
        if is_valid_block([state[0]+i,state[1]]):
            linked_list.append([state[0]+i,state[1]])
        if is_valid_block([state[0],state[1]+i]):
            linked_list.append([state[0],state[1]+i])
    return linked_list, len(linked_list)

count=4
prev_len=0
curr_len=0
Value_update_list, curr_len=linked_blocks_list(world.GOAL)
list, curr_len=linked_blocks_list(world.GOAL)

while count<max_count:
    temp_total_list=[]
    for i in range(prev_len,curr_len):
        if Value_update_list[i] not in Value_update_list[:prev_len]:
            temp_list, temp_len=linked_blocks_list(Value_update_list[i])
            temp_total_list.extend(temp_list)
    prev_len=curr_len
    for next_block in temp_total_list:
        if next_block!=world.GOAL and next_block!=world.START:
            if is_valid_block(next_block):
                if next_block not in Value_update_list:
                    Value_update_list.append(next_block)
                    list.append(next_block)
                    count+=1
                    curr_len+=1
                else:
                    if next_block[0] in [4,5,6]:
                        Value_update_list.append(next_block)
                        curr_len+=1

for state in list:
    value_update(state)

'''for state in Value_update_list:
    value_update(state)'''

for ch in values:
    print(ch, end=":\n")