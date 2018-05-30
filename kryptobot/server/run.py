from flask import Flask, jsonify, request
from kryptobot.portfolio.manager import Manager

app = Flask(__name__)
manager = Manager()


@app.route('/launch_strategy', methods=['POST'])
def launch_strategy():
    strategy = request.json["strategy"]
    params = request.json["params"]
    manager.run_strategy(strategy, params)
    return jsonify(result='success')


@app.route('/launch_harvester', methods=['POST'])
def launch_harvester():
    harvester = request.json["harvester"]
    params = request.json["params"]
    manager.run_harvester(harvester, params)
    return jsonify(result='success')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
