#from uvirun import * 
#uvicorn uvirun:app --port 80 --host 0.0.0.0 --reload
import json,os,uvicorn,time
from fastapi import FastAPI, File, UploadFile,Form, Body
from fastapi.responses import HTMLResponse

app	 = FastAPI()
now	= lambda: time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))

@app.get('/')
def home(): 
	return HTMLResponse(content=f"<h2>{getattr(app,'title')}</h2><br>uvicorn uvirun:app --port 80 --host 0.0.0.0 --reload <br><a href='/docs'> docs </a> | <a href='/redoc'> redoc </a><br>last update: {app.tm} <br> started: {now()}")
# app.title = "hello" 
# app.tm = "2022.2.13"

if __name__ == '__main__':
	uvicorn.run(app, host='0.0.0.0', port=80)

'''
@app.get('/hello')
def hello(snt:str="I'm glad to meet you."): 
	return snt
'''