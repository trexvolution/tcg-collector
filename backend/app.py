import os 
from flask import Flask, jsonify, request 
from flask_cors import CORS 
 
app = Flask(__name__) 
CORS(app) 
 
# ===================================================================== 
# DILARANG MENGUBAH ATAU MENG-HARDCODE BAGIAN INI! 
# ===================================================================== 
nama_owner = os.environ.get('NAMA_PRAKTIKAN', 'Misterius') 
nim_owner = os.environ.get('NIM_PRAKTIKAN', '00000000') 
 
# ===================================================================== 
# TEMA: TRADING CARD GAME (TCG)
# ===================================================================== 
katalog_data = { 
    "judul_katalog": f"TCG Master Deck: {nama_owner}", 
    "pemilik": nama_owner, 
    "nim": nim_owner, 
    "items": ["Blue-Eyes White Dragon", "Dark Magician", "Black Lotus"] 
} 
 
@app.route('/api/info', methods=['GET']) 
def get_info(): 
    return jsonify(katalog_data) 
 
@app.route('/api/add-item', methods=['POST']) 
def add_item(): 
    new_item = request.json.get('item') 
    if new_item: 
        katalog_data["items"].append(new_item) 
        return jsonify({"message": "Kartu baru telah ditambahkan ke Deck!", "items": 
katalog_data["items"]}), 201 
    return jsonify({"error": "Data tidak valid"}), 400 
 
if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=5000)
    
# az container create --resource-group PraktikumCloud1-RG --name api-tcg --image abdillah11/tp1-backend-api:v1 --dns-name-label TCG-Master-Deck --ports 5000 --os-type Linux --cpu 1 --memory 1.5 