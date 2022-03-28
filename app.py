#
# Simple CSV based CRUD web app
#

# packages
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import csv
import json

# create web app's instance
app = Flask('__name__')

# Homepage
@app.route('/')
def readhome():

    return render_template('home.html')

# create new CSV entry
@app.route('/kota/<id>/create', methods=['GET', 'POST'])
def create(id):
    kota = ('id-kota_' + str(id) + '.csv')
    # HTTP GET method
    if request.method == 'GET':
        # get CSV fields from string query paramater
        fields = json.loads(request.args.get('fields').replace("'", '"'))

        # render HTML page dynamically
        return render_template('entry.html', fields=fields)

    # HTTP GET method
    elif request.method == 'POST':
        # extract new CSV entry from submitted form
        data = dict(request.form)

        # upodate the CSV file
        with open(kota, 'a') as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            writer.writerow(data)

        # return to READ data page (to see the updated data)
        return redirect('/kota/' + id)

# read data from CSV
@app.route('/kota/<id>')
def read(id):
    # variable to hold CSV data
    data = []
    kota = ('id-kota_' + str(id) + '.csv')
    # read data from CSV file
    with open(kota) as f:
        # create CSV dictionary reader instance
        reader = csv.DictReader(f)

        # init CSV dataset
        [data.append(dict(row)) for row in reader]

    # render HTML page dynamically
    return render_template('index.html', data=data, list=list, len=len, str=str, id=id)

# update existing CSV row
@app.route('/kota/<id>/update', methods=['GET', 'POST'])
def update(id):
    kota = ('id-kota_' + str(id) + '.csv')
    # HTTP GET method
    if request.method == 'GET':
        # updated data
        data = []

        # open CSV file
        with open(kota) as rf:
            # create CSV dictionary reader
            reader = csv.DictReader(rf)

            # init CSV rows
            [data.append(dict(row)) for row in reader]

            return render_template('edit.html', fields=data[int(request.args.get('id'))])

    # HTTP POST method
    elif request.method == 'POST':
        # updated data
        data = []

        # open CSV file
        with open(kota) as rf:
            # create CSV dictionary reader
            reader = csv.DictReader(rf)

            # init CSV rows
            [data.append(dict(row)) for row in reader]

        # updated row
        row = {}

        for key, val in dict(request.form).items():
            if key != 'Id':
                row[key] = val

        # update CSV row
        data[int(request.form.get('Id'))] = row

        # write update CSV file
        with open(kota, 'w') as wf:
            # create CSV dictionary writer
            writer = csv.DictWriter(wf, fieldnames=data[0].keys())

            # write CSV column names
            writer.writeheader()

            # write CSV rows
            writer.writerows(data)

        return redirect('/kota/' + id)

# delete row from CSV file
@app.route('/kota/kota/<idkota>/delete')
def delete(idkota):
    kota = ('id-kota_' + str(idkota) + '.csv')
    # open CSV file
    with open(kota) as rf:
        # updated data
        data = []

        # load data
        temp_data = []

        # create CSV dictionary reader
        reader = csv.DictReader(rf)

        # init CSV rows
        [temp_data.append(dict(row)) for row in reader]

        # create mew dataset but without a row to delete
        [
            data.append(temp_data[row])
            for row in range(0, len(temp_data))
            if row != int(request.args.get('id'))
        ]

        # update the CSV file
        with open(kota, 'w') as wf:
            # create CSV dictionary writer
            writer = csv.DictWriter(wf, fieldnames=data[0].keys())

            # write CSV column names
            writer.writeheader()

            # write CSV rows
            writer.writerows(data)

    # return to READ data page (to see the updated data)
    return redirect('/kota/' + idkota)

# run HTTP server
if __name__ == '__main__':
    app.run(debug=True, threaded=True)
