import json
import unittest 
import datetime

with open("./data-1.json","r") as f:
    jsonData1 = json.load(f)
with open("./data-2.json","r") as f:
    jsonData2 = json.load(f)
with open("./data-result.json","r") as f:
    jsonExpectedResult = json.load(f)


def convertFromFormat1 (jsonObject):
    return{
        "deviceID": jsonObject["deviceID"],
        "deviceType": jsonObject["deviceType"],
        "timestamp":jsonObject["timestamp"],
        "location": jsonObject["location"],
        "status": jsonObject["operationStatus"],
        "temperature": jsonObject["temp"]
    }


def convertFromFormat2 (jsonObject):
    timestamp_ms = int(datetime.datetime.strptime(jsonObject["timestamp"], '%Y-%m-%dT%H:%M:%S.%fZ').timestamp() * 1000)
    location= f"{jsonObject['country']}/{jsonObject['city']}/{jsonObject['area']}/{jsonObject['factory']}"
    return{
        "deviceID": jsonObject["device"]["id"],
        "deviceType": jsonObject["device"]["type"],
        "timestamp": timestamp_ms,
        "location": location,
        "status": jsonObject["data"]["status"],
        "temperature": jsonObject["data"]["temperature"]
        
    }


def main (jsonObject):

    result = {}

    if (jsonObject.get('device') is None):
        result = convertFromFormat1(jsonObject)
    else:
        result = convertFromFormat2(jsonObject)

    return result


class TestSolution(unittest.TestCase):

    def test_sanity(self):

        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(
            result,
            jsonExpectedResult
        )

    def test_dataType1(self):

        result = main (jsonData1)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 1 failed'
        )

    def test_dataType2(self):

        result = main (jsonData2)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 2 failed'
        )

if __name__ == '__main__':
    unittest.main()
