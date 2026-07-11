from step import STEPS
import sympy

class check_torsion(STEPS):
    def process(self, data, info, design): 
        # design = {'Mu+': k-ft, 'Mu-': k-ft, 'Vu': kips, 'Tu': k-ft, 'type': 'middle', 'ln': feet, 'beff': inch, 'bw': inch, 'H': inch, 'hf': inch, 'cc': inch, 'fc': ksi, 'fy': ksi, 'main_bar_num': n, 'main_bar_no': n, 's': inch, 'stirrups_num': n, 'stirrups_no': n}
        # data = {'distance': inch, 'd1': inch, 'd2': inch, 'Aoh': inch^2, 'Ph': inch, 'Ao': inch^2, 'Acp': inch^2, 'Pcp': inch, 'vc': lbf}
        result = 1
        Ao, Ph, Acp, Pcp, bw = data['Ao'], data['Ph'], data['Acp'], data['Pcp'], design['bw']
        stirrups_no, Tu, fc, fy, s = design['stirrups_no'], design['Tu'], design['fc'], design['fy'], design['s']

        # 計算扭矩所需之「剪力筋面積比例」和「主筋面積」
        Tcr = 4 * (fc*1000)**0.5 * Acp**2 / Pcp / 1000
        c = sympy.symbols('c')
        Tn1 = 2 * Ao * info.A(stirrups_no) * fy * c / s
        percent_of_torsional_stirrups = info.get_c(Tn1, min(Tcr, Tu*12)/0.75) #0.4275
        
        Tn2 = 2 * Ao * c * fy / Ph
        Al1 = info.get_c(Tn2, min(Tcr, Tu*12)/0.75) #1.4
        
        Al2 = min( (5 * (fc*1000)**0.5 * Acp / (fy*1000) - info.A(stirrups_no) / s * Ph * fy / fy) , (5 * (fc*1000)**0.5 * Acp / (fy*1000) - 25 * bw / (fy*1000) * Ph * fy / fy) )
        Al = max(Al1, Al2)
        Tn = min( (2 * Ao * info.A(stirrups_no) * fy * percent_of_torsional_stirrups / s), 2 * Ao * Al * fy / Ph)
        
        data['Tn'] = Tn/12
        data['percent_of_torsional_stirrups'] = percent_of_torsional_stirrups
        data['Al'] = Al
        
        return result, data