"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from wechatAutoReplay import app

from flask import request
import hashlib
from .reply import reply,getRequest


@app.route('/wechat', methods=["GET","POST"])
def wechat():
    """wechat page"""
    app.logger.debug("in /wechat")
    # get 方法进来的，处理微信的配置界面有效性校验
    if request.method == "GET":
        signature = request.args.get("signature")
        timestamp = request.args.get("timestamp")
        nonce = request.args.get("nonce")
        echostr = request.args.get("echostr")

        token = "jasonwechat"

        data = [token, timestamp, nonce]
        temp = ''.join(data)

        temp_signature=hashlib.sha1(temp.encode('utf-8')).hexdigest()
        print(signature, temp_signature)
        if signature == temp_signature:
            print(echostr)
            return echostr
        else:
            return echostr
    else:
        return reply()

@app.route('/test', methods=["GET","POST"])
def test():
    """wechat page"""
    app.logger.debug("in /test")
    if request.method == "POST":
        return str(getRequest(request))
    else:
        return "method error"

def del_post(request):
    signature = request.args.get("signature")
    timestamp = request.args.get("timestamp")
    nonce = request.args.get("nonce")
    openid = request.args.get("openid")

    msg_body = request.get_data(as_text=True)
    if not msg_body:
        return "msg is null"
    else:
        return reply(msg_body)