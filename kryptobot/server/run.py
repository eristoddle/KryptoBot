from flask import Flask, jsonify, request
from kryptobot.portfolio.manager import Manager

app = Flask(__name__)
manager = Manager()

# NOTE: This is more an example of how to build a rest server
# rather than a module to import


@app.route('/launch_strategy', methods=['POST'])
def launch_strategy():
    params = request.json["params"]
    manager.run_strategy(params)
    return jsonify(result='success')


@app.route('/launch_harvester', methods=['POST'])
def launch_harvester():
    params = request.json["params"]
    manager.run_harvester(params)
    return jsonify(result='success')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
