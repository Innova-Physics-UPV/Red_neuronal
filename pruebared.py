import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models

def load_images_from_directory(directory):
    images = []
    for filename in os.listdir(directory):
        img = cv2.imread(os.path.join(directory, filename))
        if img is not None:
            images.append(img)
    return np.array(images)

def preprocess_images(images):
    # Normalizar imágenes
    images = images.astype('float32') / 255.
    return images

def build_model(input_shape):
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=input_shape),
        layers.MaxPooling2D((2, 2), padding='same'),
        layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        layers.MaxPooling2D((2, 2), padding='same'),
        layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        layers.UpSampling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        layers.UpSampling2D((2, 2)),
        layers.Conv2D(3, (3, 3), activation='sigmoid', padding='same')
    ])
    return model

# Directorios donde se encuentran las imágenes con ruido y las imágenes limpias
train_noisy_dir = "directorio ruido"
train_clean_dir = "directorio sin ruido"

# Cargar imágenes con ruido y limpias desde los directorios
x_train_noisy = load_images_from_directory(train_noisy_dir)
x_train_clean = load_images_from_directory(train_clean_dir)

# Comprueba las formas de tus matrices de datos
print("Forma de x_train_noisy:", x_train_noisy.shape)
print("Forma de x_train_clean:", x_train_clean.shape)

# Preprocesamiento de las imágenes
x_train_noisy = preprocess_images(x_train_noisy)
x_train_clean = preprocess_images(x_train_clean)

# Definir y compilar el modelo
input_shape = x_train_noisy.shape[1:]
model = build_model(input_shape)
model.compile(optimizer='adam', loss='mean_squared_error')

# Entrenar el modelo
model.fit(x_train_noisy, x_train_clean, epochs=10, batch_size=32)




#Esto se deja comentado porque ya es para un futuro cuando ya esté entrenada la red:
# Directorio donde se encuentran las nuevas imágenes con ruido
#test_noisy_dir = "/ruta/al/directorio/con/nuevas/imagenes/con/ruido"

# Cargar nuevas imágenes con ruido desde el directorio
#x_test_noisy = load_images_from_directory(test_noisy_dir)

# Preprocesamiento de las imágenes
#x_test_noisy = preprocess_images(x_test_noisy)

# Predicción de las imágenes limpias usando el modelo entrenado
#x_test_denoised = model.predict(x_test_noisy)

# Guardar las imágenes limpias en un directorio
#output_dir = "/ruta/al/directorio/de/salida/imagenes/limpias"
#for i, image in enumerate(x_test_denoised):
    #cv2.imwrite(os.path.join(output_dir, f"clean_image_{i}.jpg"), cv2.cvtColor(image * 255, cv2.COLOR_RGB2BGR))
