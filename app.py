import flask
from flask import Flask, request, jsonify
from azure.cosmos import exceptions, CosmosClient, PartitionKey
from decouple import config

app = Flask(__name__)

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

@app.route('/car', methods=['GET'])
def get_id():
    if 'id' in request.args:
        if 'state' in request.args:
            id = request.args['id']
            state = request.args['state']
            query = "SELECT * FROM c WHERE c.id='" + str(id) + "' AND c.state='" + str(state) + "'"
            print(query)
            items = container.query_items(query=query)
            item_list = []
            for item in items:
                item_list.append(item)
            return jsonify(item_list)
        else:
            return 'Error. No state field provided.'
    else:
        return "Error. No id field provided."

if __name__ == '__main__':
    app.run()
