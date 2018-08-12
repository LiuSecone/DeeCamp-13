# -*- coding: utf-8 -*-
import random
from smart_qq_bot.logger import logger
from smart_qq_bot.signals import (
    on_all_message,
    on_group_message,
    on_private_message,
    on_discuss_message,
)
from chatbot_cut.test_anti import  chatbot_port
import urllib
import sys
from googletrans import Translator
sys.path.append('../chatbot_cut/')
# =====唤出插件=====
# 机器人连续回复相同消息时可能会出现
# 服务器响应成功,但实际并没有发送成功的现象
# 所以尝试通过随机后缀来尽量避免这一问题
REPLY_SUFFIX = (
    '~',
    '!',
    '?',
    '||',
)

dict={}
@on_all_message(name='basic[callout]')
def callout(msg, bot):
    if msg.content[0]=='t':
        reply = bot.reply_msg(msg, return_function=True)
        translator = Translator()
        reply_content = translator.translate(msg.content[1:]).text
        reply(reply_content)
    elif msg.content[0]=='r':
        reply = bot.reply_msg(msg, return_function=True)
        translator = Translator()
        reply_content = translator.translate(msg.content[1:],dest='zh-cn').text
        reply(reply_content)
    elif "智障机器人" in msg.content:
        reply = bot.reply_msg(msg, return_function=True)
        logger.info("RUNTIMELOG " + str(msg.from_uin) + " calling me out, trying to reply....")
        reply_content = "干嘛（‘·д·）" + random.choice(REPLY_SUFFIX)
        reply(reply_content)
    elif len(msg.content)>=2 and "!"==msg.content[0] and "!"!=msg.content[1] and msg.content.find('|')!=-1 and len(msg.content[1:msg.content.find('|')])!=0:
        s1=msg.content[1:msg.content.find('|')]
        s2=msg.content[msg.content.find('|')+1:]
        dict[s1]=s2
        reply = bot.reply_msg(msg, return_function=True)
        reply("add!")
    else:
        for term in dict:
            if term in msg.content:
                reply = bot.reply_msg(msg, return_function=True)
                reply(dict[term])
                return
        if("!"==msg.content[0]):
            print("===========-------------=")
            #这一部分原来是调用网页api来自动回复，现在改为调用训练的机器人
            #url_str = "http://api.qingyunke.com/api.php?key=free&appid=0&msg={key}".format(
            #    key=urllib.parse.quote(msg.content[1:])
            #)
            #page = urllib.request.urlopen(url_str)
            #html = page.read()
            #html=html.decode('utf-8')
            #tmp=html.find("}")
            #while(html[tmp+1:].find("}")!=-1):
            #    tmp+= html[tmp+1:].find("}")+1
            #st=html[html.find("content")+10:tmp-1]
            st=chatbot_port(user_text=msg.content[1:])
            print(st)
            reply = bot.reply_msg(msg, return_function=True)
            reply(st)



# =====复读插件=====
class Recorder(object):
    def __init__(self):
        self.msg_list = list()
        self.last_reply = ""

recorder = Recorder()


@on_group_message(name='basic[repeat]')
def repeat(msg, bot):
    global recorder
    reply = bot.reply_msg(msg, return_function=True)

    if len(recorder.msg_list) > 0 and recorder.msg_list[-1].content == msg.content and recorder.last_reply != msg.content:
        if str(msg.content).strip() not in ("", " ", "[图片]", "[表情]"):
            logger.info("RUNTIMELOG " + str(msg.group_code) + " repeating, trying to reply " + str(msg.content))
            reply(msg.content)
            recorder.last_reply = msg.content
    recorder.msg_list.append(msg)


@on_group_message(name='basic[三个问题]')
def nick_call(msg, bot):
    if "我是谁" == msg.content:
        bot.reply_msg(msg, "你是{}({})!".format(msg.src_sender_card or msg.src_sender_name, msg.src_sender_id))

    elif "我在哪" == msg.content:
        bot.reply_msg(msg, "你在{name}({id})!".format(name=msg.src_group_name, id=msg.src_group_id))

    elif msg.content in ("我在干什么", "我在做什么"):
        bot.reply_msg(msg, "你在调戏我!!")


@on_discuss_message(name='basic[讨论组三个问题]')
def discuss_three_questions(msg, bot):
    if "我是谁" == msg.content:
        bot.reply_msg(msg, "你是{}!".format(msg.src_sender_name))

    elif "我在哪" == msg.content:
        bot.reply_msg(msg, "你在{name}!".format(name=msg.src_discuss_name))

    elif msg.content in ("我在干什么", "我在做什么"):
        bot.reply_msg(msg, "你在调戏我!!")