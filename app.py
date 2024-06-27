from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

COINGECKO_API_URL = "https://api.coingecko.com/api/v3"

@app.route('/api/top10', methods=['GET'])
def get_top10():
    response = requests.get(f"{COINGECKO_API_URL}/coins/markets", params={
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 10,
        'page': 1
    })
    data = response.json()
    top10 = [{
        'id': coin['id'],
        'symbol': coin['symbol'],
        'name': coin['name'],
        'price': coin['current_price'],
        'market_cap': coin['market_cap'],
        'total_supply': coin['total_supply'],
        'circulating_supply': coin['circulating_supply']
    } for coin in data]
    return jsonify({'top10': top10})

@app.route('/api/search', methods=['GET'])
def search_coin():
    query = request.args.get('query')
    response = requests.get(f"{COINGECKO_API_URL}/coins/markets", params={
        'vs_currency': 'usd',
        'ids': query
    })
    data = response.json()
    if len(data) > 0:
        coin = data[0]
        result = {
            'id': coin['id'],
            'symbol': coin['symbol'],
            'name': coin['name'],
            'price': coin['current_price'],
            'market_cap': coin['market_cap'],
            'total_supply': coin['total_supply'],
            'circulating_supply': coin['circulating_supply']
        }
        return jsonify(result)
    else:
        return jsonify({'error': 'Coin not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

