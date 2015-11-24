import dispy
import random
import time
import sys
import csv
import ftplib

# argv: [how many nodes][how many tests][how many rolls][ftp password]

global ip_master
global ip_nodes_raw

ip_master = "192.168.1.103"
ip_nodes_raw = ["192.168.1.103"]

def twoDiceRollSum (n):
    result = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for i in xrange(n):
        dice_a = random.randint(1, 6)
        dice_b = random.randint(1, 6)

        result[dice_a + dice_b - 2] += 1

    return result

def uploadResult (fileResult, psw):
    ftp = ftplib.FTP('ftp.picluster.altervista.org','picluster', psw)
    fResult = open(fileResult,'rb')    
    ftp.storbinary("STOR " + fileResult, fResult) 
    fResult.close()    
    ftp.quit()

def csv_writer (res, path):

    data = [
        ['somma', 'numero'],        
        ['Due', res[0]],
        ['Tre', res[1]],
        ['Quattro', res[2]],
        ['Cinque', res[3]],
        ['Sei', res[4]],
        ['Sette', res[5]],
        ['Otto', res[6]],
        ['Nove', res[7]],
        ['Dieci', res[8]],
        ['Undici', res[9]],
        ['Dodici', res[10]]
    ]
    
    csv_file = open(path, "wb")
    try:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)
    finally:
        csv_file.close()

def run (nNodes, nTimes, nThrows):

    #ip_master = "192.168.1.103"
    #ip_nodes_raw = ["192.168.1.103"]

    ip_nodes = []

    for i in range (nNodes):
        ip_nodes.append(ip_nodes_raw[i])

    cluster = dispy.JobCluster(
        twoDiceRollSum,
        nodes = ip_nodes,
        ip_addr = ip_master
    )

    jobs = []

    for i in range(nTimes):
        jobs.append(cluster.submit(nThrows))

    cluster.wait()
    cluster.stats()

    r = []

    for j in jobs:
        r.append(j.result)

    # global result sum
    result = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for n in r:
        for i in xrange(len(n)):
            result[i] += n[i]

    return result 

if __name__ == "__main__":

    tStart = time.time()

    result = run(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))

    tEnd = time.time() - tStart

    print "Computation real time: " + str(tEnd) + " s"

    print "Creating .csv..."
    csv_writer(result, "export.csv")

    print "Uploading data..."
    uploadResult("export.csv", sys.argv[4])

    print "Done! http://picluster.altervista.org/index.html\n"