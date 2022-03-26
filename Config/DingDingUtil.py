import json
import time
import requests


class DingDingUtil:
    #自动化回归群的钉钉机器人链接
    #url ="https://oapi.dingtalk.com/robot/send?access_token=aa93717a17a73c21fcf799234f9993ffcd761c17b915ef758a4907cc1d541e38"
    #企金测试部群的钉钉机器人链接
    url ="https://oapi.dingtalk.com/robot/send?access_token=8bdba5ce0bc34777b648f28b841e549108fae03db196a1bca72e3daee0d4e686"
    # url = DingTalkHostEnum.aa.value
    headers = {'Content-Type': 'application/json ;charset=utf-8'}

    def sendMessage(self, message):
        Message = {
            'msgtype': 'text',
            'text': {'content': message},
            'at': {
                # 如果需要@某人，写手机号
                'atMobiles': [''],
                # 如果需要@所有人，写1
                'isAtAll': 0
            }
        }
        Message = json.dumps(Message)
        res = requests.post(url=DingDingUtil.url, headers=DingDingUtil.headers, data=Message)
        print(res.text)

    def sendUrl(self, url, title, message):
        Message = {
            'msgtype': 'link',
            'link': {'messageUrl': url,
                     'picUrl': '',
                     'title': str(time.strftime('%Y-%m-%d', time.localtime(time.time()))) + title,
                     'text': message
                     }
        }
        Message = json.dumps(Message)
        requests.post(url=DingDingUtil.url, headers=DingDingUtil.headers, data=Message)


if __name__ == '__main__':
    # 自动化回归群的钉钉机器人关键字
    # sendMessage =1
    # 企金测试部群的钉钉机器人关键字
    sendMessage = 1
    DingDingUtil().sendMessage(sendMessage)
