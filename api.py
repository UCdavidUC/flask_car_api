import flask
from flask import request, jsonify
from azure.cosmos import exceptions, CosmosClient, PartitionKey
from decouple import config

endpoint = config('DB_ENDPOINT')
key = config('DB_KEY')

client = CosmosClient(str(endpoint), str(key))

database_name = 'datadog-db'
database = client.create_database_if_not_exists(id=database_name)

container_name = 'datadog-container'
container = database.create_container_if_not_exists(
    id=container_name,
    partition_key=PartitionKey('/state'),
    offer_throughput=400
)

app = flask.Flask(__name__)
app.config['DEBUG'] = True

@app.route('/cars/', methods = ['GET'])
def get_all():
    return jsonify()

@app.route('/car')
def get_id():
    if 'id' in request.args:
        if 'state' in request.args:
            id = request.args['id']
            state = request.args['state']
            item_response = container.read_item(item=id, partition_key=state)
            request_charge = container.client_connection.last_response_headers['x-ms-request-charge']
            print(item_response['id'])
    else:
        return "Error. No id field provided."

app.run()
