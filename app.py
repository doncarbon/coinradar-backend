# Import necessary modules from Flask, Flask-CORS, and requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# Define the base URL for the CoinGecko API
COINGECKO_API_URL = "https://api.coingecko.com/api/v3"

# Define a route to get the top 10 cryptocurrencies by market cap
@app.route('/api/top10', methods=['GET'])
def get_top10():
    # Send a GET request to the CoinGecko API to get the top 10 coins
    response = requests.get(f"{COINGECKO_API_URL}/coins/markets", params={
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 10,
        'page': 1
    })

    # Parse the JSON response from the API
    data = response.json()

    # Extract the relevant information for the top 10 coins
    top10 = [{
        'id': coin['id'],
        'symbol': coin['symbol'],
        'name': coin['name'],
        'price': coin['current_price'],
        'market_cap': coin['market_cap'],
        'total_supply': coin['total_supply'],
        'circulating_supply': coin['circulating_supply']
    } for coin in data]

    # Return the extracted data as a JSON response
    return jsonify({'top10': top10})

# Define a route to search for a specific cryptocurrency by its ID
@app.route('/api/search', methods=['GET'])
def search_coin():
    # Get the query parameter from the request
    query = request.args.get('query')

    # Send a GET request to the CoinGecko API to search for the coin
    response = requests.get(f"{COINGECKO_API_URL}/coins/markets", params={
        'vs_currency': 'usd',
        'ids': query
    })

    # Parse the JSON response from the API
    data = response.json()

    # Check if the API returned any results
    if len(data) > 0:
        # Extract the relevant information for the found coin
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

        # Return the extracted data as a JSON response
        return jsonify(result)
    else:
        # Return an error response if the coin was not found
        return jsonify({'error': 'Coin not found'}), 404

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

