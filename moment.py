from step import STEPS
import sympy

class check_moment(STEPS):
    def process(self, data, info, design): 
        # design = {'Mu+': k-ft, 'Mu-': k-ft, 'Vu': kips, 'Tu': k-ft, 'type': 'middle', 'ln': feet, 'beff': inch, 'bw': inch, 'H': inch, 'hf': inch, 'cc': inch, 'fc': ksi, 'fy': ksi, 'main_bar_num': n, 'main_bar_no': n, 's': inch, 'stirrups_num': n, 'stirrups_no': n}
        # data = {'distance': inch, 'd1': inch, 'd2': inch, 'Aoh': inch^2, 'Ph': inch, 'Ao': inch^2, 'Acp': inch^2, 'Pcp': inch, 'vc': lbf, 'percent_of_torsinal_stirrups': float, 'Al': inch^2}
        fc, fy, beff, bw, main_bar_no, main_bar_num, Mu_plus, Mu_minus, H = design['fc'], design['fy'], design['beff'], design['bw'], design['main_bar_no'], design['main_bar_num'], design['Mu+'], design['Mu-'], design['H']
        Al, d1, d2 = data['Al'], data['d1'], data['d2']
        result = 1
        B1 = 0.85 - 0.05*(fc - 4) 
        data['B1'] = B1
        
        c = sympy.symbols('c')
        def cal_c(b, n, A, fyy, d=d1):
            cc = -0.85 * fc * B1 * b * c 
            fs1 = 29000 * (-0.003 + 0.003 * d / c) * n * A
            fs2 = fyy * n * A
            C = info.get_c(cc + fs1 + fs2, 0)
            
            if -0.003 + 0.003 / C * d > fy / 29000:
                cc = -0.85 * fc * B1 * b * c 
                fs1 = fyy * n * A
                return [info.get_c(cc + fs1 + fs2, 0), 1]
            
            elif -0.003 + 0.003 / C * d < -fy / 29000:
                cc = -0.85 * fc * B1 * b * c 
                fs1 = -fyy * n * A
                return [info.get_c(cc + fs1 + fs2, 0), -1]
            
            else:
                return [C, 0]
        
        def cal_mn(d1, d2, cc, C, F1, F2):
            mn = (F2 * d2) + (F1 * d1) + (cc * C * B1 / 2)
            return mn
        
        # check Mu+
        C, mode = cal_c(beff, main_bar_num/2, info.A(main_bar_no) - Al/main_bar_num, fy)
        cc = -0.85 * fc * B1 * beff * C
        if mode == 0:
            F1 = 29000 * (-0.003 + 0.003 * d1 / C) * main_bar_num/2 * ( info.A(main_bar_no) - Al/main_bar_num )
            F2 = fy * main_bar_num/2 * ( info.A(main_bar_no) - Al/main_bar_num )
            Mn_plus = cal_mn(d1, d2, cc, C, F1, F2)
        elif mode == 1:
            F1 = fy * main_bar_num/2 * ( info.A(main_bar_no) - Al/main_bar_num )
            F2 = fy * main_bar_num/2 * ( info.A(main_bar_no) - Al/main_bar_num )
            Mn_plus = cal_mn(d1, d2, cc, C, F1, F2)
        elif mode == -1:
            F1 = -fy * main_bar_num/2 * ( info.A(main_bar_no) - Al/main_bar_num )
            F2 = fy * main_bar_num/2 * ( info.A(main_bar_no) - Al/main_bar_num )
            Mn_plus = cal_mn(d1, d2, cc, C, F1, F2)
        if Mn_plus / 12 < Mu_plus / 0.9: # Mn is in Kips-inch
            return 0, data
        data['Mn+'] = Mn_plus / 12
        
        # check Mu-   
        C, mode = cal_c(bw, main_bar_num/2, info.A(main_bar_no) - Al/main_bar_num, fy, H-d2)
        if mode == 0:
            F1 = 29000 * (-0.003 + 0.003 * d1 / C) * main_bar_num/2 * ( info.A(main_bar_no) - Al/main_bar_num )
            F2 = fy * main_bar_num/2 * ( info.A(main_bar_no) - Al/main_bar_num )
            Mn_minus = cal_mn(H-d2, H-d1, cc, C, F1, F2) # cal_mn(d1, d2, cc, C, F1, F2)
        elif mode == 1:
            F1 = fy * main_bar_num/2 * ( info.A(main_bar_no) - Al/main_bar_num )
            F2 = fy * main_bar_num/2 * ( info.A(main_bar_no) - Al/main_bar_num )
            Mn_minus = cal_mn(H-d2, H-d1, cc, C, F1, F2)
        elif mode == -1:
            F1 = -fy * main_bar_num/2 * ( info.A(main_bar_no) - Al/main_bar_num )
            F2 = fy * main_bar_num/2 * ( info.A(main_bar_no) - Al/main_bar_num )
            Mn_minus = cal_mn(H-d2, H-d1, cc, C, F1, F2)
        if Mn_minus / 12 < Mu_minus / 0.9: # Mn is in Kips-inch
            return 0, data
        data['Mn-'] = Mn_minus / 12
        
        # 順便先計算 Mpr 
        # 計算 Mpr+
        C, mode = cal_c(beff, main_bar_num/2, info.A(main_bar_no), fy*1.25)
        cc = -0.85 * fc * B1 * beff * C
        if mode == 0:
            F1 = 29000 * (-0.003 + 0.003 * d1 / C) * main_bar_num/2 * info.A(main_bar_no) - Al/main_bar_num
            F2 = fy*1.25 * main_bar_num/2 * info.A(main_bar_no)
            Mpr_plus = cal_mn(d1, d2, cc, C, F1, F2)
        elif mode == 1:
            F1 = fy*1.25 * main_bar_num/2 * info.A(main_bar_no)
            F2 = fy*1.25 * main_bar_num/2 * info.A(main_bar_no)
            Mpr_plus = cal_mn(d1, d2, cc, C, F1, F2)
        elif mode == -1:
            F1 = -fy*1.25 * main_bar_num/2 * info.A(main_bar_no)
            F2 = fy*1.25 * main_bar_num/2 * info.A(main_bar_no)
            Mpr_plus = cal_mn(d1, d2, cc, C, F1, F2)
        data['Mpr_plus'] = Mpr_plus / 12
        
        # 計算 Mpr-
        C, mode = cal_c(bw, main_bar_num/2, info.A(main_bar_no), fy*1.25, H-d2)
        cc = -0.85 * fc * B1 * bw * C
        if mode == 0:
            F1 = 29000 * (-0.003 + 0.003 * (H-d2) / C) * main_bar_num/2 * info.A(main_bar_no)
            F2 = fy*1.25 * main_bar_num/2 * info.A(main_bar_no)
            Mpr_minus = cal_mn(H-d2, H-d1, cc, C, F1, F2)
        elif mode == 1:
            F1 = fy*1.25 * main_bar_num/2 * info.A(main_bar_no)
            F2 = fy*1.25 * main_bar_num/2 * info.A(main_bar_no)
            Mpr_minus = cal_mn(H-d2, H-d1, cc, C, F1, F2)
        elif mode == -1:
            F1 = -fy*1.25 * main_bar_num/2 * info.A(main_bar_no)
            F2 = fy*1.25 * main_bar_num/2 * info.A(main_bar_no)
            Mpr_minus = cal_mn(H-d2, H-d1, cc, C, F1, F2)
        data['Mpr_minus'] = Mpr_minus / 12
        
        
        return result, data