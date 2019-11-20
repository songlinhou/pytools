class SpeechSynthesizer:
    def __init__(self):
        from cross_platform import in_which_env,try_import
        # Import the required module for text  
        # to speech conversion

        try:
            from gtts import gTTS 
        except:
            try_import("gtts")

        runtime = in_which_env()

        if runtime == "python":
            try:
                import vlc
            except:
                try_import("vlc")
            import vlc
        

    def available_langs(self):
        from gtts.lang import tts_langs
        return tts_langs()

    def speak(self,text,language="en",autoplay=True):
        from gtts import gTTS
        import os 
            
        # The text that you want to convert to audio 
            
        # Passing the text and language to the engine,  
        # here we have marked slow=False. Which tells  
        # the module that the converted audio should  
        # have a high speed 
        myobj = gTTS(text=text, lang=language, slow=False) 
            
        # Saving the converted audio in a mp3 file named 
        # welcome
        file_to_save = "_speech.mp3"
        myobj.save(file_to_save) 
            
        # Playing the converted file 
        # os.system("mpg321 welcome.mp3") 
        

        if runtime == "python":
            import vlc
            p = vlc.MediaPlayer(file_to_save)
            if(autoplay):
                p.play()
            return p
        else:
            from IPython.display import Audio
            return Audio(filename=file_to_save,autoplay=autoplay)

if __name__ == "__main__":
    ss = SpeechSynthesizer()
    ss.speak("hello there")