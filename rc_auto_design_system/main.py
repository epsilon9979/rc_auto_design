from information import information
from step import STEPexception
from size import check_size
from torsion import check_torsion
from moment import check_moment
from shear import check_shear
from amount import check_amount
from space import check_space

def engineer(design): 
    # design = {'Mu+': k-ft, 'Mu-': k-ft, 'Vu': kips, 'Tu': k-ft, 'type': 'middle', 'ln': feet, 'beff': inch, 'bw': inch, 'H': inch, 'hf': inch, 'cc': inch, 'fc': ksi, 'fy': ksi, 'main_bar_num': n, 'main_bar_no': n, 's': inch, 'stirrups_num': n, 'stirrups_no': n}
    
    steps = [
        check_size(), # 0
        check_torsion(), # 1
        check_moment(), # 2
        check_shear(), # 3
        check_amount(), # 4
        check_space(), # 5
    ] 
    
    info = information()
    data = {}
    for step in steps:
        try:
            result, data = step.process(data, info, design)  #執行每一個步驟的程式功能
            if result == 0:
                print(f'step failed at {steps.index(step)}')
                return 0, data
        except STEPexception as e:
            print('exception happened', e)
            return 0, data
    return 1, data


# design={
#     'Mu+': 217.992,
#     'Mu-': 272.056,
#     'Vu': 60.678,
#     'Tu': 32.776,
#     'type': 'middle',
#     'ln': 208.661,
#     'beff': 72.834,
#     'bw': 20.669,
#     'H': 23.622,
#     'hf': 7.0866,
#     'cc': 5/2.54,
#     'fc': 5,
#     'fy': 60,
#     'main_bar_num': 8,
#     'main_bar_no': 9,
#     'stirrups_num': 4,
#     'stirrups_no': 4,
#     's': 4
# }    
# result, data = engineer(design)
# print(result)
# print(data)
