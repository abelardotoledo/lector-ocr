import cv2
import pytesseract
from googletrans import Translator
import tkinter as tk
from tkinter import Label, Button, Text, ttk
#from libretranslatepy import LibreTranslateAPI

#lt = LibreTranslateAPI("https://translate.terraprint.co/") #se inicializa la api

#Inicializar variables para la camara
cuadro = 100
anchocam, altocam = 640, 480

# Initialize the webcam
cap = cv2.VideoCapture(0)

def capture_image():
    # Check if the webcam is opened correctly
    if not cap.isOpened():
        print("Error: No es posible abrir la WebCam.")
        return None

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == False: break #Si no se lee correctamente se cierra
        cv2.putText(frame, "Texto Aqui", (250, cuadro-10), cv2.FONT_HERSHEY_SIMPLEX, 0.71, (255,255,0), 2)
        cv2.rectangle(frame, (cuadro, cuadro), (anchocam - cuadro, altocam - cuadro), (0, 0, 255), 2) #Se genera el recuadro
        x1, y1 = cuadro, cuadro # Coordenadas de la esquina superior izquierda del recuadro
        ancho, alto = (anchocam - cuadro) - x1, (altocam - cuadro) - y1 # Se extrae el ancho y alto
        x2, y2 = x1 + ancho, y1 + alto #Se almacena los pixeles del recuadro
        image_recuadro = frame[y1:y2, x1:x2] #Se guardan los pixeles
        cv2.imshow("Lector OCR", frame)
        key = cv2.waitKey(1)
        if key == 32: #ASCII de la tecla espacio
            #Guarda la imagen del recuadro
            cv2.imwrite("captured_image.png", image_recuadro)
            break
        elif key == 27:  #ASCII de Esc
            break

    #Close the window
    cv2.destroyAllWindows()

    return 'captured_image.png'

def extract_text(image_path):
    # Load the captured image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use Tesseract to extract text
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    text = pytesseract.image_to_string(gray)
    return text

#def translate_text(text, src_lang, dest_lang):
def translate_text():
    texto = txt_extract_display.get(1.0, tk.END)
    origen = combo_language.get()
    translator = Translator()
    #Si es español traduce al ingles
    if origen=="Inglés":  
        traduccion = translator.translate(texto, src="auto", dest="en")
    #Si es ingles traduce al español
    elif origen=="Español":
        traduccion = translator.translate(texto, src="auto", dest="es")
    elif origen == "Japonés":
        traduccion = translator.translate(texto, src="auto", dest="ja")
    elif origen == "Alemán":
        traduccion = translator.translate(texto, src="auto", dest="de")
    elif origen == "Chino Simplificado":
        traduccion = translator.translate(texto, src="auto", dest="zh-cn")
    elif origen == "Chino Tradicional":
        traduccion = translator.translate(texto, src="auto", dest="zh-tw")
    elif origen == "Ruso":
        traduccion = translator.translate(texto, src="auto", dest="ru")
    else: print("No es posible traducir")
    txt_translate_display.delete(1.0, tk.END)
    txt_translate_display.insert(tk.END, traduccion.text)
def process_image():
    image_path = capture_image()
    if image_path:
        text = extract_text(image_path)
        display_extract_texts(text)

def display_extract_texts(extracted_text):
    txt_extract_display.delete(1.0, tk.END)
    txt_extract_display.insert(tk.END, extracted_text)

def clear_display():
    txt_extract_display.delete(1.0, tk.END)
    txt_translate_display.delete(1.0, tk.END)

# Set up the GUI
root = tk.Tk()
root.title("Lector OCR/Traductor")
root.geometry("600x550")

frame = tk.Frame(root)
frame.grid(padx=10, pady=10)
#Fila 0
label = Label(frame, text="Presione 'Capturar' para tomar una foto y extraer el texto")
label.grid(column=0, row=0)
#Fila 1
capture_button = Button(frame, text="Capturar", command=process_image)
capture_button.grid(column=0, row=1, sticky="WE")
clear_button = Button(frame, text="Limpiar", command=clear_display)
clear_button.grid(column=1, row=1, sticky = "WE")
#Fila 2
combo_language = ttk.Combobox(state="readonly", values=["Inglés", "Español", "Japonés", "Alemán", 
                                                        "Chino Simplificado", "Chino Tradicional", "Ruso"])
combo_language.place(width=300, height=20, x=10, y=60)
translate_button = Button(frame, text="Traducir", command=translate_text)
translate_button.grid(column=1, row=2, sticky="WE")

#Fila 3
lb1 = Label(frame, text="Texto Extraido")
lb1.grid(column=0, row=3)
lb2 = Label(frame, text="Texto Traducido")
lb2.grid(column=1, row=3)
#Fila 4
txt_extract_display = Text(frame, wrap=tk.WORD, height=25, width=30)
txt_extract_display.grid(column=0, row=4)
txt_translate_display = Text(frame, wrap=tk.WORD, height=25, width=30)
txt_translate_display.grid(column=1, row=4)

# Run the GUI event loop
root.mainloop()
#Release the webcam
cap.release()