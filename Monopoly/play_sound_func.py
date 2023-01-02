import winsound
import psutil
import time
import sys

def make_windows_sound(sound_file):
    #frequency = 1830 
    frequency = 330
    duration = 500
    #winsound.Beep(frequency, duration)
    winsound.PlaySound(sound_file, winsound.SND_FILENAME)

    # sound = 
    # flags = 
    # winsound.PlaySound(sound, flags)

def cur_cpu_usage():
    cpu_usage = float(psutil.cpu_percent())
    #print("Scanned cpu_usage: ", cpu_usage)
    return cpu_usage

def mean(list):
    return sum(list) / len(list)





if __name__ == "__main__":
    # for i in range(2):
    #     play("s")
    #     time.sleep(1)    
    make_windows_sound(sys.argv[1])




# if __name__ == "__main__":

#     print("Let sys.argv[1]: int -> 0-100   , to represent percent of CPU used.")
#     print("When the CPU load is under the defined threshold it beeps, letting you know ")
#     print("that you need to start another JOB.")
#     print("")

#     if len(sys.argv) > 1: threshold = int(sys.argv[1])
#     else: threshold = 65
    
#     cpu_readings = [50]*205
#     mean_cpu_level = round(mean(cpu_readings[-200:]), 1)
#     for i in range(10000000000000000000000):
#         time.sleep(0.3)
#         cur_cpu_level = cur_cpu_usage()
#         cpu_readings.append(cur_cpu_level)
#         mean_cpu_level = round(mean(cpu_readings[-200:]), 1)
#         print("\n    Current CPU level: {:<4}%   Mean minute CPU level: {:<4}%  \n ".format(
#             cur_cpu_level, mean_cpu_level))
#         if mean_cpu_level < threshold and i%30 == 0:
#             make_windows_sound()
#             #print("\n    CPU Usage too low! Optimal performance: {}%  \n ".format(threshold))
