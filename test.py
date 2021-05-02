from test_node import Node, IDLE, BUSY, SENDING
from random import random, randrange, shuffle
import numpy as np
import matplotlib.pyplot as plt

# competitive advantage of being far away and not following protocol

p = 0.5 #p-value
frame_size = 8 #tau
num_timeslots = 50000
#generation = 0.3 #lamba
g_values = np.arange(0, 1, 0.05)

#Initialize nodes
A = Node(0, 0, num_timeslots)
B = Node(1, 1, num_timeslots)
C = Node(0, 1, num_timeslots)
my_nodes = [A, B, C]

transmission_count = 0

success_values = []
A_success_values = []
B_success_values = []
C_success_values = []

for generation in g_values:
    for i in range(num_timeslots):
        #shuffle(my_nodes)
        for n in my_nodes:
            # if node is not already signaling
            if n.get_timeslot_state(i) != SENDING:
                if n.ready == 0:
                    # roll for new frame generation
                    if random() < generation:
                        n.ready = 1
            # if timeslot is perceived idle and frame is ready
            if n.get_timeslot_state(i) == IDLE and n.ready == 1:
                # roll for new signal using p-value
                if random() < p:
                    transmission_count += 1
                    # alert other nodes
                    others = (x for x in my_nodes if x != n)
                    for n2 in others:
                        n2.update_senses(n.xpos, n.ypos, frame_size, i)
                    # run node transmission
                    n.run_signal(frame_size, i)

    #print(A.timeslots)
    #print(B.timeslots)
    #print(C.timeslots)
    #print('\n')

    collisions = [0]*num_timeslots
    for i in range(num_timeslots):
        num_sending = 0
        for n in my_nodes:
            if n.timeslots[i] == 2:
                num_sending += 1
        if num_sending == 1:
            collisions[i] = 1
        elif num_sending > 1:
            collisions[i] = 2
    #print(collisions)

    num_unused = 0
    num_successful = 0
    A_num_successful = 0
    B_num_successful = 0
    C_num_successful = 0
    num_failed = 0

    for i in range(num_timeslots):
        if collisions[i] == 1:
            if A.timeslots[i] == 2:
                A_num_successful += 1
            elif B.timeslots[i] == 2:
                B_num_successful += 1
            elif C.timeslots[i] == 2:
                C_num_successful += 1

    A_success_values.append(A_num_successful/num_timeslots)
    B_success_values.append(B_num_successful/num_timeslots)
    C_success_values.append(C_num_successful/num_timeslots)

    for x in collisions:
        if x == 0:
            num_unused += 1
        elif x == 1:
            num_successful += 1
        else:
            num_failed +=1

    success_values.append(num_successful/num_timeslots)
    #print('g value: ', generation)
    #print('transmission count: ', transmission_count)
    #print('    unused = ', num_unused/num_timeslots)
    #print('    SUCCESS = ', num_successful/num_timeslots)
    #print('    FAILED = ', num_failed/num_timeslots)
    #print('    INFO SENT = ', ((num_successful-num_failed)/num_timeslots))

    for n in my_nodes:
        n.reset_timeslots()

# plotting
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(x = g_values, y = A_success_values)
plt.xlabel("g_value")
plt.ylabel("success_values")

plt.show()

# plotting
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(x = g_values, y = B_success_values)
plt.xlabel("g_value")
plt.ylabel("success_values")

plt.show()

# plotting
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(x = g_values, y = C_success_values)
plt.xlabel("g_value")
plt.ylabel("success_values")

plt.show()
