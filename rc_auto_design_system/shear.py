from step import STEPS
import sympy

class check_shear(STEPS):
    def process(self, data, info, design): 
        # design = {'Mu+': k-ft, 'Mu-': k-ft, 'Vu': kips, 'Tu': k-ft, 'type': 'middle', 'ln': feet, 'beff': inch, 'bw': inch, 'H': inch, 'hf': inch, 'cc': inch, 'fc': ksi, 'fy': ksi, 'main_bar_num': n, 'main_bar_no': n, 's': inch, 'stirrups_num': n, 'stirrups_no': n}
        # data = {'distance': inch, 'd1': inch, 'd2': inch, 'Aoh': inch^2, 'Ph': inch, 'Ao': inch^2, 'Acp': inch^2, 'Pcp': inch, 'vc': lbf, 'percent_of_torsinal_stirrups': float, 'Al': inch^2, 'B1': inch, 'Mpr_plus': k-ft, 'Mpr_minus': k-ft}
        result = 1
        ln, Vu, fy, s, stirrups_no, stirrups_num = design['ln'], design['Vu'], design['fy'], design['s'], design['stirrups_no'], design['stirrups_num']
        Mpr_plus, Mpr_minus, d2, percentage = data['Mpr_plus'], data['Mpr_minus'], data['d2'], data['percent_of_torsional_stirrups']
        Ve = (Mpr_plus + Mpr_minus) / (ln) 
        Vu = Ve + Vu # in Kips
        
        c = sympy.symbols('c')
        Vs = c * fy * d2 / s
        Av = info.get_c(Vs, Vu/0.75) 
        if ( Av + percentage * 2 * info.A(stirrups_no) ) > info.A(stirrups_no) * stirrups_num:
            result = 0
        Vs = Av * fy * d2 / s    
        
        data["Vs"] = Vs
        data["Vn"] = Vs
        data["stirrups_usage"] = ( Av + percentage * 2 * info.A(stirrups_no) ) / (info.A(stirrups_no) * stirrups_num)
        
        return result, data 