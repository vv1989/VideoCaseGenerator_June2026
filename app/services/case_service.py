from app.pipelines.case_pipeline import CasePipeline
from app.infrastructure.text.text_llm import TextLLM
from app.infrastructure.images.image_generator import ImageGenerator
from app.infrastructure.audio.voice_generator import VoiceGenerator
from app.infrastructure.video.movie_generator import MovieGenerator


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

        movie_generator = MovieGenerator(
            provider="moviepy",
            background_music="app/assets/audio/background_music.mp3"
        )

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
        return self.pipeline.build_multimedia_case(
            topic=topic,
            dilemma=dilemma,
            generate_images=True,
            generate_audio=True,
            generate_video=True
        )