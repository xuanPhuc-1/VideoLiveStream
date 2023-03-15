import cv2
import numpy as np
import pyaudio
import socket
from vidstream import ScreenShareClient
import threading

# Khai báo kết nối
HOST = '192.168.56.1'
VIDEO_PORT = 8080
AUDIO_PORT = 8081
SHARE_PORT = 9999
CHAT_PORT = 5555
#nickname = input("Choose your nickname: ")



# Khởi tạo socket video
video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
video_socket.connect((HOST, VIDEO_PORT))
print(f"Connected to video socket on {HOST}:{VIDEO_PORT}")

# Khởi tạo socket audio
audio_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
audio_socket.connect((HOST, AUDIO_PORT))
print(f"Connected to audio socket on {HOST}:{AUDIO_PORT}")





# chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# chat_socket.connect((HOST, CHAT_PORT))
# print(f"Connected to chat socket on {HOST}:{CHAT_PORT}")




client = ScreenShareClient('192.168.56.1', 9999)
client.start_stream()
print("Sharing the video")
# Mở stream audio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True)

while True:
    frame_sharing = client._get_frame()
    img = np.array(frame_sharing)
    #np.savetxt('img_screen.txt', img)
    # Nhận độ dài khung hình và khung hình từ server
    data = b''
    while len(data) < 4:
        packet = video_socket.recv(4 - len(data))
        if not packet:
            break
        data += packet
    if not packet:
        break
    length = int.from_bytes(data, byteorder='little')
    data = b''
    while len(data) < length:
        packet = video_socket.recv(length - len(data))
        if not packet:
            break
        data += packet
    if not packet:
        break

    # Chuyển đổi mảng byte thành khung hình
    frame_pic = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    #np.savetxt('img_webcam.txt', frame_pic)
    # Hiển thị khung hình
    cv2.imshow("Webcam", frame_pic)

    # Nhận độ dài audio và audio data từ server
    data = b''
    while len(data) < 4:
        packet = audio_socket.recv(4 - len(data))
        if not packet:
            break
        data += packet
    if not packet:
        break
    length = int.from_bytes(data, byteorder='little')
    data = b''
    while len(data) < length:
        packet = audio_socket.recv(length - len(data))
        if not packet:
            break
        data += packet
    if not packet:
        break

    # Ghi âm ra loa
    stream.write(data)

    # Nếu nhận được kí tự 'q' thì gửi kí tự 'q' đến server và thoát khỏi vòng lặp
    if cv2.waitKey(1) & 0xFF == ord('q'):
        video_socket.sendall(b'q')
        break

# Giải phóng tài nguyên và đóng kết nối
cv2.destroyAllWindows()
client.stop_stream()
video_socket.close()
audio_socket.close()

p.terminate()
