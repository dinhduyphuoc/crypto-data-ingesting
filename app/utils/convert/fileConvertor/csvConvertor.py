from app.utils.convert.baseAlgorithm import BaseAlgorithm
from app.utils.convert.algorithm import Algorithm
import csv,json,io

class CsvConvertor(BaseAlgorithm):
    def toJson(data):
        try:
            reader = csv.DictReader(io.StringIO(data))
            output = json.dumps(list(reader))
            return Algorithm(output)
        except:
            return Algorithm('')

    def fromJSON(data):
        try:
            result = data
            if type(data) is str:
                result = json.load(io.StringIO(data))

            output = [json.dumps(record) for record in result]
            output = '\n'.join(output)

            return output
        except:
            return ''