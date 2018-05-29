from flask import Flask, jsonify, request
from kryptobot.hydra import Hydra

app = Flask(__name__)
hydra = Hydra()


@app.route('/launch_strategy', methods=['POST'])
def launch_strategy():
    strategy = request.json["strategy"]
    params = request.json["params"]
    hydra.run_strategy(strategy, params)
    return jsonify(result='success')


@app.route('/launch_harvester', methods=['POST'])
def launch_harvester():
    harvester = request.json["harvester"]
    params = request.json["params"]
    hydra.run_harvester(harvester, params)
    return jsonify(result='success')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
