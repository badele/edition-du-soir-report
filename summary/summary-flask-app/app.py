import csv, json
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)
data = {}

input = {
    "sum": '/tmp/summary.csv',
    "trend": '/tmp/trend.csv'
}

methods = ['POST', 'GET']

for type in input:
    data[type] = {}
    with open(input[type]) as document:
        reader = csv.reader(document, delimiter=';')
        field = next(document).split(';')
        for row in reader:
            dt = datetime.strptime(row[0], '%Y-%m-%d')
            index = dt.strftime('%Y%m%d')
            bloc = []
            for key, value in enumerate(row):
                bloc.append({field[key]:(value or None)})
            data[type][index] = bloc


# Catalog
@app.route('/options', methods=['GET'])
def map_site():
    output = '<h1>Endpoints</h1><br/>'
    output += ''.join([f'/<b>{x}</b>/ {y}<br/>' for x in data for y in methods])
    output += '---<br/>'
    output += ''.join([f'/<b>{x}/last</b> {y}<br/>' for x in data for y in methods])
    output += '---<br/>'
    output += ''.join(['/<b>{}/[date]</b> {}<br/>'.format(x, y) for x in data for y in methods])
    return output

@app.route('/<type>', methods=methods)
def all_value(type):
    return json.dumps(data[type], sort_keys=True, ensure_ascii=True)

@app.route('/<type>/last', methods=methods)
def last_one(type):
    date = sorted(data[type].keys())[-1]
    return json.dumps(data[type][date], ensure_ascii=True)

@app.route('/<type>/<date>', methods=methods)
def by_date(type, date):
    return json.dumps(data[type][date], ensure_ascii=True)

# Serve basic view from templates folder
@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")

# Handle assets
@app.route('/templates/<file>', methods=['GET'])
def assets(file):
    return render_template(file)

