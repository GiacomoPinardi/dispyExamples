import dispy
import random
import time

def coinFlip (n):
    head = 0    
    for i in range(n):
        coin = random.randint(0, 1)
        if coin == 0:
            head += 1

    return head

t = time.time()

ip_master = "10.59.1.34"
ip_nodes = ["192.168.1.101", "192.168.1.102", "192.168.1.103"]
#ip_nodes = ["192.168.1.101"]

cluster = dispy.JobCluster(
    coinFlip,
    nodes = ip_nodes,
    ip_addr = ip_master
)

jobs = []

for i in range(1, 21):
    jobs.append(cluster.submit(100000))

cluster.wait()

cluster.stats()

for j in jobs:
    print "Result: " + str(j.result)

print "Computation real time: " + str(time.time() - t)
