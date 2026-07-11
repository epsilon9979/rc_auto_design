from step import STEPS

class check_amount(STEPS):
    def process(self, data, info, design):
        # design = {'Mu+': k-ft, 'Mu-': k-ft, 'Vu': kips, 'Tu': k-ft, 'type': 'middle', 'ln': feet, 'beff': inch, 'bw': inch, 'H': inch, 'hf': inch, 'cc': inch, 'fc': ksi, 'fy': ksi, 'main_bar_num': n, 'main_bar_no': n, 's': inch, 'stirrups_num': n, 'stirrups_no': n}
        # data = {'distance': inch, 'd1': inch, 'd2': inch, 'Aoh': inch^2, 'Ph': inch, 'Ao': inch^2, 'Acp': inch^2, 'Pcp': inch, 'vc': lbf, 'percent_of_torsional_stirrups': float, 'Al': inch^2, 'B1': float, 'B1': float, 'Mpr_plus': k-ft, 'Mpr_minus': k-ft, 'Vs': kips}
        result = 1
        fc, bw, fy, s, stirrups_no, stirrups_num, main_bar_no, main_bar_num = design['fc'], design['bw'], design['fy'], design['s'], design['stirrups_no'], design['stirrups_num'], design['main_bar_no'], design['main_bar_num']
        d2, Al, Acp, Ph = data['d2'], data['Al'], data['Acp'], data['Ph']
        
        # check Av,min
        if info.A(stirrups_no) * stirrups_num / s < max( 0.75 * (fc*1000)**0.5 * bw / (fy*1000), 50 * bw / (fy*1000) ):
            return 0, data

        # check As,min
        if info.A(main_bar_no) * main_bar_num < max(3 * (fc*1000)**0.5 / (fy*1000) * bw * d2, 200 / (fy*1000) * bw * d2):
            return 0, data
        
        # check As,max
        if info.A(main_bar_no) * main_bar_num > 0.025 * bw * d2:
            return 0, data
        
        # check Al,min
        if Al < min( (5 * (fc*1000)**0.5 * Acp / (fy*1000) - info.A(stirrups_no) / s * Ph * fy / fy) , (5 * (fc*1000)**0.5 * Acp / (fy*1000) - 25 * bw / (fy*1000) * Ph * fy / fy) ):
            return 0, data
            
        # check stirrups' size
        if info.D(stirrups_no) < max(0.042 * s, 0.375):
            print("check stirrups' size")
            return 0, data
        
        # check main bar placement
        if main_bar_num%2 == 1:
            print("violation:", main_bar_num)
            return 0, data
        
        # check stirrups' placement
        if main_bar_num/2 >= 2 * stirrups_num:
            return 0, data
        
        if stirrups_num > main_bar_num/2:
            return 0, data
        
        return result, data