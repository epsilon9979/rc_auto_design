from step import STEPS

class check_size(STEPS):
    def process(self, data, info, design): 
        # design = {'Mu+': k-ft, 'Mu-': k-ft, 'Vu': kips, 'Tu': k-ft, 'type': 'middle', 'ln': feet, 'beff': inch, 'bw': inch, 'H': inch, 'hf': inch, 'cc': inch, 'fc': ksi, 'fy': ksi, 'main_bar_num': n, 'main_bar_no': n, 's': inch, 'stirrups_num': n, 'stirrups_no': n}
        # data = []
        result = 1
        bw, H, cc, stirrups_no, main_bar_no, fc, Vu, Tu, hf, type, ln = design['bw'], design['H'], design['cc'], design['stirrups_no'], design['main_bar_no'], design['fc'], design['Vu'], design['Tu'], design['hf'], design['type'], design['ln']
        
        # configuration variables
        num_wing = info.type(type) # 幾側有樓板
        distance = cc + info.D(stirrups_no) * 3 - (2 * info.D(stirrups_no) - info.D(main_bar_no) / 2)
        d1 = distance # cc + info.D(stirrups_no) + info.D(main_bar_no)/2   # 4.1605
        d2 = H - distance #H - cc - info.D(stirrups_no) - info.D(main_bar_no)/2   # 20.5895
        Aoh = (d2 - d1) * (bw - cc*2 - info.D(stirrups_no)*2 - info.D(main_bar_no))
        Ph = 2 * ( (d2 - d1) + (bw - cc*2 - info.D(stirrups_no)*2 - info.D(main_bar_no)) )
        Ao = 0.85 * Aoh
        Acp = bw * H + num_wing * hf * min(H-hf, 4*hf)
        Pcp = 2 * (H + bw + num_wing*min(H-hf, 4*hf))
        vc = 2*(fc*1000)**0.5*bw*d2
        data = {'distance': distance, 'd1': d1, 'd2': d2, 'Aoh': Aoh, 'Ph': Ph, 'Ao': Ao, 'Acp': Acp, 'Pcp': Pcp, 'vc': vc}
        
        # check size
        if H > 0.25 * ln:
            return 0, data
        
        if bw < min(0.3*H, 10):
            return 0, data
        
        if (vc + 8*(fc*1000)**0.5*bw*d2) < Vu / 0.75:
            return 0, data
        
        if ( (Vu*1000/bw/d2)**2 + (Tu*12000*Ph/1.7/Aoh**2)**2 )**0.5 > 0.75 * (vc/bw/d2 + 8*(fc*1000)**0.5):
            return 0, data
        
        return result, data