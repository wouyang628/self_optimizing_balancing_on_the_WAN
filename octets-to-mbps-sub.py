#Thanks Venkat to provide this user function
from __future__ import print_function
import sys
import copy
prev_value = {}
prev_time = {}
prev_mbps = {}

def octets_to_mbps(intf_name, ifl_id, octets, **kwargs):
    intf_name_ifl_id = intf_name + '.' + ifl_id
    # Get previous values
    global prev_value
    global prev_time
    global prev_mbps

    # get present time
    cur_time = kwargs.get('point_time', 0)
    octets = int(octets)

    #convert octets to mb
    mb = octets / 1000000.0
    cur_value = mb*8

    # Calculate time difference between previous and present point
    time_difference = (cur_time - prev_time.get(intf_name_ifl_id, 0))/1000000000.0

    # Calculare data sent in Mbps
    try:
        mbps = (cur_value - prev_value.get(intf_name_ifl_id, 0)) / time_difference
    except Exception:
        print("Hit Exception", file=sys.stderr)
        mbps = prev_mbps.get(intf_name_ifl_id, 0)

    #update global values
    prev_value[intf_name_ifl_id] = cur_value
    prev_time[intf_name_ifl_id] = cur_time


    return mbps