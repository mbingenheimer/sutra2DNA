from flask import render_template, url_for, flash, redirect, session, request, make_response, jsonify
from codingwebsite import app
from codingwebsite.forms import HammingInput
from codingwebsite.hamming import encode, decode, binStringFromBitArr
from bitarray import bitarray

@app.route('/', methods = ['GET', 'POST'])
def home():
	form = HammingInput()
	session['errors'] = 'FALSE'
	if form.validate_on_submit():
		session['formMessage'] = request.form['message']
		return redirect(url_for('hammingEncoded'))
	
	if request.method == 'POST':
		session["errors"] = 'TRUE'
	return render_template('home.html', form=form)

@app.route("/hammingCode")
def hammingCode():
	message = request.args.get("message")

	myBytes = message.encode("utf-8")

	data = bitarray(bin(int(myBytes.hex(), base=16))[2:])
	code = binStringFromBitArr(encode(data))

	response = make_response(
                jsonify(
                    {"code": code}
                ),
                200,
            )
	response.headers["Content-Type"] = "application/json"
	return response

@app.route("/hammingDecode")
def hammingDecode():

	code = request.args.get("code")

	message = ""
	finalMessage= ""
	try:
		message = binStringFromBitArr(decode(bitarray(code)))
		finalMessage = bytes.fromhex(hex(int(message, 2))[2:]).decode()
	except ValueError as e:
		if str(e) == "Two errors detected.":
			finalMessage = "I can detect upto, but not correct, two errors."

	response = make_response(
                jsonify(
                    {"message": finalMessage}
                ),
                200,
            )
	response.headers["Content-Type"] = "application/json"
	return response