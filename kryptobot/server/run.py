from flask import Flask, jsonify, request
from ..hydra import Hydra

app = Flask(__name__)
hydra = Hydra()


@app.route('/launch_strategy', methods=['POST'])
def launch_strategy():
    strategy = request.json["strategy"]
    params = request.json["params"]
    result = hydra.run_strategy(strategy, params)
    return jsonify(result=result)


@app.route('/launch_harvester', methods=['POST'])
def launch_harvester():
    harvester = request.json["harvester"]
    params = request.json["params"]
    result = hydra.run_harvester(harvester, params)
    return jsonify(result=result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
