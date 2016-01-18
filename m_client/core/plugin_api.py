import global_setting
from plugins import cpu,load,memory,salt


def LinuxCpu():
    data = cpu.monitor()
    #print data
    return data

def load_info():
    data =load.monitor()
    return data
    
    
def LinuxMemory():
    return memory.monitor()

def salt_info():  
    return salt.monitor()  