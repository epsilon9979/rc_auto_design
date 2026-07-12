from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from operation import main

app = Flask(__name__, template_folder=".")

@app.route("/")
def index():
    return render_template("rc_auto.html")

@app.route('/echo', methods=['GET'])
def echo():
    # --- 1. 接收前端網頁傳來的參數 ---
    ln = request.args.get('ln', default=208.661, type=float)
    beam_type = request.args.get('type', default='middle', type=str) # 避免使用內建關鍵字 type
    bw = request.args.get('bw', default=20.669, type=float)
    H = request.args.get('H', default=23.622, type=float)
    hf = request.args.get('hf', default=7.0866, type=float)
    Mu_plus = request.args.get('Mu_plus', default=217.972, type=float)
    Mu_minus = request.args.get('Mu_minus', default=272.056, type=float)
    Vu = request.args.get('Vu', default=60.678, type=float)
    Tu = request.args.get('Tu', default=32.776, type=float)
    beff = request.args.get('beff', default=72.834, type=float)
    cc = request.args.get('cc', default=5/2.54, type=float)
    fc = request.args.get('fc', default=5, type=float)
    fy = request.args.get('fy', default=60, type=float)
    iteration_loop = request.args.get('iteration_loop', default=20, type=int)
    
    # 將接收到的資料打包，準備回傳給前端確認
    received_params = {
        "ln": ln, "type": beam_type, "bw": bw, "H": H, "hf": hf,
        "Mu_plus": Mu_plus, "Mu_minus": Mu_minus, "Vu": Vu, "Tu": Tu,
        "beff": beff, "cc": cc, "fc": fc, "fy": fy
    }
    
    # --- 2. 執行 GA 演算法模型 ---
    # 修正原本重複宣告變數的問題
    main_A, main_N, s, stirrups_A, stirrups_N, reinforcement_usage, d1, d2, sw, distance, Mn_plus, Mn_minus, Vn, Tn = main(
        ln, beam_type, bw, H, hf, Mu_plus, Mu_minus, Vu, Tu, beff, cc, fc, fy, iteration_loop
    )
    
    # --- 3. 回傳 JSON 結果給網頁前端 ---
    return jsonify({
        "message": "GA 演算法計算完成", 
        "received": received_params,  # 讓前端確認收到了什麼
        "result": {                   # GA 演算法算出來的設計成果
            "main_reinforcement_area": main_A,
            "main_reinforcement_count": main_N,
            "stirrups_spacing": s,
            "stirrups_area": stirrups_A,
            "stirrups_count": stirrups_N,
            "reinforcement_usage": -reinforcement_usage,
            "d1": d1,
            "d2": d2,
            "sw": sw,
            "distance": distance,
            "nominal_moment_plus": Mn_plus,
            "nominal_moment_minus": Mn_minus,
            "nominal_shear": Vn,
            "nominal_torsion": Tn
        }
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True) # 開啟 debug=True 方便開發時除錯