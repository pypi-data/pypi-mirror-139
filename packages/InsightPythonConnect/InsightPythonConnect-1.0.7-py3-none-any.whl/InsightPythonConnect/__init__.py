# 17 / 02 / 22        -- WORKING -- 

from IPython.display import HTML, display, clear_output
import ipywidgets as widgets
import requests 
import json
import pandas as pd

def login():

    def clickEvent(a):
        try:
            global tokenId, appId, serverUrl, cookie, session, formParam
            session= requests.Session()
            uid = login_uid.value
            pwd = login_pwd.value
            appId = login_app_id.value
            serverUrl = login_server_url.value
            if not (uid.strip() and pwd.strip() and appId.strip() and serverUrl.strip()):
                print('All input fields are required.')
            else:  
                formParam = {'USER_CODE': uid, 'PASSWORD': pwd, 'IS_PWD_ENCRYPT' : 'false', 'INPUT_STR' :'', 'DATA_FORMAT':'JSON', 'IS_DESTROY_SESSION':'false','APP_ID': appId }
                response = session.post(serverUrl + '/ibase/rest/E12ExtService/login?', formParam)

                if str(response.status_code) == '200':
                    cookie = response.cookies
                    status = (json.loads(response.text))['Response']['status']
                    if status == 'success':
                        clear_output()
                        print('Login Successful')
                        responseStr = (json.loads(response.text))['Response']['status'], json.loads(response.text) 
                        tokenId = json.loads((responseStr[1])['Response']['results'])['TOKEN_ID'] 
                    elif status == 'error':
                        print (json.loads(response.text))
                    else:
                        pass

        except Exception as e:
            print(e)

    login_uid = widgets.Text(value='', placeholder='Enter Username',description='Username')
    login_pwd = widgets.Password(value='',placeholder='Enter Password', description='Password')
    login_app_id = widgets.Text(value='APPVIS',placeholder='Enter APPID', description='App ID')
    login_server_url = widgets.Text(value='https://proteusvision.com',placeholder='Enter Server URL', description='Server Url')
    login_btn = widgets.Button(description='Login')
    
    
    display(widgets.VBox([login_uid, login_pwd, login_server_url, login_btn]))
    login_btn.on_click(clickEvent)

def send_request(url, formParam1):
    try:
        response = session.post(url, formParam1, cookies=cookie)  
        if str(response.status_code) == '200':
            status = (json.loads(response.text))['Response']['status']
            if status == 'success':
                return  json.loads(response.text)['Response']['results']
            elif status == 'error':
                return json.loads(response.text)
            else:
                pass
        else : 
            return response.text
    except Exception as e:
        print(e)

def getVisualData(visualId, argumentList='', outType='JSON'):
    try:
        formParam = {'VISUAL_ID': visualId, 'OUTPUT_TYPE':outType, 'APP_ID': appId , 'TOKEN_ID':tokenId , 'DATA_FORMAT':'JSON', 'ARGUMENT_LIST':argumentList}
        visualData = send_request(serverUrl +'/ibase/rest/GenProcessPreviewService/getVisualData?' , formParam)
        return visualData 
    except NameError:
        print('Invalid Session. Please relogin and then try to access visual.')
    except Exception as e:
        print(e)
         
def getVisualInfo(visualId=''):
    try:
        formParam = {'VISUAL_ID': visualId, 'APP_ID': appId , 'TOKEN_ID':tokenId , 'DATA_FORMAT':'JSON'}
        visualInfo = send_request(serverUrl  + '/ibase/rest/GenProcessPreviewService/getVisualInfo?', formParam)
        return visualInfo
    except NameError:
        print('Invalid Session. Please relogin and then try to access visual.')
    except Exception as e:
        print(e)
    
def getVisualList(visualId=''):
    try:
        formParam = {'VISUAL_ID': visualId, 'APP_ID': appId , 'TOKEN_ID':tokenId , 'DATA_FORMAT':'JSON'}
        visualList = send_request(serverUrl + '/ibase/rest/GenProcessPreviewService/getVisualList?' , formParam)
        return visualList
    except NameError:
        print('Invalid Session. Please relogin and then try to access visual.')
    except Exception as e:
        print(e)

