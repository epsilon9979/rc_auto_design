from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from operation import main
from procedure import parents_variable
import time

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

# --- 1. 原本的資料收集迴圈 ---
usage_counter = Counter()
data_list = {}

start = time.time()

for i in range(30):
    print(f"in {i} round")
    main_A, main_N, s, stirrups_A, stirrups_N, reinforcement_usage, d1, d2, sw, distance, Mn_plus, Mn_minus, Vn, Tn = main(ln, type, bw, H, hf, Mu_plus, Mu_minus, Vu, Tu, beff, cc, fc, fy)
    
    para = (main_A, main_N, stirrups_A, stirrups_N, s)
    usage_counter[para] += 1

end = time.time()

# --- 2. 統計數據計算 ---
# 取得所有種類出現的次數
counts = list(usage_counter.values())

# 計算平均數和標準差
mean_val = np.mean(counts)
std_val = np.std(counts)

print("===== 統計結果 =====")
print(f"總共開出 {len(usage_counter)} 種不同的結果組合")
print(f"各種類出現次數的 平均數 (Mean): {mean_val:.2f}")
print(f"各種類出現次數的 標準差 (Standard Deviation): {std_val:.2f}")
print("time cost:", end - start)
print("====================")

# --- 3. 繪製直方圖 (Bar Chart) ---
# 將 tuple 標籤簡化，方便在圖表上顯示
labels = [f"({p[0]},{p[1]},{p[2]},{p[3]},{p[4]})" for p in usage_counter.keys()]

plt.figure(figsize=(12, 6))  # 設定圖表寬高
bars = plt.bar(labels, counts, color='skyblue', edgecolor='black', alpha=0.8)

# 在長條圖上方顯示具體數字
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.1, int(yval), ha='center', va='bottom')

# 加上平均數的輔助虛線
plt.axhline(mean_val, color='red', linestyle='--', linewidth=1.5, label=f'Mean ({mean_val:.2f})')

# 調整圖表細節
plt.title("Distribution of Output Parameters (30 Runs)", fontsize=14, fontweight='bold')
plt.xlabel("Parameters Combination (main_A, main_N, s, stirrups_A, stirrups_N)", fontsize=10)
plt.ylabel("Appearance Count (Times)", fontsize=12)
plt.xticks(rotation=45, ha='right', fontsize=9)  # 將標籤旋轉 45 度避免重疊
plt.grid(axis='y', linestyle=':', alpha=0.6)     # 加上水平網格線
plt.legend()                                      # 顯示圖例

plt.tight_layout()  # 自動調整邊距防止標籤被切到
plt.show()          # 顯示圖表