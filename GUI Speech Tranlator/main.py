from tkinter import *
import os
from PIL import ImageTk, Image
import threading as td
import tkinter.messagebox as tkMessageBox
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
from googletrans import Translator
import asyncio

# Initialize the recognizer
r = sr.Recognizer()

main = Tk()
main.title("Voiceprint Translator")
main.geometry("940x570")
main.config(bg="#C7F8FF")
main.resizable(0, 0)

# Language options
lt = [
  "Afrikaans", "Albanian", "Amharic", "Arabic", "Armenian", "Azerbaijani",
  "Basque", "Belarusian", "Bengali", "Bosnian", "Bulgarian", "Catalan",
  "Cebuano", "Chichewa", "ChineseSimplified", "ChineseTraditional", "Corsican",
  "Croatian", "Czech", "Danish", "Dutch", "English", "Esperanto", "Estonian",
  "Filipino", "Finnish", "French", "Frisian", "Galician", "Georgian", "German",
  "Greek", "Gujarati", "HaitianCreole", "Hausa", "Hawaiian", "Hebrew", "Hindi",
  "Hmong", "Hungarian", "Icelandic", "Igbo", "Indonesian", "Irish", "Italian",
  "Japanese", "Javanese", "Kannada", "Kazakh", "Khmer", "Korean", "KurdishKurmanji",
  "Kyrgyz", "Lao", "Latin", "Latvian", "Lithuanian", "Luxembourgish", "Macedonian",
  "Malagasy", "Malay", "Malayalam", "Maltese", "Maori", "Marathi", "Mongolian",
  "MyanmarBurmese", "Nepali", "Norwegian", "Odia", "Pashto", "Persian", "Polish",
  "Portuguese", "Punjabi", "Romanian", "Russian", "Samoan", "ScotsGaelic", "Serbian",
  "Sesotho", "Shona", "Sindhi", "Sinhala", "Slovak", "Slovenian", "Somali", "Spanish",
  "Sundanese", "Swahili", "Swedish", "Tajik", "Tamil", "Telugu", "Thai", "Turkish",
  "Ukrainian", "Urdu", "Uyghur", "Uzbek", "Vietnamese", "Welsh", "Xhosa", "Yiddish",
  "Yoruba", "Zulu"
]


v1 = StringVar(main)
v1.set(lt[0])

v2 = StringVar(main)
v2.set(lt[1])

# Label - Translate Language via Voice Commands
Label(main, text="Translate Language via Voice Commands", font=("", 18, "bold"), bg="#C7F8FF", fg="black").place(x=240, y=20)

flag = False

# Canvas for Input and Output Boxes
can = Canvas(main, width=400, height=450, bg="#17C3B2", relief="solid", bd=1, highlightthickness=0)
can.place(x=30, y=80)

can = Canvas(main, width=400, height=450, bg="#17C3B2", relief="solid", bd=1, highlightthickness=0)
can.place(x=-30, y=80)

Label(main, text="Input Box:", font=("", 12, "bold"), bg="#17C3B2", fg="black").place(x=44, y=70)

can.place(x=490, y=80)

Label(main, text="Output Box:", font=("", 12, "bold"), bg="#17C3B2", fg="black").place(x=780, y=60)

# Text boxes for Input and Output
txtbx = Text(main, width=40, height=7, font=("", 12, "bold"), relief="solid", bd=0, highlightthickness=0)
txtbx.place(x=50, y=100)

txtbx2 = Text(main, width=40, height=7, font=("", 12, "bold"), relief="solid", bd=0, highlightthickness=0)
txtbx2.place(x=510, y=100)

translator = Translator()

def speak():
    global txtbx2
    tx = txtbx2.get("1.0", END)
    language = lt.index(v2.get())
    translated = translator.translate(tx, src='auto', dest=lt[language])
    myobj = gTTS(text=translated.text, lang=lt[language], slow=False)

    # Ensure temporary file creation and proper path handling
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
        temp_file_path = temp_file.name
        myobj.save(temp_file_path)

    try:
        song = AudioSegment.from_mp3(temp_file_path)
        play(song)
    except FileNotFoundError:
        print("Error: Could not find temporary audio file")

    # Delete the temporary file after playback
    os.remove(temp_file_path)

async def translate_text():
    global txtbx, txtbx2
    txtbx2.delete("1.0", "end-1c")
    tx = txtbx.get("1.0", END)
    language = v2.get().lower()  # Convert language name to lowercase for API compatibility
    
    try:
        translated = await translator.translate(tx, src='auto', dest=language)
        txtbx2.insert("end-1c", translated.text)
    except Exception as e:
        txtbx2.insert("end-1c", f"Error: {str(e)}")

def translate():
    asyncio.run(translate_text())



def detect():
    global flag, txtbx
    while True:
        if flag:
            print("breaked")
            break

        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)
                audio2 = r.listen(source2)
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()
                txtbx.insert("end-1c", MyText)
        except sr.RequestError as e:
            tkMessageBox.showinfo("warning", "Could not request results; {0}".format(e))
            break
        except sr.UnknownValueError:
            tkMessageBox.showinfo("warning", "unknown error occurred")
            break

def start():
    global flag, b1
    flag = False
    b1["text"] = "Stop Speaking"
    b1["command"] = stop
    td.Thread(target=detect).start()


def stop():
    global flag, b1
    b1["text"] = "Give Voice Input"
    b1["command"] = start
    flag = True


# Button - Give Voice Input
b1 = Button(
    main,
    text="Give Voice Input",
    font=("", 12, "bold"),
    width=35,
    height=1,
    bg="#FEF9EF",
    fg="black",
    command=start,
    relief="solid",
    bd=4,
    highlightthickness=0,
)
b1.place(x=50, y=250)

# Button - Speak Text
Button(
    main,
    text="Speak Text",
    font=("", 12, "bold"),
    width=35,
    height=1,
    bg="#FEF9EF",
    fg="black",
    command=speak,
    relief="solid",
    bd=4,
    highlightthickness=0,
).place(x=510, y=250)

# Button - Translate
Button(
    main,
    text="Translate",
    font=("", 15, "bold"),
    width=71,
    height=3,
    bg="#FEF9EF",
    fg="black",
    command=translate,
    relief="solid",
    bd=3,
    highlightthickness=0,
).place(x=30, y=446)

# Labels - Select Language
Label(main, text="Select Language :", font=("", 12, "bold"), bg="#17C3B2", fg="black").place(x=50, y=300)
Label(main, text="Select Language :", font=("", 12, "bold"), bg="#17C3B2", fg="black").place(x=510, y=300)

# Option Menus - Select Language
o1 = OptionMenu(main, v1, *lt)
o1.config(font=("", 12, "bold"), width=36, bg="#FEF9EF", fg="black", relief="solid", bd=1, highlightthickness=0)
o1.place(x=50, y=340)

o2 = OptionMenu(main, v2, *lt)
o2.config(font=("", 12, "bold"), width=36, bg="#FEF9EF", fg="black", relief="solid", bd=1, highlightthickness=0)
o2.place(x=510, y=340)

main.mainloop()