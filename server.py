import cv2
import numpy as np
import pyaudio
import socket
from vidstream import StreamingServer
import threading

clients = []
nicknames = []

cap = cv2.VideoCapture(0)
# Khai báo kết nối
HOST = '192.168.56.1'
VIDEO_PORT = 8080
AUDIO_PORT = 8081
CHAT_PORT = 5555
screen_stream = StreamingServer('192.168.56.1',9999)

t = threading.Thread(target=screen_stream.start_server)
t.start()



# Khai báo kích thước khung hình (điều chỉnh theo thiết bị của bạn)
WIDTH = 640
HEIGHT = 480

# Khởi tạo socket video
video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
video_socket.bind((HOST, VIDEO_PORT))
video_socket.listen(1)
print(f"Video socket is listening on {HOST}:{VIDEO_PORT}")

# Khởi tạo socket audio
audio_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
audio_socket.bind((HOST, AUDIO_PORT))
audio_socket.listen(1)
print(f"Audio socket is listening on {HOST}:{AUDIO_PORT}")








# chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# chat_socket.bind((HOST, CHAT_PORT))
# chat_socket.listen()
# print(f"Chat socket is listening on {HOST}:{CHAT_PORT}")

# Khởi tạo stream audio và biến đếm frames
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)




# Chờ kết nối từ client
print("Waiting for connection...")
video_conn, video_addr = video_socket.accept()
audio_conn, audio_addr = audio_socket.accept()
#chat_conn, chat_addr = chat_socket.accept()
print(f"Video connection from {video_addr} is established!")
print(f"Audio connection from {audio_addr} is established!")
#print(f"Chat connection from {chat_addr} is established!")




while True:
    # Đọc khung hình từ webcam
    ret, frame = cap.read()

    # Thay đổi kích thước khung hình
    frame = cv2.resize(frame, (WIDTH, HEIGHT), interpolation = cv2.INTER_AREA)

    # Chuyển đổi khung hình thành mảng byte
    frame = cv2.imencode('.jpg', frame)[1].tobytes()

    # Gửi độ dài khung hình và khung hình đến client
    video_conn.sendall(len(frame).to_bytes(4, byteorder='little'))
    video_conn.sendall(frame)

    # Ghi âm từ microphone
    audio_data = stream.read(1024)
    
    # Gửi độ dài audio và audio data đến client
    audio_conn.sendall(len(audio_data).to_bytes(4, byteorder='little'))
    audio_conn.sendall(audio_data)
    


    # Nếu nhận được kí tự 'q' thì thoát khỏi vòng lặp
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên và đóng kết nối
cap.release()
cv2.destroyAllWindows()
screen_stream.stop_server()
video_conn.close()
audio_conn.close()

p.terminate()
