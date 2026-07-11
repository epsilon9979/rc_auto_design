import random
import numpy as np
from main import engineer
from information import information

info = information()

# variables ##########################
start_main_A = 8 # 8
end_main_A = 10 # 10
start_main_N = 4 # 4
end_main_N = 10 # 10
start_s = 2 # 2
end_s = 6 # 6
start_stirrups_A = 3 # 3
end_stirrups_A = 5 # 5
start_stirrups_N = 2 # 2
end_stirrups_N = 5 # 5

length_main_A = int( np.log2((end_main_A - start_main_A) + 1) ) + 1
length_main_N = int( np.log2((end_main_N - start_main_N) + 1) ) + 1
length_s      = int( np.log2((end_s - start_s) + 1) ) + 1
length_stirrups_A = int( np.log2((end_stirrups_A - start_stirrups_A) + 1) ) + 1
length_stirrups_N = int( np.log2((end_stirrups_N - start_stirrups_N) + 1) ) + 1
length_total = length_main_N + length_main_A + length_s + length_stirrups_A + length_stirrups_N

interval_main_A = length_main_A
interval_main_N = interval_main_A + length_main_N
interval_s = interval_main_N + length_s
interval_stirrups_A = interval_s + length_stirrups_A

config2 = [length_main_A, length_main_N, length_s, length_stirrups_A, length_stirrups_N, length_total]
config3 = [interval_main_A, interval_main_N, interval_s, interval_stirrups_A]
config4 = [start_main_A, end_main_A, start_main_N, end_main_N, start_s, end_s, start_stirrups_A, end_stirrups_A, start_stirrups_N, end_stirrups_N]

def mapping(binary, start, end):
    length = len(binary)
    real = 0
    for i in range(length):
        real += binary[i] * 2 ** (length - 1 - i)
    result = round( start + (end - start) * real / (2 ** length - 1) )
    return result

def objective_func(design):
    reinforcement_usage = (
        design['main_bar_num'] * info.A(design['main_bar_no']) * design['s'] +
        design['stirrups_num'] * info.A(design['stirrups_no']) * ( design['H'] - design['cc'] * 2 - info.D(design['stirrups_no']) ) + 
        2 * info.A(design['stirrups_no']) * ( design['bw'] - design['cc'] * 2 - info.D(design['stirrups_no']) )
    ) * design['ln'] / design['s']
    result, data = engineer(design)
    if result == 0:
        return 0, data
    else:
        return -reinforcement_usage, data

def crossover(parent1, parent2):
    z = random.randint(0, len(parent1) - 1)
    child1 = parent1[:z] + parent2[z:]
    child2 = parent2[:z] + parent1[z:]
    return child1, child2

def mutation(child):
    z = random.randint(0, len(child) - 1)
    child[z] = 1 - child[z]
    return child

def fitness_cal(design):
    p, data = objective_func(design)
    return p, data

def parents_variable(parents):
    main_A = mapping(parents[0:interval_main_A], start_main_A, end_main_A)
    main_N = mapping(parents[interval_main_A:interval_main_N], start_main_N, end_main_N)
    s = mapping(parents[interval_main_N:interval_s], start_s, end_s)
    stirrups_A = mapping(parents[interval_s:interval_stirrups_A], start_stirrups_A, end_stirrups_A)
    stirrups_N = mapping(parents[interval_stirrups_A:length_total], start_stirrups_N, end_stirrups_N)
    return main_A, main_N, s, stirrups_A, stirrups_N
   
def generation(parents_matrix, config1, config2):
    population_size, cr, mr = config1
    config2 = config2.copy()
    
    # 計算所有parents的適應值
    P_fitness = []  # p_fitness = [ p1, p2, p3, p4 ....]
    parents_matrix_qualified = []
    data_list = []
    for parents in parents_matrix:
        main_A, main_N, s, stirrups_A, stirrups_N = parents_variable(parents)
        config2['main_bar_no'] = main_A
        config2['main_bar_num'] = main_N
        config2['s'] = s
        config2['stirrups_no'] = stirrups_A
        config2['stirrups_num'] = stirrups_N
        design = config2.copy()
        print(main_A, main_N, stirrups_A, stirrups_N, s)
        p, data = fitness_cal(design)
        if p != 0:
            P_fitness.append(p)
            parents_matrix_qualified.append(parents)
            data_list.append(data)
    
    if len(parents_matrix_qualified) < 2:
        return parents_matrix, P_fitness, parents_matrix_qualified, data_list
     
    # 計算所有parents的相對得分
    P_score = [ P_fitness[i] - min(P_fitness) for i in range(len(parents_matrix_qualified))]
    
    # 計算所有parents的機率
    if sum(P_score) == 0:
        P_score = [1] * len(parents_matrix_qualified)
    probability = [ P_score[i] / sum(P_score) for i in range(len(parents_matrix_qualified)) ]

    # 計算所有parents的累加機率
    cumulation = 0
    cumulation_probability = []  # cumulation_probability = [0.0, 0.42604282962520207,... 0.7091113498911773, 1]
    for i in range(len(parents_matrix_qualified)):
        cumulation += probability[i]
        cumulation_probability.append(cumulation)


    children_matrix = []
    while len(children_matrix) < population_size:
        P_fitness_record = P_fitness.copy() # 若直接賦值P_fitness,則P_fitness_record和P_fitness會指向同一個list，當P_fitness_record被修改時，P_fitness也會被修改。
        parents_matrix_record = parents_matrix_qualified.copy() 
        length = len(parents_matrix_qualified)
        
     
        z1 = random.uniform(0, 1)
        parent1 = 0
        for i in range(0, length-1):
            if z1 >= cumulation_probability[length - 1 - i]:
                parent1 = parents_matrix[length - i]
                P_fitness_record.pop(length - i)
                parents_matrix_record.pop(length - i)
                break
        if parent1 == 0:
            parent1 = parents_matrix[0]
            P_fitness_record.pop(0)
            parents_matrix_record.pop(0)
            
        # 有第二組合格基因時選擇 parent2
        if len(P_fitness_record) != 0:
            length_record = length - 1
            P_score_record = [ P_fitness_record[i] - min(P_fitness_record) for i in range(length_record) ] 
            if sum(P_score_record) == 0:
                P_score_record = [1] * length_record
            probability_record = [ P_score_record[i] / sum(P_score_record) for i in range(length_record) ]
            
            cumulation = 0
            cumulation_probability_record = [] 
            for i in range(length_record):
                cumulation += probability_record[i]
                cumulation_probability_record.append(cumulation)
            
            # 選擇parent2
            z2 = random.uniform(0, 1)
            parent2 = 0
            for i in range(0, length_record-1):
                if z2 >= cumulation_probability_record[length_record - 1 - i]: 
                    parent2 = parents_matrix_record[length_record -1 - i]
                    break
            if parent2 == 0:
                parent2 = parents_matrix_record[0]
        
        # 沒有第二組合格基因的話，則兩組基因皆取同一組
        else:
            parent2 = parent1.copy()
        
        # do crossover or not
        if random.uniform(0, 1) <= cr:
            child1, child2 = crossover(parent1, parent2)
        else:
            child1, child2 = parent1, parent2
            
        # do mutation or not
        if random.uniform(0, 1) <= mr:
            child1 = mutation(child1)
        if random.uniform(0, 1) <= mr:
            child2 = mutation(child2)
        
        # if x1 + y1 <= 4 and x2 + y2 <= 4: (variable relation restriction)
        children_matrix.append(child1)
        children_matrix.append(child2)
    
    return children_matrix, P_fitness, parents_matrix_qualified, data_list

#