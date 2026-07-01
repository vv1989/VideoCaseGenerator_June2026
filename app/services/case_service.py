from app.pipelines.case_pipeline import CasePipeline
from app.infrastructure.text.text_llm import TextLLM
from app.infrastructure.images.image_generator import ImageGenerator
from app.infrastructure.audio.voice_generator import VoiceGenerator
from app.infrastructure.video.movie_generator import MovieGenerator
from app.infrastructure.config.template_loader import TemplateLoader

import os
import random

class CaseService:

    def __init__(self):

        text_llm = TextLLM(
            provider="groq",
            api_key=None
        )

        image_generator = ImageGenerator(
            provider="assets"
        )

        voice_generator = VoiceGenerator(
            provider="edge_tts"
        )

        MovieGenerator(
            provider="moviepy",
            background_music=get_random_background_music()
        )
        self.template_loader = TemplateLoader()

        self.pipeline = CasePipeline(
            text_llm=text_llm,
            image_generator=image_generator,
            voice_generator=voice_generator,
            movie_generator=movie_generator,
            max_retries=1
        )

    def get_dilemmas(self, topic):
        return self.pipeline.generate_dilemmas(topic)

    def build_case(self, topic, dilemma):
        # template = self.template_loader.load("template_001")
        template = self.template_loader.load_random()
        return self.pipeline.build_multimedia_case(
            topic=topic,
            dilemma=dilemma,
            template=template,
            generate_images=True,
            generate_audio=True,
            generate_video=True
        )
    
    def get_random_background_music():

        music_folder = "app/assets/audio/background_music"

        music_files = [
            os.path.join(music_folder, f)
            for f in os.listdir(music_folder)
            if f.endswith(".mp3")
        ]

        return random.choice(music_files)