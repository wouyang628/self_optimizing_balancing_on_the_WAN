import json
import datetime as dt
import user_functions
#read in the ML result from Heahtbot

with open('ml.json', 'r') as data_file:
    json_data = data_file.read()
data = json.loads(json_data)

for i in data:
    hostname = i['hostName']
    interfaceName = i['interfaceName']
    hour = dt.datetime.now().hour
    hour = str(hour)
    thresholdkey = 'highThreshold' + hour
    highThreshold = i[thresholdkey]
    nodeID = user_functions.get_nodeID_from_hostname(hostname)
    link = user_functions.get_link_from_nodeID_and_interface(nodeID, interfaceName)
    linkIndex = link['linkIndex']
    linkID = link['id']
    endA_ID = link['endA']['node']['id']
    endZ_ID = link['endZ']['node']['id']
    if 'designParameters' in link['endA'].keys():
        currentThresholdA = link['endA']['designParameters']['trafficRerouteThreshold']
    else:
        currentThresholdA = -1
    if 'designParameters' in link['endZ'].keys():
        currentThresholdZ = link['endZ']['designParameters']['trafficRerouteThreshold']
    else:
        currentThresholdZ = -1   
    if endA_ID == nodeID:
        print "this is endA"
        endA_Threshold = highThreshold
        endZ_Threshold = currentThresholdZ
    else:
        print "this is endZ"
        endZ_Threshold = highThreshold
        endA_Threshold = currentThresholdA

    payload = user_functions.generate_link_traffic_threshold_payload(linkIndex,linkID,endA_ID,endZ_ID,endA_Threshold,endZ_Threshold)    
    r = user_functions.update_link_traffic_threshold(payload, linkIndex) 
    print r
