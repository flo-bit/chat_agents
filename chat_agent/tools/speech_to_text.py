import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)


def transcribe(path: str, language: str = None, prompt: str = None):
    audio_file = open(path, "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        language=language,
        prompt=prompt,
    )
    return transcript.text


async def speech_to_text(agent, path: str, language: str = None, prompt: str = None):
    content = transcribe(path, language, prompt)
    return f"speech to text transcription of file at {path}\nSTART\n{content}\nEND"


async def speeches_to_texts(agent, paths: list, language: str = None, no_prompt: bool = False):
    content = ""
    last_content = ""
    for path in paths:
        if no_prompt:
            last_content = ""
        last_content = await transcribe(path, language, last_content)
        content += f"speech to text transcription of file at {path}\nSTART\n{last_content}\nEND\n\n"

    return content

tool_speech_to_text = {
    "info": {
        "type": "function",
        "function": {
            "name": "speech_to_text",
            "description": "Transcribes an audio file to text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to audio file to transcribe, relative to the current working directory"
                    },
                    "language": {
                        "type": "string",
                        "description": "optional 2 letter language code, of the language spoken in the audio file",
                    },
                    "prompt": {
                        "type": "string",
                        "description": "optional prompt to use for transcription",
                    },
                },
                "required": ["text", "path"],
            },
        }
    },
    "function": speech_to_text,
}

tool_speeches_to_texts = {
    "info": {
        "type": "function",
        "function": {
            "name": "speeches_to_texts",
            "description": "Transcribes multiple audio files to text, will use the output of the previous file as prompt for the next file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "paths": {
                        "type": "array",
                        "description": "Paths to audio files to transcribe, relative to the current working directory",
                        "items": {
                            "type": "string",
                        }
                    },
                    "language": {
                        "type": "string",
                        "description": "optional 2 letter language code, of the language spoken in the audio files",
                    },
                    "no_prompt": {
                        "type": "boolean",
                        "description": "optional boolean, if true, will not use the output of the previous file as prompt for the next file.",
                    },
                },
                "required": ["paths"],
            },
        }
    },
    "function": speeches_to_texts,
}
