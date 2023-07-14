import os
from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch, RequestsHttpConnection

app = Flask(__name__)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Create Elasticsearch client
es = Elasticsearch(
    hosts=[f"{os.getenv('ELASTICSEARCH_SCHEMA')}://{os.getenv('ELASTICSEARCH_USERNAME')}:{os.getenv('ELASTICSEARCH_PASS')}@{os.getenv('ELASTICSEARCH_HOST')}:{os.getenv('ELASTICSEARCH_PORT')}"],
    verify_certs=False,
    connection_class=RequestsHttpConnection
)

# Create Elasticsearch index
try:
    if not es.indices.exists(index='cities'):
        es.indices.create(index='cities')
except Exception as e:
    print(f"Error creating Elasticsearch index: {str(e)}")

# Health endpoint
@app.route('/health')
def health():
    if es.ping():
        return 'OK', 200  # Return 200 OK status if Elasticsearch is reachable
    else:
        return 'Elasticsearch is not reachable', 500  # Return 500 Internal Server Error status if Elasticsearch is not reachable

# Insert a city and its population
@app.route('/city', methods=['POST'])
def insert_city():
    data = request.get_json()
    city = data.get('city')
    population = data.get('population')

    doc = {
        'city': city,
        'population': population
    }

    res = es.index(index='cities', doc_type='_doc', body=doc)

    return jsonify(res)

# Update a city and its population
@app.route('/city', methods=['PUT'])
def update_city():
    data = request.get_json()
    city = data.get('city')
    population = data.get('population')

    doc = {
        'doc': {
            'population': population
        }
    }

    res = es.update(index='cities', doc_type='_doc', id=city, body=doc)

    return jsonify(res)

# Delete a city and its population
@app.route('/city', methods=['DELETE'])
def delete_city():
    data = request.get_json()
    city = data.get('city')

    res = es.delete(index='cities', id=city)

    return jsonify(res)

# Retrieve the population of a city
@app.route('/city', methods=['GET'])
def get_population():
    data = request.get_json()
    city = data.get('city')
    
    res = es.get(index='cities', id=city)

    return jsonify(res)

# Main execution
if __name__ == '__main__':
    app.run(host=os.getenv('FLASK_RUN_HOST', 'localhost'), port=os.getenv('FLASK_RUN_PORT', 5000))
