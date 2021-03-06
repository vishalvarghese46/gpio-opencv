import numpy as np
import cv2
import socket


class videoStreaming(object):
    def __init__(self, host, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(0)
        self.connection, self.client_address = self.server_socket.accept()
        self.connection = self.connection.makefile('rb')
        self.host_name = socket.gethostname()
        self.host_ip = socket.gethostbyname(self.host_name)
        self.streaming()

    def streaming(self):

        try:
            print(f'Host: {self.host_name}, {self.host_ip}')
            print(f'Connection from: {self.client_address}')
            print("Streaming...")
            print("Press 'q' to exit")

            # need bytes here
            stream_bytes = b' '
            while True:
                stream_bytes += self.connection.read(1024)
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    cv2.imshow('image', image)

                    grey_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    blur = cv2.GaussianBlur(grey_img, (5,5), 0)
                    ret, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)

                    '''
                    mask = cv2.erode(thresh1, None, iterations=2)
                    mask = cv2.dilate(mask, None, iterations=2)
                    '''

                    contours, hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)
                    if len(contours)>0:
                        c = max(contours, key=cv2.contourArea)
                        M = cv2.moments(c)         #Finding the moments which will return a dictiornary of
                                                                    #mass of the object, area of the object etc.
                        cx = int(M['m10']/M['m00'])     #finding the centroids from the moments dictionary cx, cy
                        cy = int(M['m01']/M['m00'])

                        cv2.line(image, (cx, 0), (cx, 720), (255, 0, 0), 1)
                        cv2.line(image, (0, cy), (1280, cy), (255, 0, 0), 1)

                        cv2.drawContours(image, contours, -1, (0, 255, 0), 1)

                    else:
                        print("Can't see shit dawg!")

                    #self.connection.send(bytes("1", "utf-8"))
                    print(cx, cy)

                    cv2.imshow('Frame', image)


                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
        finally:
            self.connection.close()
            self.server_socket.close()


if __name__ == '__main__':
    # host, port
    h, p = "192.168.1.67", 8000
    videoStreaming(h, p)
