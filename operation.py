import matplotlib.pyplot as plt
import numpy as np
import random
from procedure import generation, fitness_cal, config2, parents_variable
import time

### setting parameters ###

# GA
population_size = 30
iteration_loop = 50
cr = 0.9
mr = 0.3

# architect
ln = 208.661 # ft
type = 'middle'
bw = 20.669 # inch
H = 23.622 # inch
hf = 7.0866 # inch

# engineer
Mu_plus = 217.972 # k-ft
Mu_minus = 272.056 # k-ft
Vu = 60.678 # kips
Tu = 32.776 # k-ft
beff = 72.834 # ft
cc = 5/2.54 # inch
fc = 5 # ksi
fy = 60 # ksi


length_main_A, length_main_N, length_s, length_stirrups_A, length_stirrups_N, length_total = config2

def main(ln, type, bw, H, hf, Mu_plus, Mu_minus, Vu, Tu, beff, cc, fc, fy, iteration_loop):
    # start = time.time()
    parents_matrix = [[int(random.randint(0, 1)) for _ in range(length_total)] for _ in range(population_size)] 

    config1 = [population_size, cr, mr]
    config2 = {
        'Mu+': Mu_plus,
        'Mu-': Mu_minus,
        'Vu': Vu,
        'Tu': Tu,
        'type': type,
        'ln': ln,
        'beff': beff,
        'bw': bw,
        'H': H,
        'hf': hf,
        'cc': cc,
        'fc': fc,
        'fy': fy,
    }
    iteration_track = []
    local_maximum_track = []
    global_maximum_track = []
    global_maximum = -10000
    for iteration in range(iteration_loop):
        local_maximum = -10000
        
        children_matrix, P_fitness, parents_matrix_qualified, data_list = generation(parents_matrix, config1, config2)
        if len(parents_matrix_qualified) == 0:
            parents_matrix = [[int(random.randint(0, 1)) for _ in range(length_total)] for _ in range(population_size)] 
            print("no available chromosome, regenerate a initial population")
            continue
        local_maximum = max(P_fitness)
        index = P_fitness.index(local_maximum)
        local_parents = parents_matrix_qualified[index]
        local_data = data_list[index]
        if local_maximum > global_maximum:
            global_parents = local_parents.copy()
            global_maximum = local_maximum
            global_data = local_data.copy()
            
        iteration_track.append(iteration)
        local_maximum_track.append(local_maximum)
        global_maximum_track.append(global_maximum)  
        parents_matrix = children_matrix
        
        print("global_parents", global_parents)     
        print("iteration:", iteration)
        print("local_maximum:", local_maximum)
        print("global_maximum:", global_maximum)
        
    # end = time.time()
    # print("\n")
    # print("time cost:", end - start)
    # print("\n")
    
    # # 歷時紀錄
    # plt.plot(iteration_track, local_maximum_track, label='Local Maximum (Current Gen)', color='blue', linestyle='--')
    # plt.plot(iteration_track, global_maximum_track, label='Global Maximum (Best So Far)', color='red', linewidth=2)
    # plt.xlabel('Iteration (Generation)')
    # plt.ylabel('Objective Function Value')
    # plt.title('Genetic Algorithm Optimization Progress')
    # plt.grid(True)
    # plt.legend()
    
    reinforcement_usage = global_maximum
    main_A, main_N, s, stirrups_A, stirrups_N = parents_variable(global_parents)
    Mn_plus, Mn_minus, Vn, Tn = global_data['Mn+'], global_data['Mn-'], global_data['Vn'], global_data['Tn']
    d1, d2, distance, sw = global_data['d1'], global_data['d2'], global_data['distance'], global_data['sw']
    return int(main_A), int(main_N), int(s), int(stirrups_A), int(stirrups_N), float(reinforcement_usage), float(d1), float(d2), float(sw), float(distance), float(Mn_plus), float(Mn_minus), float(Vn), float(Tn)

# main_A, main_N, s, stirrups_A, stirrups_N, reinforcement_usage, d1, d2, sw, distance, Mn_plus, Mn_minus, Vn, Tn = main(ln, type, bw, H, hf, Mu_plus, Mu_minus, Vu, Tu, beff, cc, fc, fy,)

# print("main_A:", main_A, "main_N:", main_N, "stirrups_A:", stirrups_A, "stirrups_N:", stirrups_N)
# print("d1:", d1, "d2:", d2, "distance:", distance, "sw:", sw, "s:", s)
# print("Mn_plus:", Mn_plus, "Mn_minus:", Mn_minus, "Vn:", Vn, "Tn:", Tn)
# print("least reinforcement usage:", -reinforcement_usage)
# plt.show()