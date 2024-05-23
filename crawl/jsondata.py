import requests
import json


def get_json_data(freewayid=1, start=0, end=10000):
    res = requests.get('https://1968.freeway.gov.tw/api/getRoadInformation', params={'action': "roadinfo", 'freewayid': freewayid,'from_milepost': start,'end_milepost': end, 'cctv' : True})
    # print(res.json())

    row_data = res.json()
    data = row_data["response"]
    # print(len(data["road_extend"]))
    road = []
    for each_road in data["road_extend"]:
        if each_road["freewayid"] == str(freewayid) and \
            ((start <= each_road["end_milepost"] and each_road["end_milepost"] <= end) or \
             (start <= each_road["from_milepost"] and each_road["from_milepost"] <= end)):
            road.append(each_road)
    for each_cctv in data["cctv"]:
        for each_road in road:
            if each_road["directionid"] == each_cctv["maindirection"]:
                if (each_cctv["mileage"] - each_road["end_milepost"]) * (each_cctv["mileage"] - each_road["from_milepost"]) <= 0:
                    each_cctv["speed"] = each_road["section_average_speed"]
                    break
    
    return data["cctv"]



if __name__ == '__main__':
    data = get_json_data()
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)