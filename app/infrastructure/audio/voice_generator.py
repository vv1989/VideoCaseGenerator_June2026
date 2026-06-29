import asyncio
import os

import edge_tts
import nest_asyncio


nest_asyncio.apply()


class VoiceGenerator:

    DEFAULT_VOICES = {

        "narrator":
            "en-GB-RyanNeural",

        "actor1":
            "en-GB-SoniaNeural",

        "actor2":
            "en-IN-PrabhatNeural",

        "actor3":
            "en-US-AndrewNeural"
    }

    # ==================================================
    # INIT
    # ==================================================

    def __init__(
        self,
        provider="edge_tts",
        debug=True
    ):

        self.provider = provider
        self.debug = debug

        if self.provider != "edge_tts":

            raise ValueError(
                f"Unsupported provider: "
                f"{provider}"
            )

        if self.debug:

            print(
                "\n🎤 VoiceGenerator initialized"
            )

            print(
                f"🔧 Provider: "
                f"{self.provider}"
            )

    # ==================================================
    # INTERNAL
    # ==================================================

    async def _save_audio(
        self,
        text,
        voice,
        filepath,
        rate="+0%"
    ):

        communicate = edge_tts.Communicate(
            text=text,
            voice=voice,
            rate=rate
        )

        await communicate.save(
            filepath
        )

    # ==================================================
    # GENERATE AUDIO
    # ==================================================

    def generate(
        self,
        text,
        voice_key,
        filepath
    ):

        os.makedirs(
            os.path.dirname(filepath),
            exist_ok=True
        )

        voice = self.DEFAULT_VOICES.get(
            voice_key,
            self.DEFAULT_VOICES[
                "narrator"
            ]
        )

        loop = asyncio.get_event_loop()

        rate = "+0%"

        if voice_key == "narrator":

            rate = "-10%"

        loop.run_until_complete(

            self._save_audio(
                text=text,
                voice=voice,
                filepath=filepath,
                rate=rate
            )

        )
        print(
            f"🎤 Audio saved: "
            f"{filepath}"
        )

        return filepath

    # ==================================================
    # INFO
    # ==================================================

    def __repr__(self):

        return (
            f"VoiceGenerator("
            f"provider={self.provider})"
        )

