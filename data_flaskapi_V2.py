from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "clear_data"
app.config["MONGO_URI"] = "mongodb://34.97.198.241:27017/clear_data"
app.config['JSON_AS_ASCII'] = False
mongo = PyMongo(app)

rents = ['gender', 'landlord', 'phone', 'region', 'rent_type', 'renter', 'situation']

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/Rentinfo/all', methods=['GET'])  # viewing all contents of rentList
def get_all_Rentinfo():
    Rentinfo = mongo.db.all_info
    output = []
    for j in Rentinfo.find():
        j.pop('_id')  # json序列化
        output.append(j)
    return jsonify({'result': output})


@app.route('/Rentinfo', methods=['GET'])
def Rentinfo_result():
    query_parameters = request.args
    req_params = {}

    gender = query_parameters.get('gender')
    landlord = query_parameters.get('landlord')
    # phone = query_parameters.get('phone')
    region = query_parameters.get('region')
    rent_type = query_parameters.get('rent_type')
    renter = query_parameters.get('renter')
    situation = query_parameters.get('situation')


    if gender:
        req_params['gender'] = gender
    if landlord:
        req_params['landlord'] = landlord
    if region:
        req_params['region'] = region
    if rent_type:
        req_params['rent_type'] = rent_type
    if renter:
        req_params['renter'] = renter
    if situation:
        req_params['situation'] = situation
    if not (gender or landlord or region or rent_type or renter or situation):
        return  page_not_found(404)

    Rentinfo = mongo.db.all_info
    output = []
    keys = list(req_params.keys())
    kk = len(keys)

    for ss in Rentinfo.find():
        ss.pop('_id')
        kn = 0
        for param in req_params.keys():
            if ss[param] == req_params[param]:  #資料庫 == user查詢
                kn += 1
        if kn == kk:
            output.append(ss)


    return jsonify({'req_params':req_params,'result': output})


if __name__ == '__main__':
    app.run(debug=True)
