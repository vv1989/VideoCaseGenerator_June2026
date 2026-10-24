import os
from PIL import Image

from dotenv import load_dotenv

load_dotenv()

import streamlit as st

from app.services.case_service import CaseService


st.set_page_config(
    page_title="AI Video Case Generator",
    page_icon="🎬",
    layout="wide"
)

# ---------------------------------------------------
# Cache the service so it is created only once
# ---------------------------------------------------
@st.cache_resource
def get_service():
    return CaseService()

st.markdown("""
<style>
            
html,
body,
[data-testid="stAppViewContainer"]{
    background:#ffffff;
    color:#262730;
}

[data-testid="stHeader"]{
    background:#ffffff;
}

[data-testid="stSidebar"]{
    background:#fafafa;
}
            
div.block-container{
    padding-top:1rem;
    padding-left:2rem;
    padding-right:2rem;
    max-width:1100px;
}
@media (max-width:768px){

.block-container{
    padding-left:1rem;
    padding-right:1rem;
}

}
.stButton > button{
    width:100%;
    height:55px;
    border-radius:14px;
    font-size:18px;
    font-weight:600;
    transition:0.2s;
}

.stButton > button:hover{
    transform:translateY(-2px);
}

div[data-testid="stRadio"]{
    padding:15px;
    border-radius:10px;
    background:#f8f9fa;
}

textarea{
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

st.title("🎬 AI Business Video Case Generator")

st.write(
    "Generate realistic AI-powered business case studies with professional narration, actors, images and video."
)

st.divider()

with st.sidebar:

    st.header("⚙ Settings")

    # text_provider = st.selectbox(
    #     "Text Provider",
    #     [
    #         "Groq",
    #         "OpenAI",
    #         "Claude"
    #     ]
    # )

    st.info("Text Provider: Groq")

    st.divider()

    generate_images = st.checkbox(
        "Generate Images",
        value=True
    )

    generate_audio = st.checkbox(
        "Generate Audio",
        value=True
    )

    generate_video = st.checkbox(
        "Generate Video",
        value=True
    )

st.markdown("## 📝 Business Topic")

topic = st.text_area(
    "",
    height=160,
    placeholder="Example:\nA company must decide whether to build software internally or outsource development."
)

if st.button("🚀 Generate Dilemmas"):

    if not topic.strip():
        st.warning("Please enter a business topic.")
        st.stop()

    service = get_service()

    with st.spinner("Generating dilemmas..."):

        dilemmas = service.get_dilemmas(topic)
        print(type(dilemmas))
        print(dilemmas)

    st.session_state["topic"] = topic
    st.session_state["dilemmas"] = dilemmas

    st.success("✅ Dilemmas generated successfully.")

if "dilemmas" in st.session_state:

    st.divider()

    st.subheader("📋 Choose a Dilemma")

    selected_dilemma = st.radio(
        "",
        st.session_state["dilemmas"]
    )

    st.write("")

    if st.button("🎥 Generate Multimedia Case"):

        service = get_service()

        with st.spinner("Generating multimedia case... This may take several minutes."):

            case = service.build_case(
                st.session_state["topic"],
                selected_dilemma
            )
            # st.write(vars(case))



            # =================================================
            # DEBUG: INSPECT ALL GENERATED IMAGES
            # =================================================

            st.subheader("Debug: Generated Scene Images")

            case_id = getattr(case, "case_id", None)

            if case_id:
                image_folder = os.path.join(
                    "generated_cases",
                    case_id,
                    "images"
                )

                st.caption(f"Case ID: {case_id}")
                st.caption(f"Image folder: {os.path.abspath(image_folder)}")

                if os.path.isdir(image_folder):
                    image_files = sorted(
                        filename
                        for filename in os.listdir(image_folder)
                        if filename.lower().endswith(
                            (".png", ".jpg", ".jpeg", ".webp")
                        )
                    )

                    st.write(f"Found {len(image_files)} image files.")

                    if image_files:
                        for filename in image_files:
                            image_path = os.path.join(
                                image_folder,
                                filename
                            )

                            st.markdown(f"**{filename}**")

                            try:
                                with Image.open(image_path) as img:
                                    st.image(
                                        img.copy(),
                                        caption=f"{img.width} × {img.height}",
                                        use_container_width=True
                                    )
                            except Exception as exc:
                                st.error(f"Could not open {filename}: {exc}")
                    else:
                        st.warning("No image files found in this folder.")
                else:
                    st.error("The images folder does not exist.")
            else:
                st.warning("Could not determine the case ID.")

            # =================================================
            # DEBUG: INSPECT INDIVIDUAL SCENE VIDEOS
            # =================================================

            import glob
            import subprocess
            import imageio_ffmpeg

            st.subheader("Debug: Individual Scene Videos")

            if case_id and os.path.isdir(image_folder):
                scene_videos = sorted(
                    glob.glob(
                        os.path.join(
                            "generated_cases",
                            case_id,
                            "images",
                            "scene_*.mp4"
                        )
                    )
                )

                st.write(f"Found {len(scene_videos)} scene videos.")

                if scene_videos:
                    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

                    for scene_video in scene_videos:
                        st.markdown(
                            f"**{os.path.basename(scene_video)}**"
                        )

                        try:
                            result = subprocess.run(
                                [
                                    ffmpeg_exe,
                                    "-hide_banner",
                                    "-loglevel", "error",
                                    "-i", scene_video,
                                    "-frames:v", "1",
                                    "-f", "image2pipe",
                                    "-vcodec", "png",
                                    "-"
                                ],
                                capture_output=True,
                                timeout=15,
                                check=False
                            )

                            if result.returncode == 0 and result.stdout:
                                st.image(
                                    result.stdout,
                                    caption=os.path.basename(scene_video),
                                    width=400
                                )
                            else:
                                st.warning(
                                    f"Could not extract a frame from "
                                    f"{os.path.basename(scene_video)}."
                                )

                        except Exception as exc:
                            st.error(f"Preview error: {exc}")
                else:
                    st.warning(
                        "No scene_*.mp4 files found in the images folder."
                    )

if "case" in st.session_state:

    case = st.session_state["case"]

    st.divider()

    st.subheader("📽 Generated Case")

    st.header(case.title)

    # st.write(f"**Topic:** {case.topic}")

    # st.write(f"**Dilemma:** {case.dilemma}")

    # st.write(f"**Setting:** {case.setting}")

    # video_path = getattr(case, "output_video_path", None)
    video_path = getattr(case, "output_video_path", None) or getattr(case, "video_path", None)

    if video_path and not os.path.isabs(video_path):
        video_path = os.path.abspath(video_path)

    st.write("Current directory:", os.getcwd())
    st.write("Video path:", video_path)
    st.write("Exists:", os.path.exists(video_path) if video_path else False)

    if video_path:

        folder = os.path.dirname(video_path)

        # st.write("Folder:", folder)
        # st.write("Folder exists:", os.path.exists(folder))

        # if os.path.exists(folder):
            # st.write("Files in folder:", os.listdir(folder))

    if video_path and os.path.exists(video_path):

        st.write(
            "Video size (MB):",
            round(os.path.getsize(video_path) / (1024 * 1024), 2)
        )

        with open(video_path, "rb") as f:
            video_bytes = f.read()

        st.video(video_bytes, format="video/mp4")

        st.download_button(
            label="📥 Download Video",
            data=video_bytes,
            file_name="generated_case.mp4",
            mime="video/mp4",
            use_container_width=True,
            key="download_generated_video",
        )

    else:
        st.error("Video file not found.")
