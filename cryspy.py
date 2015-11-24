# Cryptography with Dispy

import dispy

def crypt(data, psw):
    crypted = ""
    for i in range(len(data)):
        crypted += (XOR(data[i], psw[i%len(psw)]))

    return crypted

def decrypt(data, psw):
    decrypted = ""
    for i in range(len(data)):
        decrypted += (XOR(data[i], psw[i%len(psw)]))

    return decrypted

def XOR (c, x):
    a = bin(ord(c))[2:]
    b = bin(ord(x))[2:]
    
    if len(a) < 8:
        a = (8-len(a))*"0" + a

    if len(b) < 8:
        b = (8-len(b))*"0" + b

    result = ""

    for i in range(8):
        result += str(int(a[i] != b[i]))
    
    result = chr(int(result, 2))

    return result

ip_master = "192.168.1.106"
ip_nodes = ["192.168.1.107"]

cluster = dispy.JobCluster(
    crypt,
    depends = [XOR],
    nodes = ip_nodes,
    ip_addr = ip_master
)

job = cluster.submit("Testing dispy and XOR cryptography", "password")
# cluster.wait() or job() to wait only the job
job()

cluster.stats()

computationResult = job.result
print "Crypted string: " + computationResult
print "Decrypted string: " + decrypt(computationResult, "password")