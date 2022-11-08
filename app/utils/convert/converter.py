from utils.convert.fileConvertor.csvConvertor import CsvConvertor
from utils.convert.fileConvertor.ndjsonConvertor import NDJsonConvertor



class Convertor:
    def convertFrom(type,data):
        match type:
            case 'Csv': return CsvConvertor.toJson(data)
            case 'NDJson': return NDJsonConvertor.toJson(data)
