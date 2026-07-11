from step import STEPS

class check_space(STEPS):
    def process(self, data, info, design):
        # design = {'Mu+': k-ft, 'Mu-': k-ft, 'Vu': kips, 'Tu': k-ft, 'type': 'middle', 'ln': feet, 'beff': inch, 'bw': inch, 'H': inch, 'hf': inch, 'cc': inch, 'fc': ksi, 'fy': ksi, 'main_bar_num': n, 'main_bar_no': n, 's': inch, 'stirrups_num': n, 'stirrups_no': n}
        # data = {'distance': inch, 'd1': inch, 'd2': inch, 'Aoh': inch^2, 'Ph': inch, 'Ao': inch^2, 'Acp': inch^2, 'Pcp': inch, 'vc': lbf, 'percent_of_torsional_stirrups': float, 'Al': inch^2, 'B1': float, 'B1': float, 'Mpr_plus': k-ft, 'Mpr_minus': k-ft, 'Vs': kips}

        result = 1
        bw, main_bar_no, main_bar_num, stirrups_no, stirrups_num, fy, cc, fc, s = design['bw'], design['main_bar_no'], design['main_bar_num'], design['stirrups_no'], design['stirrups_num'], design['fy'], design['cc'], design['fc'], design['s']
        distance, Vs, d2 = data['distance'], data['Vs'], data['d2']
        
        # check main bars' space
        sw = ( bw - distance * 2) / ( main_bar_num/2 - 1 )
        data['sw'] = sw
        
        if Vs*1000 > 4 * (fc*1000)**0.5 * bw * d2:
            if sw > min( (600 / fy - 2.5 * cc), (480 / fy), (d2 / 2), 12 ):
                return 0, data
        else:
            if sw > min( (600 / fy - 2.5 * cc), (480 / fy), d2, 24 ):
                return 0, data
                
        if main_bar_num/2 == stirrups_num:
            if sw > 14:
                return 0, data
        else:
            if sw - info.D(main_bar_no) > 6:
                return 0, data
                
        if sw < info.D(main_bar_no):
            return 0, data
               
        # check stirrups' space along length
        if fy == 60:
            if s > min( d2/4, 6 * info.D(main_bar_no), 6 ):
                return 0, data
        elif fy == 80:
            if s > min( d2/4, 5 * info.D(main_bar_no), 6 ):
                return 0, data
                
        if s - info.D(stirrups_no) < 1:
            return 0, data
        
        return result, data