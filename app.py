import json,random,re,time,jsonpath,requests,urllib3
from flask import Flask, render_template, request
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('daka.html')

@app.route('/run_program', methods=['POST'])
def run_program():
    input_content = request.form['input_content']
    token = input_content
    if len(token) == 32:
        daka(token)
        return "打卡完成！"
    else:
        return "输入有误，重新再试！"

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
    # 提交协议头信息，获取全部路线数据信息
    reqgetline = requests.post(url=getline, headers=header, data=getdata)
    jsondata = json.loads(reqgetline.text)
    getcode = jsonpath.jsonpath(jsondata, '$[code]')
    if 200 in getcode:
        print("获取线路成功")
        print(f"页面响应信息:{reqgetline.text}")
    elif 500 in getcode:
        print("获取线路失败")
        print(f"页面响应信息:{reqgetline.text}")
    reqmap = requests.post(url=map, headers=header)
    lngs = re.findall(',"lng":(.{1,12}?),"total_distence":', reqmap.text)
    lats = re.findall(',"lat":(.{9,12}?)}', reqmap.text)
    ids = re.findall(',"id":(.{1,12}?),"lat":', reqmap.text)
    print(lngs, lats, ids)

    for i in range(3):
        data = {
            "ble": "false",
            "gps": "false",
            "lat": lats[i],
            "lng": lngs[i],
            "bs_id": "",
            "bs_name": "",
            "id": ids[i]
        }
        reqdaka = requests.post(url=daka, headers=header, data=data)
        jsondata = json.loads(reqdaka.text)
        code = jsonpath.jsonpath(jsondata, '$[code]')
        # 极限8分钟打卡
        if 200 in code:
            print(f"第{i + 1}次打卡成功")
            print(f"页面响应信息:{reqdaka.text}")
        elif 500 in code:
            print(f"第{i + 1}次打卡失败")
            print(f"页面响应信息:{reqdaka.text}")
        time.sleep(270 + random.randint(1, 35))

if __name__ == '__main__':
    app.run()



