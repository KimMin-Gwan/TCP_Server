
from fastapi.responses import RedirectResponse, FileResponse 
from fastapi import FastAPI, HTTPException, WebSocket 
from fastapi import UploadFile, File
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel
import uvicorn
import json

#-----------------------------------------------------------
from controller import Master_Controller


# 앱 서버
class AppServer():
    def __init__(self, controller:Master_Controller = None):
        self.app = FastAPI()   # app
        self.controller = controller

        # 미들웨어
        self.app.add_middleware(
            CORSMiddleware, 
            allow_origins='*',
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # 메인 라우터 실행
        self.register_routes()
    
    # 메인 라우터
    def register_routes(self):
        @self.app.get("/")
        async def home_page():
            return "hello_world"
        
        # 도착지 분석
        @self.app.post("/get_wav")
        async def recog_voice(file: UploadFile = File(..., required = False)):
            # file 상태 체크
            if file is None:
                print('SYSTEM_CALL_ERROR||Wav_File_did_not_Uploaded')
                result = {"place" : "Default", "stt":"잘 이해하지 못했어요."}
                return result
            print("SYSTEM_CALL||Wav_File_Upload_Complete")   

            try:
                # 컨트롤러 실행
                result = self.controller.makeWAV2Text(file=file)
            except Exception as e:
                print("SYSTEM_CALL_ERROR||Controller_did_not_work")
                print(e)
                result = {"place":"Default", "stt":"잘 이해하지 못했어요."}
            return result

        # 경로 찾기
        @self.app.get("/search_path")
        def search_path(bid:int, target:str):
            if bid is None or target is None:
                print('SYSTEM_CALL_ERROR||Beacon_ID_and_targer_did_not_accept')
                result = {"result":"Error"}
                return result
            try:
                # 컨트롤러 실행
                result = self.controller.getShortestPath(bid=bid, target=target)
            except Exception as e:
                print("SYSTEM_CALL_ERROR||Controller_did_not_work")
                print(e)
                result = {"result":"Error"}

            return result
            
    # 서버 실행기
    def run_system(self):
        uvicorn.run(self.app, host="127.0.0.1", port=8000)
        
        
        