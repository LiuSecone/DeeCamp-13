from chatbot_cut.test_port import  chatbot_port
import sys
import os
import time
s=chatbot_port()
print("?????")
while(True):
    st=''
    with open('qq_intput.txt', 'r', encoding='utf-8') as f:
        st=f.read()
        st=st.strip()
        st=st[1:]
    time.sleep(0.1)
    if len(st)>=1 and st[0]!='%':
        print('2')
        st=s.chat(st)
        with open('qq_intput.txt', 'w', encoding='utf-8') as f:
            print('%',st[:st.find('<')],file=f)
            print('3')
