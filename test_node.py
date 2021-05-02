import numpy as np

IDLE = 0
BUSY = 1
SENDING = 2

class Node:
    #Class for a CSMA sim node

    def __init__(self, x_position, y_position, num_timeslots):
        self.xpos = x_position
        self.ypos = y_position
        self.num_timeslots = num_timeslots
        self.timeslots = [IDLE]*num_timeslots
        self.ready = 0

    # update internal idle/busy timeslot values based on new sensed signal
    def update_senses(self, signal_position_x, signal_position_y, signal_length, curr_timeslot):
        distance = int(np.sqrt((signal_position_x-self.xpos)**2 + (signal_position_y-self.ypos)**2))
        busy_start = distance + curr_timeslot
        busy_end = distance + curr_timeslot + signal_length
        for i in range(busy_start,busy_end):
            if i < self.num_timeslots and self.timeslots[i] == IDLE:
                self.timeslots[i] = BUSY

    def reset_timeslots(self):
        self.timeslots = [IDLE]*self.num_timeslots

    def get_timeslot_state(self, curr_timeslot):
        return self.timeslots[curr_timeslot]

    def run_signal(self, signal_length, curr_timeslot):
        signal_start = curr_timeslot
        signal_end = curr_timeslot + signal_length
        for i in range(signal_start, signal_end):
            if i < self.num_timeslots:
                self.timeslots[i] = SENDING
        self.ready = 0
