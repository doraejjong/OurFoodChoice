from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/list', methods=['GET'])
def show_menus():


    select = request.args.get("select")
    price = request.args.get("price")

    result = []


    shops = list(db.all_shops.find({"select":select}, {'_id': False}))
    for shop in shops:
        for menu in shop["menus"]:
            _price = menu["price"].replace(",","").replace("원","")
            try:
                int(_price)
            except:
                continue

            if int(_price) == 0:
                continue

            elif ["image"] == "":
                pass

            elif int(_price) <= int(price):
                info = {"shop": shop, "menu": menu}


                result.append(info)




    return jsonify({'result': 'success', 'shops_list': result})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)