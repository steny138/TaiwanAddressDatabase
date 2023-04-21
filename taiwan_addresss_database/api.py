import os
import requests
import json
from urllib import parse
import xml.etree.ElementTree as et
from dotenv import load_dotenv


load_dotenv()


class TGOS(object):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
    }
    form = {
        "oAPPId": os.getenv("TGOSQueryAddraAppId"),
        "oAPIKey": os.getenv("TGOSQueryAddrAPIKey"),
        "oResultDataType": "JSON",
    }

    def get_counties(self):
        data = parse.urlencode(self.form)
        url = "https://addr.tgos.tw/addrws/v40/GetAddrList.asmx/GetCountyList"
        r = requests.post(url=url, headers=self.headers, data=data)
        return self.__parse_xml(r.text)

    def get_towns(self, county):
        form = dict(self.form)
        form.update(oCountyName=county)

        data = parse.urlencode(form)
        url = "https://addr.tgos.tw/addrws/v40/GetAddrList.asmx/GetTownList"
        r = requests.post(url=url, headers=self.headers, data=data)

        return self.__parse_xml(r.text)

    def get_roads(self, county, town):
        form = dict(self.form)
        form.update(oCountyName=county, oTownName=town)

        data = parse.urlencode(form)
        url = "https://addr.tgos.tw/addrws/v40/GetAddrList.asmx/GetRoadList"
        r = requests.post(url=url, headers=self.headers, data=data)

        return self.__parse_xml(r.text)

    def get_lanes(self, county, town, road):
        form = dict(self.form)
        form.update(oCountyName=county, oTownName=town, oRoadName=road)

        data = parse.urlencode(form)
        url = "https://addr.tgos.tw/addrws/v40/GetAddrList.asmx/GetLaneList"
        r = requests.post(url=url, headers=self.headers, data=data)

        return self.__parse_xml(r.text)

    def get_alleies(self, county, town, road, lane=""):
        form = dict(self.form)
        form.update(oCountyName=county, oTownName=town, oRoadName=road, oLane=lane)

        data = parse.urlencode(form)
        url = "https://addr.tgos.tw/addrws/v40/GetAddrList.asmx/GetAlleyList"
        r = requests.post(url=url, headers=self.headers, data=data)
        return self.__parse_xml(r.text)

    def get_no_lists(self, county, town, road, lane="", alley=""):
        form = dict(self.form)
        form.update(
            oCountyName=county,
            oTownName=town,
            oRoadName=road,
            oIsShowCodeBase="true",
            oLane=lane,
            oAlley=alley,
        )

        data = parse.urlencode(form)
        url = "https://addr.tgos.tw/addrws/v40/GetAddrList.asmx/GetNoList"
        r = requests.post(url=url, headers=self.headers, data=data)
        return self.__parse_xml(r.text)

    def __parse_xml(self, content):
        root = et.fromstring(content)
        json_str = root.text

        return json.loads(json_str)


if __name__ == "__main__":
    tgos = TGOS()
    # result = tgos.get_counties()
    # result = tgos.get_towns("新北市")
    # result = tgos.get_roads("新北市", "林口區")
    # result = tgos.get_lanes("新北市", "林口區", "文化一路一段")
    # result = tgos.get_alleies("新北市", "林口區", "文化一路一段", "100巷")
    result = tgos.get_no_lists("新北市", "林口區", "文化一路一段", "100巷", "10弄")
    print(result)
