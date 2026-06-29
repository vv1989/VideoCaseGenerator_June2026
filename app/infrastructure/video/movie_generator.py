import os
import json

import subprocess
import imageio_ffmpeg

from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    ColorClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips,
    concatenate_audioclips
)

from moviepy.audio.AudioClip import (
    CompositeAudioClip
)

from moviepy.video.fx.all import (
    fadein,
    fadeout
)

from moviepy.audio.fx.all import (
    audio_fadein,
    audio_fadeout
)

from PIL import (
    Image,
    ImageDraw,
    ImageFont
)

import numpy as np

class MovieGenerator:

    def __init__(
        self,
        provider="moviepy",
        background_music="app/assets/audio/background_music.mp3",
        debug=True
    ):

        self.provider = provider
        self.background_music = background_music
        self.debug = debug

        self.background_music_clip = None

        if os.path.exists(self.background_music):

            self.background_music_clip = AudioFileClip(
                self.background_music
            )

        if self.provider != "moviepy":

            raise ValueError(
                f"Unsupported provider: "
                f"{provider}"
            )

        if self.debug:

            print(
                "\n🎬 MovieGenerator initialized"
            )

            print(
                f"🔧 Provider: "
                f"{self.provider}"
            )

    # ==================================================
    # CREATE OVERLAY
    # ==================================================

    def create_actor_overlay(
        self,
        actor_name,
        actor_role,
        output_path = None
    ):

        width = 900
        height = 120

        img = Image.new(
            "RGBA",
            (width, height),
            (0, 0, 0, 180)
        )

        draw = ImageDraw.Draw(img)

        try:

            name_font = ImageFont.truetype(
                "arial.ttf",
                40
            )

            role_font = ImageFont.truetype(
                "arial.ttf",
                28
            )

        except:

            name_font = ImageFont.load_default()
            role_font = ImageFont.load_default()

        draw.text(
            (20, 15),
            actor_name,
            fill="white",
            font=name_font
        )

        draw.text(
            (20, 65),
            actor_role,
            fill="white",
            font=role_font
        )

        return np.array(img)
    
    # ==================================================
    # CREATE MOVIE
    # ==================================================

    def create_movie(
        self,
        case,
        image_folder,
        audio_folder,
        output_file
    ):

        clips = []

        available_audio = set(os.listdir(audio_folder))
        available_images = set(os.listdir(image_folder))

        narrator_scenes = [

            scene

            for scene in case.scenes

            if scene.speaker.lower()
            == "narrator"
        ]

        last_narrator_id = (
            narrator_scenes[-1]
            .scene_id
        )

        actor_lookup = {

            actor.actor_id: actor

            for actor in case.actors
        }

        introduced_actors = set()

        # ------------------------------------------
        # Build Clips
        # ------------------------------------------

        for scene in case.scenes:

            first_appearance = False

            if scene.actor_id is not None:

                if scene.actor_id not in introduced_actors:

                    first_appearance = True

                    introduced_actors.add(
                        scene.actor_id
                    )

            audio_path = os.path.join(

                audio_folder,

                f"{scene.scene_id}.mp3"
            )

            audio_filename = f"{scene.scene_id}.mp3"

            if audio_filename not in available_audio:

                raise FileNotFoundError(
                    f"Missing audio file: "
                    f"{audio_path}"
                )
            
            audio_clip = AudioFileClip(
                audio_path
            )

            # Small delay after image appears
            audio_clip = audio_clip.set_start(
                0.10
            )
            # ----------------------------------
            # Audio Fade In / Out
            # ----------------------------------

            audio_clip = audio_fadein(
                audio_clip,
                0.15
            )

            audio_clip = audio_fadeout(
                audio_clip,
                0.15
            )

            duration = (
                audio_clip.duration + 0.10
            )

            FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

            # ----------------------------------
            # Select Image
            # ----------------------------------

            if scene.speaker.lower() == "narrator":

                if (
                    scene.scene_id
                    == last_narrator_id
                ):

                    image_name = (
                        "closing.png"
                    )

                else:

                    image_name = (
                        "cover.png"
                    )

            else:

                actor_name = (
                    scene.speaker
                    .lower()
                    .replace(" ", "_")
                )

                image_name = (
                    f"actor_{actor_name}.png"
                )

            image_path = os.path.join(
                image_folder,
                image_name
            )

            if image_name not in available_images:

                raise FileNotFoundError(
                    f"Missing image file: "
                    f"{image_path}"
                )

            print(
                f"🖼️ Using image: "
                f"{image_name}"
            )

            scene_output = os.path.join(
                image_folder,
                f"scene_{scene.scene_id}.mp4"
            )

            command = [

                FFMPEG,

                "-y",

                "-loop", "1",

                "-i", image_path,

                "-itsoffset", str(AUDIO_DELAY),

                "-i", audio_path,

                "-t", str(scene_duration),

                "-c:v", "libx264",

                "-preset", "ultrafast",

                "-tune", "stillimage",

                "-pix_fmt", "yuv420p",

                "-c:a", "aac",

                scene_output

            ]

            result = subprocess.run(
                command,
                capture_output=True,
                text=True
            )

            print("Concat return code:", result.returncode)
            print("movie.mp4 exists:", os.path.exists(output_file))

            if result.returncode != 0:
                raise RuntimeError(result.stderr)

            print(result.stdout)
            print(result.stderr)

            clip = (
                ImageClip(
                    image_path
                )
                .set_duration(
                    duration
                )
                .set_audio(
                    audio_clip
                )
            )

            if first_appearance:

                actor = actor_lookup[
                    scene.actor_id
                ]

                title_bg = (
                    ColorClip(
                        size=(900, 120),
                        color=(0, 0, 0)
                    )
                    .set_opacity(0.6)
                    .set_duration(2)
                    .set_position(
                        (50, 850)
                    )
                )

                overlay_image = self.create_actor_overlay(
                    actor_name=actor.name,
                    actor_role=actor.role,
                    output_path=None
                )

                overlay_clip = (
                    ImageClip(overlay_image)
                    .set_duration(2)
                    .set_position(
                        (50, 850)
                    )
                )

                clip = CompositeVideoClip(
                    [
                        clip,
                        overlay_clip
                    ]
                )     
                   
            # ----------------------------------
            # Visual Fade In / Out
            # ----------------------------------

            # clip = fadein(clip,0.4)

            # clip = fadeout(clip,0.4)

            clips.append(
                clip
            )

        # ------------------------------------------
        # Add Transitions
        # ------------------------------------------

        video_clips = []

        for i, clip in enumerate(clips):

            video_clips.append(
                clip
            )

            # Add transition after every scene
            # except the last one

            if i < len(clips) - 1:

                transition = ColorClip(

                    size=clip.size,

                    color=(0, 0, 0),

                    duration=0.15

                )

                video_clips.append(
                    transition
                )

        # ------------------------------------------
        # Concatenate Clips
        # ------------------------------------------

        print("\n===== CLIP DEBUG =====")

        for i, clip in enumerate(video_clips):
            print(
                i,
                "duration =", clip.duration,
                "size =", clip.size,
                "start =", clip.start,
                "end =", clip.end
            )

        print("======================\n")

        final_video = (
            concatenate_videoclips(

                video_clips,

                method="compose"

            )
        )

    # ------------------------------------------
    # Background Music
    # ------------------------------------------

        target_duration = (
            final_video.duration + 2
        )

        if self.background_music_clip is not None:

            # Make an independent copy
            music = self.background_music_clip.copy()

            music = music.volumex(
                0.20
            )

            # ----------------------------------
            # Trim or Loop Music
            # ----------------------------------

            if (
                music.duration
                >= target_duration
            ):

                music = music.subclip(
                    0,
                    target_duration
                )

            else:

                # Repeat music until
                # it reaches target duration

                loops = int(
                    target_duration
                    // music.duration
                ) + 1

                music = concatenate_audioclips(

                    [music] * loops

                ).subclip(
                    0,
                    target_duration
                )

            # ----------------------------------
            # Combine Narration + Music
            # ----------------------------------

            final_audio = (
                CompositeAudioClip(
                    [
                        final_video.audio,
                        music
                    ]
                )
            )

            final_audio = (
                final_audio.set_duration(
                    target_duration
                )
            )

            final_video = (
                final_video.set_audio(
                    final_audio
                )
            )

            final_video = (
                final_video.set_duration(
                    target_duration
                )
            )

        else:

            print(
                f"⚠️ Background music not found: "
                f"{self.background_music}"
            )
        # ------------------------------------------
        # Fade Entire Movie In / Out
        # ------------------------------------------

        final_video = fadein(
            final_video,
            1.0
        )

        final_video = fadeout(
            final_video,
            1.0
        )

        # ------------------------------------------
        # Export
        # ------------------------------------------

        os.makedirs(
            os.path.dirname(
                output_file
            ),
            exist_ok=True
        )

        final_video.write_videofile(

            output_file,

            fps=24,

            codec="libx264",

            audio_codec="aac",

            threads=os.cpu_count(),

            preset="ultrafast"
        )

        print(
            f"\n🎬 Video saved: "
            f"{output_file}"
        )

        return output_file

    # ==================================================
    # INFO
    # ==================================================

    def __repr__(self):

        return (
            f"MovieGenerator("
            f"provider={self.provider})"
        )
    
    def create_movie_ffmpeg(
        self,
        case,
        image_folder,
        audio_folder,
        output_file
    ):

        import os
        import subprocess
        import imageio_ffmpeg

        FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

        os.makedirs(
            os.path.dirname(output_file),
            exist_ok=True
        )

        narrator_scenes = [
            scene
            for scene in case.scenes
            if scene.speaker.lower() == "narrator"
        ]

        last_narrator_id = narrator_scenes[-1].scene_id

        actor_lookup = {

            actor.actor_id: actor

            for actor in case.actors

        }

        introduced_actors = set()

        AUDIO_DELAY = 0.75
        TRANSITION_DURATION = 0.15
        INTRO_DURATION = 2.0
        ENDING_DURATION = 2.0

        total_duration = 0

        for scene in case.scenes:

            first_appearance = False

            if scene.actor_id is not None:

                if scene.actor_id not in introduced_actors:

                    first_appearance = True

                    introduced_actors.add(
                        scene.actor_id
                    )

            audio_path = os.path.join(
                audio_folder,
                f"{scene.scene_id}.mp3"
            )

            audio_duration = AudioFileClip(audio_path).duration

            scene_duration = audio_duration + AUDIO_DELAY

            total_duration += scene_duration

            if scene.speaker.lower() == "narrator":

                if scene.scene_id == last_narrator_id:
                    image_name = "closing.png"
                else:
                    image_name = "cover.png"

            else:

                actor_name = (
                    scene.speaker
                    .lower()
                    .replace(" ", "_")
                )

                image_name = f"actor_{actor_name}.png"

            image_path = os.path.join(
                image_folder,
                image_name
            )

            overlay_path = None

            if first_appearance:

                actor = actor_lookup[
                    scene.actor_id
                ]

                overlay = self.create_actor_overlay(

                    actor_name=actor.name,

                    actor_role=actor.role

                )

                overlay_path = os.path.join(

                    image_folder,

                    f"overlay_{scene.actor_id}.png"

                )

                Image.fromarray(
                    overlay
                ).save(
                    overlay_path
                )

            scene_output = os.path.join(
                image_folder,
                f"scene_{scene.scene_id}.mp4"
            )

            if first_appearance:

                command = [

                    FFMPEG,

                    "-y",

                    "-loop", "1",

                    "-i", image_path,

                    "-i", overlay_path,

                    "-i", audio_path,

                    "-filter_complex",

                    "[0:v][1:v]overlay=50:850:enable='between(t,0,2)'",

                    "-c:v", "libx264",

                    "-preset", "ultrafast",

                    "-tune", "stillimage",

                    "-pix_fmt", "yuv420p",

                    "-shortest",

                    "-af",

                    f"adelay={int(AUDIO_DELAY*1000)}|{int(AUDIO_DELAY*1000)}",

                    "-c:a", "aac",

                    scene_output

                ]

            else:

                command = [

                    FFMPEG,

                    "-y",

                    "-loop", "1",

                    "-i", image_path,

                    "-i", audio_path,

                    "-c:v", "libx264",

                    "-preset", "ultrafast",

                    "-tune", "stillimage",

                    "-pix_fmt", "yuv420p",

                    "-shortest",

                    "-af",

                    f"adelay={int(AUDIO_DELAY*1000)}|{int(AUDIO_DELAY*1000)}",

                    "-c:a", "aac",

                    scene_output

                ]

            result = subprocess.run(
                command,
                capture_output=True,
                text=True
            )

            print(result.stdout)
            print(result.stderr)

        target_duration = total_duration + 6

        concat_file = os.path.join(
            image_folder,
            "files.txt"
        )

        with open(concat_file, "w") as f:

            for scene in case.scenes:

                scene_video = os.path.join(
                    image_folder,
                    f"scene_{scene.scene_id}.mp4"
                )

                # FFmpeg prefers forward slashes
                f.write(
                    f"file 'scene_{scene.scene_id}.mp4'\n"
                )
                
        command = [

            FFMPEG,

            "-y",

            "-f", "concat",

            "-safe", "0",

            "-i", concat_file,

            "-c", "copy",

            output_file

        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        print(result.stdout)
        print(result.stderr)

        print("🎬 Final movie created.")

        music_file = self.background_music

        if not os.path.exists(music_file):
            raise FileNotFoundError(music_file)

        print(music_file)
        
        temp_output = output_file.replace(
            ".mp4",
            "_music.mp4"
        )        

        command = [

            FFMPEG,

            "-y",

            "-i", output_file,

            "-stream_loop", "-1",

            "-i", music_file,

            "-filter_complex",

            "[1:a]volume=0.20[a1];[0:a][a1]amix=inputs=2:duration=longest",

            "-c:v", "copy",

            "-c:a", "aac",

            "-t",
            str(target_duration),

            temp_output

        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        print(result.stdout)
        print(result.stderr)

        print("FFmpeg return code:", result.returncode)
        print("movie.mp4 exists:", os.path.exists(output_file))
        print("movie_music.mp4 exists:", os.path.exists(temp_output))

        if result.returncode != 0:
            raise RuntimeError(
                f"FFmpeg failed:\n{result.stderr}"
            )

        return temp_output