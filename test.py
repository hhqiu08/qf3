import streamlit as st
from streamlit_chat import message
import requests
import json

API_Key=st.text_input("设置API_Key:",key='input1')
Secret_Key=st.text_input("设置Secret_Key:",key='input2')

def get_access_token(API_Key,Secret_Key):
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """
    hed='https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='
    md='&client_secret='
    
    url =hed +API_Key+md+Secret_Key
    
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")


def test(prmt,API_Key,Secret_Key):
   
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie_speed?access_token=" + get_access_token(API_Key,Secret_Key)
    
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": prmt
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    #print(response.text)
    return response.text

def generate_response(prompt,API_Key,Secret_Key):
    r=test(prompt,API_Key,Secret_Key)
    i1=r.find('"result":',0,len(r))
    i2=r.find('"is_truncated":',0,len(r))
    ms=r[i1+10:i2-2]
    return ms
 
st.markdown("#### 我是医生聊天机器人,我可以回答您的任何问题！")
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
user_input=st.text_input("请输入您的问题:",key='input3')
if user_input:
    output=generate_response(user_input,API_Key,Secret_Key)
    st.session_state['past'].append(user_input)
    st.session_state['generated'].append(output)
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], 
                is_user=True, 
                key=str(i)+'_user')



