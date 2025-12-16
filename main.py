from CombinationGenerator import CombinationGenerator
from colorama import Fore, Back, Style, init
import readchar
from NSDevice import sendRecord, connect

cg = CombinationGenerator()
init(autoreset=True) # colorama init


# Control
# cg.register('trial_name', ['PH_Dec25'])
# cg.register('artery_type', ['CONTROL'])
# cg.register('blockage', ['0pc'])
# cg.register('location', ['low', 'mid', 'up'])
# cg.register('bpm', ["60bpm", "70bpm", "80bpm", "90bpm"])
# cg.register('rep', ['1rep', '2rep', '3rep', '4rep', '5rep'])

# CCA
# cg.register('trial_name', ['PH_Dec25'])
# cg.register('artery_type', ['CCA'])
# cg.register('blockage', ['30pc', '40pc', '50pc', '60pc', '65pc', '70pc', '72pc', '78pc', '88pc']) # 9
# cg.register('location', ['low', 'mid', 'up'])
# cg.register('bpm', ["60bpm", "70bpm", "80bpm", "90bpm"])
# cg.register('rep', ['1rep', '2rep', '3rep', '4rep', '5rep'])

# # ICA
# cg.register('trial_name', ['PH_Dec25'])
# cg.register('artery_type', ['ICA'])
# cg.register('blockage', ['30pc', '40pc', '50pc', '54pc', '67pc', '70pc', '72pc', '84pc']) # 8
# cg.register('location', ['low', 'mid', 'up'])
# cg.register('bpm', ["60bpm", "70bpm", "80bpm", "90bpm"])
# cg.register('rep', ['1rep', '2rep', '3rep', '4rep', '5rep'])

# new shi
ica_sorted = ['ICA_30pc', 'ICA_50pc','ICA_52pc', 'ICA_54pc', 'ICA_67pc', 'ICA_70pc', 'ICA_84pc']
cca_sorted = ['CCA_30pc', 'CCA_40pc', 'CCA_50pc', 'CCA_65pc', 'CCA_70pc', 'CCA_78pc', 'CCA_88pc']

ica_seq = [1,7,4,3,6,2,5]
cca_seq = [1,7,4,3,6,2,5]

ica = []
cca = []

for i in range(len(ica_seq)):
    ica.append(ica_sorted[ica_seq[i]-1])
for i in range(len(cca_seq)):
    cca.append(cca_sorted[cca_seq[i]-1])



cg.register('trial_name', ['PH_Dec25'])
cg.register('blockage', ['CONTROL_0pc', ica[0], ica[1], ica[2], cca[0], cca[1], cca[2], ica[3], ica[4], ica[5], cca[3], cca[4], cca[5], ica[6], cca[6]])
cg.register('location', ['low', 'mid', 'up'])
cg.register('bpm', ["60bpm",  "80bpm", "90bpm"])
cg.register('rep', ['1rep', '2rep', '3rep', '4rep', '5rep'])

# while True:
#     current_name = cg.getNext()
#
#     if current_name is None:
#         print(Style.BRIGHT + Fore.GREEN + Back.GREEN + "DONE!")
#         break
#
#     print(current_name)
#
# quit()



print(Fore.YELLOW + "This doesn't work with Pycharm terminal because readchar is low-level apparently.")

start_idx = 1
for i in range(1, start_idx):
    cg.getNext()

idx = start_idx

connect()

def record(name):
    print(Fore.CYAN + f"[{idx}]: " + current_name + "\t\t" + Fore.GREEN + "[_] START " + Fore.YELLOW + "[s] SKIP")
    while True:
        key = readchar.readkey()
        if key == ' ':
            print("Recording...")
            sendRecord(name)
            # rec done
            print(Fore.WHITE + "Recording done.\t\t" + Fore.GREEN + "[c] CONFIRM " + Fore.YELLOW + "[r] REPEAT")
            key = readchar.readkey()
            if key == 'c':
                return True
            else:
                print(Fore.YELLOW + "REJECTED. Repeating...")
                return False

        elif key == 's':
            return True

while True:
    current_name = cg.getNext()

    if current_name is None:
        print(Style.BRIGHT + Fore.GREEN + Back.GREEN + "DONE!")
        break

    if idx % 50 == 0:
        print(Fore.RED + "TIME FOR BACKUP! [c] to confirm.")
        while True:
            if readchar.readkey() == 'c':
                break

    ret = False
    while not ret:
        ret = record(current_name)

    idx += 1

