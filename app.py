from flask import Flask, request, jsonify, url_for
import requests
from opencage.geocoder import OpenCageGeocode
import os

app = Flask(__name__)

def get_coordinates(place_name):
    geocoder = OpenCageGeocode("55ca49d87f7f4a48b8b5fd3311485161")
    results = geocoder.geocode(place_name)
    if results and len(results):
        return (results[0]['geometry']['lat'], results[0]['geometry']['lng'])
    else:
        return None

@app.route('/phone_location', methods=['GET'])
def get_phone_location():
    phone_number = request.args.get('phone_number')
    API_KEY = '87a87dbc1a7b67052f8a3a4d7e1ca4f7'
    # Construct URL using url_for
    url = url_for('validate_number', _external=True, access_key=API_KEY, number=phone_number)
    response = requests.get(url)
    data = response.json()
    if data['valid']:
        location = data['location']
        co = get_coordinates(location)
        return jsonify({'phone_location': co}), 200
    else:
        return jsonify({'error': 'Invalid phone number'}), 400

@app.route('/validate_number')
def validate_number():
    access_key = request.args.get('access_key')
    number = request.args.get('number')
    url = f'http://apilayer.net/api/validate?access_key={access_key}&number={number}&country_code=&format=1'
    response = requests.get(url)
    return response.json()

if __name__ == '__main__':
    app.run()
