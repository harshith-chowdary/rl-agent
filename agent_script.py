import plotter
import gridworld
import random

def is_valid_block(state):
    if state in world.obstacles:
        return 0
    if state[0] in range(10) and state[1] in range(15):
        return 1
    return 0


def value_update(state):
    # updates the value of a block into the values 2D array
    global values
    for i in range(4):
        next_state, reward = world.step(state,i)
        vs_next=values[next_state[0]][next_state[1]]
        if vs_next!='X':
            vs=reward+vs_next
            #print(vs)
            #vs=vs+(0.01)*(reward+vs_next-vs) --> TD(0) method
            if values[state[0]][state[1]]=='X':
                values[state[0]][state[1]]=vs
            else:
                if vs>values[state[0]][state[1]]:
                    values[state[0]][state[1]]=vs
    #print(values[state[0]][state[1]])
    #return values[state[0]][state[1]]


def operation_scavenger():
    # to value unvalued blocks till call-time and returns number of unvalued 
    count_left=0
    for y in range(world.WORLD_HEIGHT):
        for x in range(world.WORLD_WIDTH):
            if values[y][x]=='X' and [y,x] not in world.obstacles:
                value_update([y,x])
                if values[y][x]=='X':
                    count_left+=1
    return count_left


def seq_values_update(state):
    # updates the values of blocks in an effective sequence
    Y=state[0]
    X=state[1]
    for radius in range(1,18):
        for y in range(0,radius+1):
            if is_valid_block([Y+y,X+radius-y]):
                value_update([Y+y,X+radius-y])
            if is_valid_block([Y+y,X-radius+y]):
                value_update([Y+y,X-radius+y])
            if is_valid_block([Y-y,X-radius+y]):
                value_update([Y-y,X-radius+y])
            if is_valid_block([Y-y,X+radius-y]):
                value_update([Y-y,X+radius-y])
    left=operation_scavenger()
    while left>0:
        #print(left, end='\n')
        left=operation_scavenger()
    for count in range(4):
        for y in range(world.WORLD_HEIGHT):
            for x in range(world.WORLD_WIDTH):
                if [y,x] not in world.obstacles:
                    value_update([y,x])


def is_good_action(state,action):
    # to make agent choose the better next step
    next_state, reward=world.step(state,action)
    if next_state==state:
        return 0
    if values[next_state[0]][next_state[1]]<values[state[0]][state[1]]:
        return 0
    return 1


def possible_path_recursion(state):
    # for generating a possible path to reach goal
    curr_path_list=[]
    total_reward=0
    if state==world.GOAL:
        return curr_path_list, total_reward, len(curr_path_list)
    for action in range(4):
        if is_good_action(state,action):
            curr_path_list.append(action)
            next_state, temp_reward=world.step(state,action)
            total_reward+=temp_reward
            possible_path_recursion(next_state)
    return [0],0,0


def possible_path_iteration_random(state):
    # effective than recursive method
    curr_path_list=[]
    total_reward=0
    while state!=world.GOAL:
        good_actions=[]
        for action in range(4):
            if is_good_action(state,action):
                good_actions.append(action)
        if good_actions:
            action=random.choice(good_actions)
            good_actions.clear()
            curr_path_list.append(action)
            next_state, temp_reward=world.step(state,action)
            total_reward+=temp_reward
            state=next_state
        else:
            return [],0,0
    return curr_path_list, total_reward, len(curr_path_list)


def possible_path_iteration(state):
    # effective than previous random iteration method
    curr_path_list=[]
    state_path_list=[]
    total_reward=0
    while state!=world.GOAL:
        flag=0
        for action in range(4):
            if is_good_action(state,action):
                flag=1
                curr_path_list.append(action)
                next_state, temp_reward=world.step(state,action)
                total_reward+=temp_reward
                state=next_state
                state_path_list.append(next_state)
        if flag==0:
            return curr_path_list, total_reward,0,0
    return curr_path_list, total_reward, len(curr_path_list), state_path_list

world=gridworld.GridWorld()
graph_out=plotter.line_graph()
values=[['X']*world.WORLD_WIDTH for i in range(world.WORLD_HEIGHT)]
values[world.GOAL[0]][world.GOAL[1]]=0
rewards_list=[]
paths_tried=[]
paths_list=[]
states_path=[]

seq_values_update(world.GOAL)
#values[6][1]='S'

for ch in values:
    print(ch, end="\n")

paths_triggered=0
N=25
#N=int(input("Enter the limit to successful paths : "))
successful_paths=[i for i in range(N)]
while len(rewards_list)<N:
    paths_triggered+=1
    path,reward,steps,statepath=possible_path_iteration(world.START)
    if steps!=0:
        paths_list.append(path)
        rewards_list.append(reward)
        paths_tried.append(paths_triggered)
        states_path.append(statepath)
        print("Path is : ",path)
        print("Reward is : ",reward)
        print("No of paths triggered till now : ",paths_triggered)
print(rewards_list)
max_reward=max(rewards_list)
indx_max_rew_path=rewards_list.index(max_reward)
print("Therefore the path with maximum reward is : ")
print("Path : ",paths_list[indx_max_rew_path])
print("Path States : ",states_path[indx_max_rew_path])
print("With the highest reward of : ",max_reward)
graph_out.draw(paths_tried,rewards_list,"Rewards Distribution for succeeded Paths","Number of Paths Triggered","Reward")
graph_out.draw(paths_tried,successful_paths,"Successful Paths vs Paths Triggered","Number of Paths Triggered","Successful Paths")