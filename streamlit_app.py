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
/* Keep the application readable even when the browser/device prefers dark mode. */
:root {
    color-scheme: light;
}

html, body, [data-testid="stApp"], [data-testid="stAppViewContainer"],
[data-testid="stMain"], [data-testid="stMainBlockContainer"] {
    background: #ffffff !important;
    color: #262730 !important;
}

[data-testid="stHeader"] {
    background: #ffffff !important;
}

[data-testid="stSidebar"],
[data-testid="stSidebar"] > div {
    background: #f7f8fa !important;
    color: #262730 !important;
}

[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] label,
.stText,
.stCaption,
h1, h2, h3, h4, h5, h6,
label {
    color: #262730;
}

div.block-container {
    padding-top: 1rem;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 1100px;
}

@media (max-width: 768px) {
    div.block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
}

/* Text inputs and text areas */
div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div,
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background: #ffffff !important;
    color: #262730 !important;
    border-color: #c9cdd4 !important;
    border-radius: 10px !important;
}

input, textarea {
    color: #262730 !important;
    caret-color: #262730 !important;
}

input::placeholder, textarea::placeholder {
    color: #686d78 !important;
    opacity: 1 !important;
}

/* Dropdowns and select controls */
div[data-baseweb="select"] > div {
    background: #ffffff !important;
    color: #262730 !important;
    border-color: #c9cdd4 !important;
}

div[data-baseweb="popover"],
div[data-baseweb="menu"],
ul[role="listbox"],
li[role="option"] {
    background: #ffffff !important;
    color: #262730 !important;
}

/* Radio and checkbox areas */
div[data-testid="stRadio"] {
    padding: 15px;
    border-radius: 10px;
    background: #f4f6f8 !important;
}

div[data-testid="stRadio"] *,
div[data-testid="stCheckbox"] *,
div[data-testid="stToggle"] * {
    color: #262730;
}

/* Buttons */
.stButton > button,
.stDownloadButton > button {
    width: 100%;
    min-height: 48px;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 600;
    color: #262730 !important;
    background: #f2f3f5 !important;
    border: 1px solid #c9cdd4 !important;
    transition: 0.2s;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: #e7e9ed !important;
    border-color: #aeb4bf !important;
    transform: translateY(-1px);
}

/* Keep alerts, code blocks, and bordered panels legible */
[data-testid="stAlert"] {
    color: #262730 !important;
}

[data-testid="stAlert"] * {
    color: inherit;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: #d9dde4 !important;
}

pre, code {
    color: #262730;
}

hr {
    border-color: #e0e3e8 !important;
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
            # Persist the generated case across Streamlit reruns so the
            # final-video display block below can access it.
            st.session_state["case"] = case

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
