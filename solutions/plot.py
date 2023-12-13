import matplotlib.pyplot as plt 
import sys

def get_args(args):
    if len(args) == 0:
        print("No args given, stopping")
        exit(0)
    if len(args) == 2:
        mode = str(args[1])
        if mode != "gpu":
            mode = "cpu"
    else:
        mode = "cpu"

    core_num = int(args[0])
    return core_num, mode

def read_data(filename: str) -> tuple[list, list]:
    x, y = [], []
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines[3:]:
            arg, func = line.split()
            arg = int(arg)
            func = float(func)
            x.append(arg)
            y.append(func)
        return x, y

def get_data(core_num: int, mode: str):
    if mode != "gpu": mode = ""
    else: mode = "_" + mode
    core_num = str(core_num)
    filename_bw = f"osu_p2p{mode}_bw_c{core_num}.txt"
    filename_lat = f"osu_p2p{mode}_lat_c{core_num}.txt"
    return read_data(filename_bw), read_data(filename_lat)
            
core, mode = get_args(sys.argv[1:])
bw, lat = get_data(core, mode)


# plt.plot(x, y, marker = 'o', c = 'b') 
# plt.title("Comparison") 
# plt.xlabel('Memory footprint') 
# plt.xticks(x,[f"{x[i]} ({z[i]})" for i in range(len(x))], rotation=90)
# plt.ylabel('Bandwidth [GB/s]') 
# # plt.yscale('log')
# plt.legend() 

fig, axs = plt.subplots(1,2, figsize=(20,8))
fig.suptitle('Comparison')
ax1, ax2 = axs
ax1.set(xlabel='Packet size [bits]', ylabel='Network latency [usec]', title='Latency / Packet size', xscale="log", yscale="log")
ax2.set(xlabel='Packet size [bits]', ylabel='Bandwidth [GB/s]', title='Bandwidth / Packet size', xscale="log", yscale="log")
ax1.plot(*lat, marker = 'o', c = 'b', label=f'Network latency C = {core} [usec]')
ax2.plot(*bw, marker = 'o', c = 'b', label=f'Bandwidth C = {core} [MB/s]')


if core != 0:
    bw0, lat0 = get_data(0, mode)
    ax1.plot(*lat0, marker = 'o', c = 'r', label=f'Network latency C = 0 [usec]')
    ax2.plot(*bw0, marker = 'o', c = 'r', label=f'Bandwidth C = 0 [GB/s]')
    
# 1 usec, 12.5 GB/s
# 25 GB/s
BW_THEORY = 25 if mode == "gpu" else 12.5
BW_THEORY = BW_THEORY * 1000
LAT_THEORY = 1
ax1.axhline(y=LAT_THEORY, color='green', linestyle='--', label='Theoretical Latency')
ax2.axhline(y=BW_THEORY, color='green', linestyle='--', label='Theoretical Bandwidth')
    
ax1.legend()
ax2.legend()
# plt.show()

# plt.savefig("mvm_ji.png",bbox_inches='tight',dpi=100)
plt.tight_layout()
plt.savefig(f"osu_p2p_{'' if mode != 'gpu' else mode}_c{core}.png")