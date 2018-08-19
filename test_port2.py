from chatbot_cut.test_port import  chatbot_port
import sys
import os
from tfidf.test_port import Chatbot_port2
import time
s=chatbot_port()
t=Chatbot_port2()
print("?????")
type=0
while(True):
    st=''
    with open('qq_intput.txt', 'r', encoding='utf-8') as f:
        st=f.read()
        st=st.strip()
    time.sleep(0.1)
    if len(st)>=1 and st[0]!='%':
        print('2')
        if type==0:
            st=s.chat(st[1:])
        else:
            st=t.chat(st[1:])
        with open('qq_intput.txt', 'w', encoding='utf-8') as f:
            print('%',st[:st.find('<')],file=f)
            print('3')

