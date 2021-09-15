import matplotlib.pyplot as plt
import numpy as np
import yaml

config = yaml.safe_load(open("./config.yml"))

names0 = ['NO_CACHE', 'FIFO', 'LFU', 'LRU', 'RR', 'Belady']
_names0 = np.arange(len(names0))
runtime = [5229.55, 3708.59, 3706.47, 3471.87, 3734.41, 3763.89]

hit_count = [15352, 14946, 15561, 15135, 14840]
miss_count = [11231, 11637, 11022, 11448, 11743]
swap_count = [4230, 7771, 5127, 5908, 8070]
time_save_count = [929.26, 964.08, 938.16, 911.39, 944.85]
full_download_time_count = [1319.48, 1319.48, 1319.48, 1319.48, 1319.48]

names = ['FIFO', 'LFU', 'LRU', 'RR', 'Belady']
_names = np.arange(len(names))

# Makespan
plot0 = plt.figure(0)
ax = plt.subplot(111)
ax.bar(names0, runtime, width=0.5)
plt.xlabel('Policies')
plt.ylabel('Runtime [s]')
plt.title('%s runtime' % config['simulator']['name'])
plt.savefig("0.png")

# Cache evaluation
plot1 = plt.figure(1)
ax = plt.subplot(111)
hit = ax.bar(_names-0.3, hit_count, width=0.3, color='g', align='center')
miss = ax.bar(_names, miss_count, width=0.3, color='r', align='center')
swap = ax.bar(_names+0.3, swap_count, width=0.3, color='b', align='center')
ax.legend((hit, miss, swap), ('hit', 'miss', 'swap'))
plt.xlabel('Policies')
plt.ylabel('Files')
plt.xticks(_names, names)
plt.suptitle("Cache policies evaluation", fontsize=18)
plt.title("%s, nodes: %d, cache size: %d, vcpu: %d, cache factor: %.2f" %
 (config['simulator']['name'], config['simulator']['nodes'], config['simulator']['cache']['size'], config['simulator']['vcpu'], config['simulator']['cache_factor']), fontsize=10)
plt.savefig("1.png")

# File download
plot2 = plt.figure(2)
ax = plt.subplot(111)
time_save = ax.bar(_names - 0.3, time_save_count, width=0.3, color='orange', align='center')
full_download = ax.bar(_names, full_download_time_count, width=0.3, color='purple', align='center')
ax.legend((time_save, full_download), ('download_size', 'full_download_size'))
plt.xticks(_names, names)
plt.xlabel('Policies')
plt.ylabel('Size [GB]')
plt.suptitle("File download", fontsize=18)
plt.title("bandwith: %.2f Gb/s, delay: %.1fs" % (config['simulator']['bandwith'], config['simulator']['delay']), fontsize=10)
plt.savefig("2.png")
plt.show()
