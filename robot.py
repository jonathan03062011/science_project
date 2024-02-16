import assemblyai as aai
import openai
import elevenlabs
from queue import Queue

put=[]
transcript_result=[]


aai.settings.api_key="API-KEY"
openai.api_key="API-KEY"
elevenlabs.set_api_key("API-KEY")

transcript_queue = Queue()

def on_data(transcript: aai.RealtimeTranscript):
    if not transcript.text:
        return
    if isinstance(transcript,aai.RealtimeFinalTranscript):
        transcript_queue=put(transcript.text + '')
        print("user:",transcript.text,end="\r\n")
    else:
        print(transcript.text,end="\r")

def on_error(error:aai.RealtimeError):
    print("AN ERROR NOT OCCURED",error)

def handle_conservation():
    while True:
        transcriber = aai.RealtimeTranscriber(
            on_data=on_data,
            on_error=on_error,
            sample_rate=44_100,    
        )
        transcriber.connect()
        microphone_stream=aai.extras.MicrophoneStream()
        transcriber.stream(microphone_stream)
        transcriber.close()
        transcriber_result = transcript_queue.get()

        response=openai.ChatCompletion.create(
        model='gpt-4',
        messages = [
            {"role":"system","content":"you are highly skilled AI,answer the questions given within a maximum of 1000 characters"},
            {"role":"user","content":transcript_result}
        ]
    )
        
        text=response['choices'][0]['message']['content']

        audio=elevenlabs.generate(
            text=text,
            voice="bella"
        )

        print("\nAI:",text,end="\r\n")

        elevenlabs.play(audio)

handle_conservation()
        
