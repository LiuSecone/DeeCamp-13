# coding: utf-8
import re
from smart_qq_bot.handler import (
    list_handlers,
    list_active_handlers,
    activate,
    inactivate,
)
from smart_qq_bot.logger import logger
from smart_qq_bot.signals import on_all_message, on_bot_inited, on_private_message
from chatbot_cut.test_anti import  chatbot_port
import urllib
import sys
sys.path.append('../chatbot_cut/')
cmd_hello = re.compile(r"!hello")
cmd_hello2 = re.compile(r"智超")
cmd_list_plugin = re.compile(r"!list_plugin")
cmd_inactivate = re.compile(r"!inactivate \{(.*?)\}")
cmd_activate = re.compile(r"!activate \{(.*?)\}")
dict={}
def do_activate(text):
    result = re.findall(cmd_activate, text)
    if result:
        activate(result[0])
        return "Function [%s] activated successfully" % result[0]


def do_inactivate(text):
    re.findall(cmd_inactivate, text)
    result = re.findall(cmd_inactivate, text)
    if result:
        inactivate(result[0])
        return "Function [%s] inactivated successfully" % result[0]


def do_hello(text):
    if re.match(cmd_hello, text):
        return "大头沙皮!"
    if "智超" in text:
        return "优秀！"
    if "智障机器人" in text:
        reply_content = "干嘛（‘·д·）"
        return reply_content
    elif len(text)>=2 and "!"==text[0] and "!"!=text[1] and text.find('|')!=-1 and len(text[1:text.find('|')])!=0:
        s1=text[1:text.find('|')]
        s2=text[text.find('|')+1:]
        dict[s1]=s2
        return "add!"
    else:
        for term in dict:
            if term in text:
                return dict[term]
        if("!"==text[0]):
            print("===========-------------=")
            #这一部分原来是调用网页api来自动回复，现在改为调用训练的机器人
            #url_str = "http://api.qingyunke.com/api.php?key=free&appid=0&msg={key}".format(
            #    key=urllib.parse.quote(text[1:])
            #)
            #page = urllib.request.urlopen(url_str)
            #html = page.read()
            #html=html.decode('utf-8')
            #tmp=html.find("}")
            #while(html[tmp+1:].find("}")!=-1):
            #    tmp+= html[tmp+1:].find("}")+1
            #st=html[html.find("content")+10:tmp-1]
            st=chatbot_port(user_text=text[1:])
            print(st)
            return st

def do_list_plugin(text):
    if re.match(cmd_list_plugin, text):
        text = "All: %s\n\nActive: %s" % (
            ", ".join(list(list_handlers())), ", ".join(list(list_active_handlers()))
        )
        return text

@on_bot_inited("PluginManager")
def manager_init(bot):
    logger.info("Plugin Manager is available now:)")


@on_all_message(name="PluginManger[hello]")
def hello_bot(msg, bot):
    result = do_hello(msg.content)
    if result is not None:
        return bot.reply_msg(msg, result)


@on_private_message(name="PluginManager[manage_tools]")
def manage_tool(msg, bot):
    private_handlers = (
        do_inactivate, do_activate, do_list_plugin
    )
    for handler in private_handlers:
        result = handler(msg.content)
        if result is not None:
            return bot.reply_msg(msg, result)