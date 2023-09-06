from pycsdr.modules import ExecModule
from pycsdr.types import Format
from csdr.module import JsonParser
from owrx.adsb.modes import AirplaneLocation
from owrx.map import Map, Source


class HfdlAirplaneLocation(AirplaneLocation):
    pass


class HfdlSource(Source):
    def __init__(self, flight):
        self.flight = flight

    def getKey(self) -> str:
        return "hfdl:{}".format(self.flight)

    def __dict__(self):
        return {"flight": self.flight}


class DumpHFDLModule(ExecModule):
    def __init__(self):
        super().__init__(
            Format.COMPLEX_FLOAT,
            Format.CHAR,
            [
                "dumphfdl",
                "--iq-file", "-",
                "--sample-format", "CF32",
                "--sample-rate", "12000",
                "--output", "decoded:json:file:path=-",
                "0",
            ],
            flushSize=50000,
        )


class HFDLMessageParser(JsonParser):
    def __init__(self):
        super().__init__("HFDL")

    def process(self, line):
        msg = super().process(line)
        if msg is not None:
            payload = msg["hfdl"]
            if "lpdu" in payload:
                lpdu = payload["lpdu"]
                if lpdu["type"]["id"] in [13, 29]:
                    hfnpdu = lpdu["hfnpdu"]
                    if hfnpdu["type"]["id"] == 209:
                        if "pos" in hfnpdu:
                            pos = hfnpdu['pos']
                            if abs(pos['lat']) <= 90 and abs(pos['lon']) <= 180:
                                Map.getSharedInstance().updateLocation(HfdlSource(hfnpdu["flight_id"]), HfdlAirplaneLocation(pos), "HFDL")
        return msg