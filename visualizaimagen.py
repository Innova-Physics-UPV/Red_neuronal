#este código es para una vez ejecutemos la red con las imagenes nuevas sin ruido, poder visualizarlas.

import matplotlib.pyplot as plt

# Directorio donde se guardaron las imágenes limpias
output_dir = "/ruta/al/directorio/de/salida/imagenes/limpias"

# Leer las imágenes limpias desde el directorio de salida
clean_images = []
for filename in os.listdir(output_dir):
    img = cv2.imread(os.path.join(output_dir, filename))
    if img is not None:
        clean_images.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

# Visualizar las imágenes limpias
plt.figure(figsize=(10, 10))
for i in range(len(clean_images)):
    plt.subplot(1, len(clean_images), i + 1)
    plt.imshow(clean_images[i])
    plt.axis('off')
    plt.title(f"Clean Image {i+1}")
plt.show()
#