#from fastapi import UploadFile ,File
#import time
#import shutil
import speech_recognition as sr

import re  # String 분석용도 
import requests

from constant import TMAP_APPKEY
from model import Master_Model, Target

class Master_Controller:
    def __init__(self, model:Master_Model = None):
        print("SYSTEM_CALL||Master_Controller_Created")
        self.__model:Master_Model = model # 마스터 모델
        
    # 최단 거리 검색
    #def makeWAV2Text(self, file:UploadFile= None):
    def makeWAV2Text(self, id):
        # 저장경로
        #save_path = f"./temp/{file.filename}" 
        #with open(save_path, "wb") as f:
            #shutil.copyfileobj(file.file, f) # 받은 파일 저장
        #print(f"SYSTEM_CALL||WAV_File_Saved_to_{save_path}")
        #time.sleep(0.5) # 잠시 대기
        
        #파일 이름 지정
        file_name = f"./sample{id}.wav"
        
        # Wav파일 분석 및 목표 찾기
        wav_recognizer = Wav_Recognizer()
        result:str = wav_recognizer.recognizing_file(file_path=file_name)
        print(f"Target_place : {result}")
        
        # dict 형태로 반환 데이터 준비
        return_data = {"place" : result, "stt" : f"{result}까지의 최단 거리를 검색합니다."}
        return return_data

    # 최단 경로 계산
    def getShortestPath(self, bid:str= '-1', target:str = "default"):
        print(f"SYSTEM_CALL||BID:{bid}and_Target:{target}_inserted")
        
        
        # 예외처리 return 문
        if bid == '-1' or target == "default":
            return 
        
        # 경로 검색기 생성
        path_finder = Path_Finder()
        # String 형태로 타입 변경
        bid = str(bid)

        # 현재 위치와 목표 위치 설정
        now_place:Target = self.__model.get_coord(bid)
        target_place:Target = self.__model.make_target(target=target)
        print("now_place :", now_place.get_name())
        print("target_place :", target_place.get_name())

        # Tmap 대중교통 경로 검색
        bus = path_finder.path_finding(now_place=now_place, target_place=target_place)
    
        # 버스를 찾지 못했을 때
        if bus == "None":
            return {"result": f"{target}로 갈수 있는 버스는 없습니다. 죄송합니다."}
        
        # 버스 찾았을 때 Dict 형태로 반환 데이터 준비
        return_data = f"{target}으로 가기 위해 {bus}"
        return_data = return_data + "번 버스를 타야합니다. 감사합니다."
            
        return {"result":return_data}
            
        
        
        

class Path_Finder:
    def __init__(self):
        print("SYSTEM_CALL||Welcome_Path_Finder")
        
    def path_finding(self, now_place:Target, target_place:Target):
        # Tmap 대중교통 url
        api_url = "https://apis.openapi.sk.com/transit/routes"
        
        # 전송할 데이터 (헤더)
        headers = {
            "accept": "application/json",  # JSON 형식으로 데이터
            "appKey": TMAP_APPKEY,  # 인증 토큰
            "content-type":"application/json"
        }

        # 전송할 데이터 (바디)
        body = {
            "startX": str(now_place.get_x()),
            "startY": str(now_place.get_y()),
            "endX": str(target_place.get_x()),
            "endY": str(target_place.get_y()),
            "count" : 1,
            "lang": 0,
            "format":"json"
        }

        # POST 요청 보내기
        response = requests.post(api_url, headers=headers, json=body)
        response = response.json()  # 돌아온 데이터 바디
        try:
            # 버스 한개만 가지고 온다
            result = self.__get_data_from_response(response=response)
        except Exception as e:
            result = "None"
        
        # bus정보의 리스트
        return result

    def __get_data_from_response(self, response:dict):
        
        bus:list = response["metaData"]["plan"]["itineraries"][0]["legs"][1]["route"]
        return bus
        

# WAV 파일 분석기
class Wav_Recognizer:
    def __init__(self):
        self.__recognizer = sr.Recognizer()
    
    # 분석기
    def recognizing_file(self, file_path = "./temp/"):
        # 음성 파일 열기
        with sr.AudioFile(file_path) as source:
            audio = self.__recognizer.record(source, duration= 120)
        
        # text로 변환 
        text = self.__recognizer.recognize_google(audio_data=audio, language='ko-KR')
        location_result = self.__extract_location(text) 
        
        # 목적지 반환
        return location_result
    
    # 문장에서 핵심 경로 추출
    def __extract_location(self, sentence):
        # "으로" 또는 "에"가 포함된 부분을 추출
        match = re.search(r'(.+?)(으로|에)', sentence)
        
        if match:
            result = match.group(1).strip()
            return result
        else:
            return None


        