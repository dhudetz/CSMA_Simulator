from test_node import Node, IDLE, BUSY, SENDING
from random import random, randrange, shuffle
import numpy as np
import matplotlib.pyplot as plt

# competitive advantage of being far away and not following protocol

p_values = [0.01, 0.1, 0.5, 1] #p-value
frame_size = 8 #tau
num_timeslots = 50000
#generation = 0.3 #lamba
g_values = np.arange(0, 0.75, 0.01)

#Initialize nodes
A = Node(0, 0, num_timeslots)
B = Node(1, 1, num_timeslots)
C = Node(0, 1, num_timeslots)
my_nodes = [A, B, C]

transmission_count = 0

success_values = []

for p_index, p in enumerate(p_values):
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

        num_unused = 0
        num_successful = 0
        A_num_successful = 0
        B_num_successful = 0
        C_num_successful = 0
        num_failed = 0

        for x in collisions:
            if x == 0:
                num_unused += 1
            elif x == 1:
                num_successful += 1
            else:
                num_failed +=1
        success_values.append([])
        success_values[p_index].append(num_successful/num_timeslots)

        #print('g value: ', generation)
        #print('transmission count: ', transmission_count)
        #print('    unused = ', num_unused/num_timeslots)
        #print('    SUCCESS = ', num_successful/num_timeslots)
        #print('    FAILED = ', num_failed/num_timeslots)
        #print('    INFO SENT = ', ((num_successful-num_failed)/num_timeslots))

        for n in my_nodes:
            n.reset_timeslots()

# plotting
fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.scatter(x = g_values, y = success_values[0], s=10, c='b', marker="s", label='p = 0.01')
ax1.scatter(x = g_values, y = success_values[1], s=10, c='r', marker="o", label='p = 0.10')
ax1.scatter(x = g_values, y = success_values[2], s=10, c='g', marker="h", label='p = 0.50')
ax1.scatter(x = g_values, y = success_values[3], s=10, c='m', marker="*", label='p = 1.00')
plt.legend(loc='upper right');
plt.xlabel("Generation_Value")
plt.ylabel("Throughput")

plt.show()
