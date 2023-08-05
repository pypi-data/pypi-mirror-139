from flask import Flask

from datetime import datetime, date

# from flask.json import JSONEncoder


# class CustomJSONEncoder(JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, (datetime, date)):
#             return obj.isoformat()
#         return super().default(obj)


app = Flask(__name__)
app.config["APPLICATION_ROOT"] = "/api/v1"
# app.json_encoder = CustomJSONEncoder
