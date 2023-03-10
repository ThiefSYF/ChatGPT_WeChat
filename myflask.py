import hashlib
from flask import Flask, request, make_response, render_template
from wechatpy import parse_message, create_reply
import wechatpy
import urllib
import time
import pickle
import os

from gptManage import gptSessionManage,gptMessageManage
 
app = Flask(__name__)
app.debug = True

##############################openai基础设置##########################
tokens = ['Bearer sk-XXX1','Bearer sk-XXX2']
max_tokens = 250
model = 'gpt-3.5-turbo'
temperature = 0.8
rsize = 200 # 设置每条消息的回复长度，超过长度将被分割
##############################wechat基础设置##########################
wechattoken = 'wechattoken'


msgsmanag = gptMessageManage(tokens,max_tokens,model,temperature,rsize)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route('/wechat/', methods=['GET', 'POST']) 
def wechat():

    global reply
    global msgsmanag
    global wechattoken
    if request.method == 'GET':
        token = wechattoken# 设置 wechat token
        data = request.args
        signature = data.get('signature', '')
        timestamp = data.get('timestamp', '')
        nonce = data.get('nonce', '')
        echostr = data.get('echostr', '')
        s = sorted([timestamp, nonce, token])
        s = ''.join(s)
        if hashlib.sha1(s.encode('utf-8')).hexdigest() == signature:
            response = make_response(echostr)
            return response
    else:
        msg = parse_message(request.get_data())
        if msg.type == 'text':
            #如果msg包含sensitive_data中的词，则不回复:
            if any(word in msg.content for word in sensitive_data):
                reply = create_reply("警告：包含敏感词！", message=msg)
            else:
                rtext = msgsmanag.get_response(msg,int(time.time()))
                reply = create_reply(str(rtext).strip(), message=msg)#创建消息
        if msg.type == 'image':
            rtext = '你发送了一张图片'
            reply = create_reply(rtext, message=msg)#创建消息
        return reply.render()#回复消息

if __name__ == '__main__':
    #使用OS读取txt文件内容，以换行符为分界存为一个列表
    current_path = os.path.dirname(__file__)
    with open(current_path+"/sensitive_words_lines.txt", 'r', encoding='utf-8') as f:
        sensitive_data = f.readlines()
    print(sensitive_data[5])
    app.run( host = '0.0.0.0',port=80)