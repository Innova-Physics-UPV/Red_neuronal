clear all;

% Seleccionamos la carpeta con las imágenes (y saca el path)
path_name = uigetdir(pwd, 'Selecciona la carpeta con imágenes');

% Creamos una carpeta en el one drive con las imágenes procesadas (se crea
% dentro de la carpeta seleccionada)
carpeta_onedrive = fullfile(path_name, 'Imágenes Procesadas');
if ~exist(carpeta_onedrive, 'dir')
    mkdir(carpeta_onedrive);
end

% Lista de archivos de imagen en la carpeta + formato en que tenemos las
% imágenes
archivos_imagenes = dir(fullfile(path_name, '*.png'));

% Número de píxeles deseados
numero_pixeles = 270;

% Vamos iterando las imágenes desde la primera hasta la última
for i = 1:length(archivos_imagenes)
    % Leer la imagen con la que esta trabajando
    ruta_imagen = fullfile(path_name, archivos_imagenes(i).name);
    imagen_original = imread(ruta_imagen);

    % Obtener el tamaño actual de la imagen
    [alto_original, ancho_original, ~] = size(imagen_original);

    % Verificar si la imagen es más pequeña que el número de píxeles deseados
    if alto_original < numero_pixeles || ancho_original < numero_pixeles
        % Crear una nueva imagen con el tamaño deseado y rellenar con ceros
        imagen_redimensionada = zeros(numero_pixeles, numero_pixeles, size(imagen_original, 3));

        % Copiar la imagen original en la esquina superior izquierda
        imagen_redimensionada(1:alto_original, 1:ancho_original, :) = imagen_original;
    else
        % Redimensionar la imagen al tamaño deseado
        imagen_redimensionada = imresize(imagen_original, [numero_pixeles, numero_pixeles]);
    end

    % Generar tipo de ruido y intensidad aleatorios
    tipos_de_ruido = {'gaussian', 'salt & pepper', 'speckle'};
    tipo_de_ruido = tipos_de_ruido{randi(length(tipos_de_ruido))};
    intensidad_de_ruido = rand() * 0.5;

    % Agregar ruido a la imagen redimensionada
    imagen_con_ruido = imnoise(imagen_redimensionada, tipo_de_ruido, intensidad_de_ruido);

    % Mostrar la imagen original y la imagen con todos los cambios
    figure;
    subplot(1, 2, 1);
    imshow(imagen_original);
    title('Imagen Original');

    subplot(1, 2, 2);
    imshow(imagen_con_ruido);
    title('Imagen con Ruido');

    % Guardar la nueva imagen en la carpeta de OneDrive
    nombre_nueva_imagen = sprintf('imagen_procesada_%d.png', i);
    ruta_guardado = fullfile(carpeta_onedrive, nombre_nueva_imagen);
    imwrite(imagen_con_ruido, ruta_guardado);
end
