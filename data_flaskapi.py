from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "clear_data"
app.config["MONGO_URI"] = "mongodb://34.97.198.241:27017/clear_data"
app.config['JSON_AS_ASCII'] = False
mongo = PyMongo(app)

rents = ['gender', 'landlord', 'phone', 'region', 'rent_type', 'renter', 'situation']


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
    if request.method == 'GET':
        gender = request.args.get('gender', '')
        landlord = request.args.get('landlord', '')
        phone = request.args.get('phone', '')
        region = request.args.get('region', '')
        rent_type = request.args.get('rent_type', '')
        renter = request.args.get('renter', '')
        situation = request.args.get('situation', '')

    else:
        return "Error: No parameter provided. Please specify a parameter."

    Rentinfo = mongo.db.all_info
    output = []

    for ss in Rentinfo.find():
        ss.pop('_id')
        if ss['gender'] == gender:
            if ss['region'] == region:
                output.append(ss)

        elif ss['landlord'] == landlord:
            output.append(ss)
        elif ss['phone'] == phone:
            output.append(ss)

    return jsonify({'result': output})


if __name__ == '__main__':
    app.run(debug=True)
