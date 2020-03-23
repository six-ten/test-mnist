from tensorflow.keras.models import load_model
import numpy as np
from pprint import pprint
import socket
import matplotlib.pyplot as plt
print('finished importing libs')
model = None

host = socket.gethostname()
port = 6789
server_socket = socket.socket()
server_socket.bind((host,port))
image_dims = (28,28,1)

model_state = False


def init_task(ml_model='model.h5'):
    global model
    print('loading classification model')
    model = load_model(ml_model)
    print('finished loading')


def run_task(image):
    global model_state
    if not model_state :
        model_state = True
        init_task()
    else :
        #return np.array([0,0,0,1,0,0,0],dtype='float32')
        try :
            plt.imshow(image.reshape(image.shape[1:3]))
            plt.show()
        except Exception as e :
            print(e)
        return model.predict(image)[0]


def clean_up():
    server_socket.close()
    


def run_server():
    server_socket.listen(3)
    while True :
        pprint('awaiting connection')
        conn, address = server_socket.accept()
        print('connection from : '+str(address))
        while True :
            
            data = conn.recv(1024)
            try:
                if data.decode()[:4] == 'quit':
                    conn.close()
                    clean_up()
                    break
            except Exception as e :
                print(e)
            image = np.frombuffer(data,dtype='uint8',count=-1)
            image = np.divide(image,255.0,dtype='float32')
            image = image.reshape((1,)+image_dims)
            res = run_task(image)
            msg = str(np.argmax(res,axis=0))
            conn.send(msg.encode())
            

run_server()
















    
