import requests
import json
import argparse

# bug: fail when data to 高架路段 會沒有speed
# maindirection: south = 3, north = 4
def get_json_data(freewayid=1, start=0, end=10000, maindirection=4):
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

    data['cctv'] = [d for d in data['cctv'] if d.get("maindirection") == str(maindirection)]
        
    return data["cctv"]



if __name__ == '__main__':
    parser = argparse.ArgumentParser('Get_json_data', add_help=False)
    parser.add_argument('--freewayid', default=1, type=int)
    parser.add_argument('--start', default=0, type=int)
    parser.add_argument('--end', default=10000, type=int)
    parser.add_argument('--direction', default=4, type=int)
    args = parser.parse_args()
    data = get_json_data(args.freewayid, args.start, args.end, args.direction)
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)