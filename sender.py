import cv2
import numpy as np
from vidstream import ScreenShareClient

client = ScreenShareClient('192.168.56.1', 9999)
client.start_stream()
while True:
    print("Hello")
    frame = client._get_frame()    # Đọc khung hình
    img = np.array(frame)              #Đây là im

    # Hiển thị khung hình đã thay đổi kích thước
    if cv2.waitKey(1) == ord('q'):    # Thoát vòng lặp khi nhấn phím 'q'
        break

cv2.destroyAllWindows()
client.stop_stream()
