from flask import render_template, url_for, flash, redirect, session, request, make_response, jsonify
from codingwebsite import app
from codingwebsite.forms import HammingInput
from codingwebsite.hamming import encode, decode, binStringFromBitArr
import unireedsolomon as rs
from bitarray import bitarray

@app.route('/')
def home():
	return render_template('home.html')

@app.route("/reedsolomon")
def reedsolomon():

	return render_template("reedsolomon.html")

@app.route("/hammingCode")
def hammingCode():
	message = request.args.get("message")

	myBytes = message.encode("utf-8")

	data = bitarray(bin(int(myBytes.hex(), base=16))[2:]) #complicated way of getting bits from unicode text
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

@app.route("/rsCode")
def rsCode():
	message = request.args.get("message")
	noErrors = request.args.get("noErrors")
	coder = rs.RSCoder(len(message) + int(noErrors),len(message))

	encodedText = coder.encode(message)

	myBytes = encodedText.encode("utf-8")


	data = bitarray(bin(int(myBytes.hex(), base=16))[2:])
	code = binStringFromBitArr(data)

	response = make_response(
                jsonify(
                    {"code": code}
                ),
                200,
            )
	response.headers["Content-Type"] = "application/json"
	return response

@app.route("/rsDecode")
def rsDeocde():
	code = request.args.get("code")
	noErrors = request.args.get("noErrors")
	messageLength = request.args.get("messageLength")
	coder = rs.RSCoder(int(messageLength) + int(noErrors), int(messageLength))

	message = ""
	finalMessage= ""
	try:
		#message = binStringFromBitArr(decode(bitarray(code)))
		message = bytes.fromhex(hex(int(code, 2))[2:]).decode()
		finalMessage = coder.decode(message)[0]
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