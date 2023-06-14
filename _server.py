from flask import Flask, request
import json
import time
from dotenv import load_dotenv
import os
from exts.BybitHook.instances_manager import InstancesManager

app = Flask(__name__)
instancesManager = InstancesManager()

def response(status):
    status_code = {
        200: 'OK',
        400: 'Bad Request',
        403: 'Forbidden',
        500: 'Internal Server Error'
    }
    return app.response_class(
        response=json.dumps({'status': status_code[status]}),
        status=status,
        mimetype='application/json'
    )


def append_timestamp(timestamp, strategy_name):
    dumped = False
    while not dumped:
        try:
            with open('timestamps.json', 'r+') as f:
                try:
                    timestamps = json.load(f)
                except Exception:
                    timestamps = {}
                if strategy_name not in timestamps.keys():
                    timestamps[strategy_name] = []
                timestamps[strategy_name].append(timestamp)
                f.seek(0)
                f.truncate()
                json.dump(timestamps, f)
                dumped = True
        except Exception:
            try:
                with open('timestamps.json', 'w+') as nf:
                    json.dump(timestamps, nf)
            except Exception:
                pass


def get_timestamp(strategy_name):
    try:
        with open('timestamps.json', 'r+') as f:
            timestamps = json.load(f)
            lines = timestamps[strategy_name]
            last_line = lines[-1]
            if len(lines) >= 10:
                # Array of timestamps is full, remove all timestamps
                timestamps[strategy_name] = []
                f.seek(0)
                f.truncate()
                json.dump(timestamps, f)

            return last_line
    except Exception:
        return '0'


@app.route('/')
def index():
    return open('index.html', 'r').read()


@app.route('/stra', methods=['POST'])
async def order():
    load_dotenv()
    try:
        position = json.loads(request.data)['Position']
        token = json.loads(request.data)['Token']
        if token != os.getenv('PRIVATE_TOKEN'):
            return response(403)
        straname = json.loads(request.data)['Strategy']
        # Loads config.json

        with open('config.json', 'r') as f:
            config = json.load(f)
        if straname not in config.keys():
            return response(400)

        api_key = config[straname]['API_KEY']
        api_secret = config[straname]['API_SECRET']
        if api_key is None or api_secret is None:
            return response(400)
    except KeyError:
        return response(400)
    try:
        currentTimestamp = str(time.time())
        currentInstance = instancesManager.getInstance(straname)
        await currentInstance.refresh_telegram()
        if position == 'long':
            await currentInstance.close_order()
            await currentInstance.place_order('Buy')
        elif position == 'short':
            await currentInstance.close_order()
            await currentInstance.place_order('Sell')
        elif position == 'flat' and (float(currentTimestamp) - float(get_timestamp(straname))) > 30:
            await currentInstance.close_order()
        append_timestamp(currentTimestamp, straname)
        return response(200)
    except Exception as e:
        print(e)
        return response(500)
