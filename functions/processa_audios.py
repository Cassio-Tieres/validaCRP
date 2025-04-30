import speech_recognition as sr
from pydub import AudioSegment

def transcreve_audio(file_path):
    file_path = file_path.replace('/', '\\')
    print(file_path)
    with open (file_path, 'rb') as audio_file:
        audio = AudioSegment.from_file(audio_file, format="ogg")
        audio.export("uploads/temp.wav", format="wav")
    
    with sr.AudioFile("uploads/temp.wav") as source:
        audio = sr.Recognizer().record(source)
        try:
            texto = sr.Recognizer().recognize_google(audio, language="pt-BR")
            return texto
        except sr.UnknownValueError:
            return "Não consegui entender o áudio."
        except sr.RequestError as e:
            return f"Erro ao solicitar resultados do Google Speech Recognition: {e}"