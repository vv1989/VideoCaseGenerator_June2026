import os

class GenerateVideo:

    def __init__(self, movie_generator):

        self.movie_generator = movie_generator

    # ==================================================
    # 🎬 VIDEO GENERATION
    # ==================================================

    def execute(self, case):

        print("\n🎬 ===== GENERATING VIDEO =====")

        image_folder = os.path.join(
            "generated_cases",
            case.case_id,
            "images"
        )

        audio_folder = os.path.join(
            "generated_cases",
            case.case_id,
            "audio"
        )

        output_file = os.path.join(
            "generated_cases",
            case.case_id,
            "movie.mp4"
        )

        final_video = self.movie_generator.create_movie_ffmpeg(
            case=case,
            image_folder=image_folder,
            audio_folder=audio_folder,
            output_file=output_file
        )

        print(
            f"\n🎬 Video saved: {final_video}"
        )

        print("RETURNING:", final_video)

        return final_video

