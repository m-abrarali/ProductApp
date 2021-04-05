import json
import requests
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('template.html')


@app.route('/healthz/')
def health_check():
    liveliness_check = "I'm alive!"
    return liveliness_check

@app.route('/product-list/')
def product_list():
    """Request Product data from API"""
    try:
        print('Please see complete list of products below')
        api = "https://reqres.in/api/products/"
        response = requests.get(api)
        parsed = json.loads(response.text)
        data = json.dumps(parsed["data"], indent=4, sort_keys=True)
        return data

    except Exception as err:
        print("Unable to retrieve product list.")
        print(type(err))  # the exception error type
        print(err.args)  # arguments stored in .args
        print(err)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True,use_reloader=True)
