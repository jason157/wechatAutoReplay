#coding=utf-8
import xmltodict
import json
import elasticsearch
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import parse_message
from wechatpy.replies import TextReply
from wechatAutoReplay import app



def reply(msg_xml):
    '''
    按微信XML格式相应
    '''
    print(msg_xml)
    msg_dict = xmltodict.parse(msg_xml, encoding='utf8')
    print( msg_dict)
    msg_dict = msg_dict['xml']
    to_user_name = msg_dict["ToUserName"]
    from_user_name = msg_dict["FromUserName"]
    create_time = msg_dict["CreateTime"]
    msg_type = msg_dict["MsgType"]
    content = msg_dict["Content"]
    msg_id = msg_dict["MsgId"]
    if msg_type == 'text':
        print("---------------------",content,msg_id)
        es_client = es_login()
        result = searchDataFromES(es_client, "linux_database", content)
        print(result)
        return findAnwser(content)
    print(msg_dict)
    return msg_xml

def getRequest(request):
    '''
    获取到微信传输的请求，并解析
    '''
    if request.method == "GET":
        signature = request.args.get("signature")
        timestamp = request.args.get("timestamp")
        nonce = request.args.get("nonce")
        echostr = request.args.get("echostr")

        token = "jasonwechat"
        try:
            app.logger.debug("check_signature success")
            check_signature(token,signature,timestamps,nonce)
        except InvalidSignatureException:
            app.logger.debug("signature error")
            return "signature error"
    if request.method == "POST": # 处理POST请求
        contentType = request.headers.get("Content-Type")  #
        if contentType != "text/xml":  #确认消息头的content type是xml的
            app.logger.debug(str(contentType))
            rt_msg = "conten type error"
            reply = TextReply(content=rt_msg)
            xml = reply.render()
            return xml
        #正常解析body
        data = request.get_data()
        app.logger.debug(str(data))
        try:
            data = str(data, encoding = 'cp1252')
            msg = parse_message(data) #尝试解析消息体
            app.logger.debug(str(msg))
        except Exception:
            app.logger.error(str("pars data error"))
            reply = TextReply(content="消息解析失败")
            xml = reply.render()
            return xml
        print(msg)
        
        if msg.type == "text":
            result = findAnwser(msg.content)
            reply = TextReply(content=result)
            xml = reply.render()
            return xml
        else:
            reply = TextReply(content="你输入的格式不支持")
            xml = reply.render()
            return xml


def findAnwser(content):
    '''
    再数据库中查找到答案，并返回
    '''

    return content

es_host = "localhost"
es_port = "9288"

def es_login(host="localhost", port="9288"): 
    """连接es""" 
    return elasticsearch.Elasticsearch(hosts=[{"host": host, "port": port}])

def searchDataFromES(es_client, index, querystr,field="_all"):
     datas = {
        "query": {
            "match": {
                "ostype": querystr
                }
            }
        }
     result = es_client.search(index=index, body=datas)
     return json.dumps(result)
