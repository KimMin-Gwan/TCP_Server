import json
import requests
import pygame
import socket
import os

from constant import HOST, PORT, BUFFER_SIZE
    
class TCP_Server:
    def __init__(self):
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sock.connect((HOST, PORT))
        
    def send_string(self, bid = '-1', target = "Default"):
        protocol = f'STRING:{bid}:{target}'
        self.client_sock.sendall(protocol.encode())
        
        result = self.client_sock.recv(BUFFER_SIZE)
        decoded_data = result.decode()
        
        result = self.client_sock.recv(BUFFER_SIZE)
        decoded_data = json.loads(result.decode()) 
        
        return decoded_data
        
    def send_file(self, file_path):
        
        with open(file_path, 'rb') as file:
            file_size = os.path.getsize(file_path)
            protocol = f'FILE:{file_size}'
            self.client_sock.sendall(protocol.encode())
            recive = self.client_sock.recv(BUFFER_SIZE)
            
            data = file.read(BUFFER_SIZE)
            while data:
                self.client_sock.send(data)
                data = file.read(BUFFER_SIZE)
        
        result = self.client_sock.recv(BUFFER_SIZE)
        
        decoded_data = json.loads(result.decode())
        
        return decoded_data

    def close_socket(self):
        protocol = 'END:'
        self.client_sock.sendall(protocol.encode())
        self.client_sock.close()
    
# 버스 파인더
class Bus_Finder():
    def __init__(self):
        #self.url = url  # 기본 url(constant로 옮길것)
        self.tcp_connect = TCP_Server()
        #self.server_flag = False # 서버 플래그
        #self.__check_flag()  #서버 가동 확인

    # 경로까지 버스 찾기
    def run_bus_finder(self, bid = "1"):
        # 서버 가동 확인
        #self.__check_flag()
        #if not self.server_flag:
        #    return
        
        # 목표위치 검색
        target = self.__get_target()
        if target == "Default":
            try:
                self.tcp_connect.close_socket()
            except:
                print("may be connection close")
            finally:
                return
        
        # 경로 까지 버스 검색
        self.__search_path(bid=bid, target=target)
        
        try:
            self.tcp_connect.close_socket()
        except:
            print("may be connection close")
        finally:
            return
        
        

    # 도착지 찾기
    def __get_target(self):
        ## url 제작
        #url = self.url + "get_wav"

        ## 음성 녹음 파일 열기
        #file = {'file': ('sample.wav', open('./sample.wav', 'rb'))}

        file_path = './sample.wav'

        response = self.tcp_connect.send_file(file_path)

        # 서버에 데이터 요청 
        #json_result = response.json()
        print(response)

        # 음성 재생
        #tts = response['stt']
        #kakaoTTS = KakaoTTS()
        #kakaoTTS.saveFile(tts)
        #kakaoTTS.playFile()

        target:str = response['place']
        return target

    # 경로 찾기
    def __search_path(self, bid, target):
        # url 제작
        #url = self.url + f"search_path/?bid={bid}&target={target}"

        response = self.tcp_connect.send_string(bid=bid, target=target)
        # 서버로 데이터 요청
        #response = requests.get(url)
        #response = response.json()
        print(response)

        # 음성 재생
        #stt = response["result"]
        #kakaoTTS = KakaoTTS()
        #kakaoTTS.saveFile(stt)
        #kakaoTTS.playFile()
        return

    ## 서버가 연결되었는지 확인하는 코드
    #def __check_flag(self):
        ## 기본 주소로 서버에 접속
        #response = requests.get(self.url)
        ## 서버가 정상작동한다면 상태 코드가 200 일것
        #if response.status_code == 200:
            ## 정상작동하면 플레그 True로 변경
            #self.server_flag = True
            #print("SYSTEM_CALL||Server_Connected_Well")
        #else:
            ## 정상작동하면 플레그 False 로 변경
            #self.server_flag = False
            #print(f"SYSTEM_CALL||Server_Connected_fail(Code:{response.status_code})")


# 자신의 REST_API_KEY를 입력
# constant로 옮길것
REST_API_KEY = "YOUR_REST_API_KEY"


# TTS
class KakaoTTS:
    def __init__(self, text, API_KEY=REST_API_KEY):
        # TTS데이터를 얻기 위해 텍스트를 서버로 전송
        self.resp = requests.post(
            url="https://kakaoi-newtone-openapi.kakao.com/v1/synthesize",
			headers={
				"Content-Type": "application/xml",
				"Authorization": f"KakaoAK {API_KEY}"
			},
			data=f"<speak>{text}</speak>".encode('utf-8')
        )

    # TTS 파일 저장
    def saveFile(self, filename="output.mp3"):
        with open(filename, "wb") as file:
            file.write(self.resp.content)
        return

    # 파일 재생
    def playFile(self):
        pygame.mixer.init()
        pygame.mixer.music.load("output.mp3")
        pygame.mixer.music.play()


if __name__ == "__main__":
    bus_finder = Bus_Finder()
    bus_finder.run_bus_finder()
    
    
        
    
        
        