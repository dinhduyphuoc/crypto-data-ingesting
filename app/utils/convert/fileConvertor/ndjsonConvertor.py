from app.utils.convert.baseAlgorithm import BaseAlgorithm
from app.utils.convert.algorithm import Algorithm
import json,io,csv


class NDJsonConvertor(BaseAlgorithm):
    def toJson(data):
        try:
            result = []

            for ndjson_line in data.splitlines():
                if not data.strip():
                    continue  # ignore empty lines
                json_line = json.load(io.StringIO(ndjson_line))
                result.append(json_line)
            output = json.dumps(result)
            return Algorithm(output)
        except:
            return Algorithm('')

    def fromJSON(data):
        try:
            result = data
            if type(data) is str:
                result = json.load(io.StringIO(data))

            # output = [json.dumps(record) for record in result]
            ret = io.StringIO()
            cw = csv.writer(ret)
            for key, value in result.items():
                cw.writerow([key, str(value)])
            return ret.read()
        except:
            return ''
