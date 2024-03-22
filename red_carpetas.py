
import os
from keras.preprocessing import image
from PIL import Image
import matplotlib.pyplot as plt
from keras.models import load_model
from keras.preprocessing import image
from keras.models import Sequential
from keras.layers import Flatten, Conv2D, MaxPool2D, Conv2DTranspose, Reshape
from tensorflow.keras.optimizers import Adam
from PIL import Image
import numpy as np


def preprocessing(ruta_imagen):
    imagen = Image.open(ruta_imagen)

    imagen = imagen.resize((400, 400))  # Reemplaza con las dimensiones esperadas por tu modelo
    tensor_imagen = image.img_to_array(imagen)
    #tensor_imagen = np.expand_dims(tensor_imagen, axis=0) #le anado una dimension al tensor para que sea el tamano necesario para la red
    tensor_imagen /= 255.0  # Normalizar los valores de pixeles al rango [0, 1]
    return tensor_imagen

#A partir de los directorios de las carpetas las preproceso y las meto en X e Y
#ruido
ruta_carpeta_ruido = ''
elementos_ruido = os.listdir(ruta_carpeta_ruido)
X =[]
for elemento in elementos_ruido:
    Img_ruido=preprocessing(''+ elemento)
    X.append(Img_ruido)

#limpio o no ruido
ruta_carpeta_limpio = ''
elementos_limpio = os.listdir(ruta_carpeta_limpio)
Y =[]
for elemento in elementos_limpio:
    Img_limpio=preprocessing('' +elemento)
    Y.append(Img_limpio) 

X = np.array(X)
Y = np.array(Y)

input_shape = (400, 400, 3)#ancho, altura y canales (3 porq es con RGB)

#creamos nuestro modelo
model = Sequential([
    Conv2D(filters=32, kernel_size=(3, 3), activation='relu', padding = 'same', input_shape=input_shape), 
    MaxPool2D(pool_size=(2, 2), strides=2), #divide por 2 dimensiones
    Conv2D(filters=64, kernel_size=(3, 3), activation='relu', padding = 'same'),
    MaxPool2D(pool_size=(2, 2), strides=2),
    Conv2DTranspose(3, kernel_size=(4, 4), strides=(4, 4), padding='same', activation='sigmoid') #las capas de maxpool2D dividen por dos las dimensiones, antes de esta tengo dimensiones (100,100,3) y yo quiero tenero (400,400,3) igual q el input. Asi que multiplico por 4
])    

model.compile(optimizer=Adam(learning_rate=0.0001), loss='mean_squared_error', metrics=['accuracy'])
model.fit(X, Y, epochs=10, batch_size=3) #batch_size=3 xq estoy entrenando ahora con tres imagenes

#prediccion para una imagen nueva con ruido
imagen_con_ruido= np.array(preprocessing('')) #mete la ruta de la imagen que quieres predecir
imagen_con_ruido = np.expand_dims(imagen_con_ruido, axis=0) #al realizar predicciones con model.predict keras necesita que incluyas la dimension del lote, aunque sea solo con una muestra. En el entrenamiento lo hace solo keras, pero aqui hay q ponerlo si o si.
imagen_sin_ruido_predicha = model.predict(imagen_con_ruido)
imagen_sin_ruido_predicha = imagen_sin_ruido_predicha.squeeze() * 255.0
imagen_resultante = Image.fromarray(imagen_sin_ruido_predicha.astype('uint8'))
#imagen_resultante.save(r"C:\Users\julia\Documents\Innova\matlab\imagenes\imagen_procesada_4_predicha.png") #PARA GUARDAR IMAGEN

plt.imshow(imagen_resultante)
plt.axis('off')  # Desactivar ejes
plt.show()
