import os
import cv2
import shutil

def crear_estructura_directorios(dir_origen, dir_destino):
    if os.path.exists(dir_destino):
        print(f"El directorio destino {dir_destino} ya existe. Eliminándolo.")
        shutil.rmtree(dir_destino)
    shutil.copytree(dir_origen, dir_destino, ignore=shutil.ignore_patterns('*.jpeg', '*.jpg', '*.png'))

def procesar_imagenes(dir_origen, dir_destino, funcion_filtro):
    for root, dirs, files in os.walk(dir_origen):
        for file in files:
            if file.lower().endswith(('.jpeg', '.jpg', '.png')):
                # Ruta completa del archivo
                ruta_archivo = os.path.join(root, file)
                # Leer la imagen
                img = cv2.imread(ruta_archivo)
                if img is None:
                    print(f"No se pudo leer la imagen {ruta_archivo}.")
                    continue
                # Aplicar la función de filtro
                img_procesada = funcion_filtro(img)
                # Construir la ruta de destino correspondiente
                ruta_relativa = os.path.relpath(root, dir_origen)
                dir_destino_sub = os.path.join(dir_destino, ruta_relativa)
                if not os.path.exists(dir_destino_sub):
                    os.makedirs(dir_destino_sub)
                ruta_archivo_destino = os.path.join(dir_destino_sub, file)
                # Guardar la imagen procesada
                cv2.imwrite(ruta_archivo_destino, img_procesada)
                print(f"Procesado y guardado: {ruta_archivo_destino}")

def filtro_bilateral(img):
    # Parámetros óptimos para imágenes de rayos X
    d = 9
    sigmaColor = 75
    sigmaSpace = 75
    img_procesada = cv2.bilateralFilter(img, d, sigmaColor, sigmaSpace)
    return img_procesada

def filtro_canny_edge(img):
    # Convertir a escala de grises
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Aplicar el filtro Canny Edge con parámetros óptimos
    threshold1 = 30
    threshold2 = 100
    bordes = cv2.Canny(gris, threshold1, threshold2)
    # Convertir los bordes a 3 canales para mantener el formato de color
    img_procesada = cv2.cvtColor(bordes, cv2.COLOR_GRAY2BGR)
    return img_procesada

if __name__ == '__main__':
    # Directorio de origen
    dir_origen = r'C:\Users\dnlal\Downloads\archive (3)\Covid19-dataset'  # Ajusta esta ruta

    # Conjunto de datos con Filtro Bilateral
    dir_destino_bilateral = r'C:\Users\dnlal\Downloads\archive (3)\Covid19-dataset-bilateral'
    crear_estructura_directorios(dir_origen, dir_destino_bilateral)
    procesar_imagenes(dir_origen, dir_destino_bilateral, filtro_bilateral)

    # Conjunto de datos con Filtro Canny Edge
    dir_destino_canny = r'C:\Users\dnlal\Downloads\archive (3)\Covid19-dataset-canny'
    crear_estructura_directorios(dir_origen, dir_destino_canny)
    procesar_imagenes(dir_origen, dir_destino_canny, filtro_canny_edge)

    print("Procesamiento completado.")
