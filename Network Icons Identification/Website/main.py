from flask import Flask, request, render_template, flash, url_for, redirect
from networkType import identify_network_type
from callType import identify_call_service
from networkStrength import identify_network_strength

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template('index.html')

@app.route('/updateicons', methods=['GET', 'POST'])
def updateicons():
    if request.method == 'GET':
        # page for user to upload screenshot to be cropped
        return render_template('updateIconsUpload.html')
    elif request.method == 'POST':
        # save uploaded file to static folder
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        else:
            print("done")
            file.save('static/uploadScreenshot.png')
        callServiceIconPresent = request.form.get('callServiceIconPresent') != None
        print(callServiceIconPresent)
        return render_template('updateIconsCoordinates.html', callServiceIconPresent = callServiceIconPresent)
    
@app.route('/checknetwork', methods=['GET', 'POST'])
def checknetwork():
    if request.method == 'GET':
        # page for user to upload screenshot to be checked
        return render_template('checkNetworkUpload.html')
    elif request.method == 'POST':
        # save uploaded file to static folder
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        else:
            print("done")
            file.save('static/uploadScreenshot.png')
        # get coordinates of icons from cookies
        networkIconCoordinates = request.cookies.get('networkIconCoordinates').split(',')
        networkType = identify_network_type('static/uploadScreenshot.png', [int(networkIconCoordinates[1]), int(networkIconCoordinates[3]), int(networkIconCoordinates[0]), int(networkIconCoordinates[2])])
        networkStrengthIconCoordinates = request.cookies.get('networkStrengthIconCoordinates').split(',')
        networkStrength = identify_network_strength('static/uploadScreenshot.png', [int(networkStrengthIconCoordinates[1]), int(networkStrengthIconCoordinates[3]), int(networkStrengthIconCoordinates[0]), int(networkStrengthIconCoordinates[2])])
        callServiceIconCoordinates = request.cookies.get('callServiceIconCoordinates').split(',')
        if callServiceIconCoordinates == ['']:
            callServiceType = False
        else:
            callServiceType = identify_call_service('static/uploadScreenshot.png', [int(callServiceIconCoordinates[1]), int(callServiceIconCoordinates[3]), int(callServiceIconCoordinates[0]), int(callServiceIconCoordinates[2])])
        return render_template("checkNetworkResults.html", networkType=networkType, callServiceType=callServiceType, networkStrength=networkStrength)

if __name__ == '__main__':
    # Secret key required for cookies
    app.secret_key = 'super secret key'
    app.run(debug=True)