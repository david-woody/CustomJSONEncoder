import calendar
from datetime import datetime
from json import JSONEncoder

from flask import Flask, jsonify


class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                if obj.utcoffset() is not None:
                    obj = obj - obj.utcoffset()
                millis = int(
                    calendar.timegm(obj.timetuple()) * 1000 +
                    obj.microsecond / 1000
                )
                return millis
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder

@app.route('/')
def hello_world():
    now = datetime.now()
    return jsonify({'now': now})




if __name__ == '__main__':
    app.run(debug=True)
