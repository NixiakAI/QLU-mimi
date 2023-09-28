import json, time, requests, random
def daka(token):
    getline = "https://admin.report.mestallion.com/api/mini/sport/getline"
    map = "https://admin.report.mestallion.com/api/mini/sport/today"
    daka = "https://admin.report.mestallion.com/api/mini/sport/daka"

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
        "Content-Type": "application/x-www-form-urlencoded",
        "Token": token,
        "Referer": "https://servicewechat.com/wx5069fcccc8151ce3/28/page-frame.html",
    }
    getdata = {
        "lat": "36.55358",
        "lng": "116.75199"
    }
    reqgetline = requests.post(url=getline, headers=header, data=getdata)
    jsondata = json.loads(reqgetline.text)

    if jsondata['code'] == 200:
        print("获取线路成功")
    elif jsondata['code'] == 500:
        print('已经获取过路线了')

    frequent = requests.post(url=map, headers=header)
    #计算打卡点个数
    count_frequent = str(frequent.json()).count('point_name')
    # 获取每个打卡点的经纬度和id值
    parsed_data = json.loads(frequent.text)

    points = parsed_data['data']['line']['lines']
    lngs,lats,ids = [],[],[]
    for point in points:
        lngs.append(point['lng'])
        lats.append(point['lat'])
        ids.append(point['id'])

    #打卡业务代码
    for i in range(count_frequent):
        data = {
            "ble": "false",
            "gps": "false",
            "lat": lats[i],
            "lng": lngs[i],
            "bs_id": "",
            "bs_name": "",
            "id": ids[i],
        }
        requests.post(url=daka, headers=header, data=data)
        # 极限8分钟打卡
        time.sleep(270 + random.randint(1, 35))

#This put your token
token = '**********************'
daka(token)
