from deepgram import Deepgram
import asyncio
import os

DEEPGRAM_API_KEY = "api_key"

async def transcribe_verbatim(audio_file):
    dg_client = Deepgram(DEEPGRAM_API_KEY)

    with open(audio_file, 'rb') as audio:
        source = {'buffer': audio, 'mimetype': 'audio/mp3'} 

        response = await dg_client.transcription.prerecorded(
            source,
            {
                'punctuate': True,
                'language': 'en',
                'model': 'general',
                'disfluency': False,
                'filler_words': True,
                'utterances': True,
                'paragraphs': True,
            }
        )

        transcript = response['results']['channels'][0]['alternatives'][0]['transcript']
        print(transcript)

        with open("verbatim_transcript.txt", "w", encoding="utf-8") as f:
            f.write(transcript)

# Run it using the following:
# asyncio.run(transcribe_verbatim("your_audio_file.mp3"))
