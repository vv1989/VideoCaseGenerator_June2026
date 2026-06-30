import os
import shutil
import base64

from openai import OpenAI
from google import genai


class ImageGenerator:

    def __init__(
        self,
        provider="gemini",
        api_key=None,
        debug=True
    ):

        self.provider = provider.lower()
        self.debug = debug

        # ==========================================
        # OPENAI
        # ==========================================

        if self.provider == "openai":

            self.client = OpenAI(
                api_key=api_key
                or os.getenv(
                    "OPENAI_API_KEY"
                )
            )

            self.model = "gpt-image-1"

        # ==========================================
        # GEMINI
        # ==========================================

        elif self.provider == "gemini":

            self.client = genai.Client(
                api_key=api_key
                or os.getenv(
                    "GEMINI_API_KEY"
                )
            )

            self.model = (
                "imagen-4.0-generate-001"
            )

        # ==========================================
        # ASSETS
        # ==========================================

        elif self.provider == "assets":

            self.asset_folder = (
                "app/assets/images"
            )

            self.model = (
                "local_assets"
            )

            self._actor_counter = 0

        # ==========================================
        # UNSUPPORTED
        # ==========================================

        else:

            raise ValueError(
                f"Unsupported provider: "
                f"{provider}"
            )

        if self.debug:

            print(
                "\n🎨 ImageGenerator initialized"
            )

            print(
                f"🔧 Provider: "
                f"{self.provider}"
            )

            print(
                f"🧠 Model: "
                f"{self.model}"
            )

    # ==================================================
    # GENERATE IMAGE
    # ==================================================

    def generate_and_save(
        self,
        prompt,
        filepath,
        image_type=None,
        template=None,
        size="1024x1024"
    ):
        print("\n🎨 Generating image...")
        print(f"📁 Output: {filepath}")

        os.makedirs(
            os.path.dirname(filepath),
            exist_ok=True
        )

        # ==========================================
        # OPENAI
        # ==========================================

        if self.provider == "openai":

            response = (
                self.client.images.generate(
                    model=self.model,
                    prompt=prompt,
                    size=size
                )
            )

            image_bytes = (
                base64.b64decode(
                    response.data[0].b64_json
                )
            )

        # ==========================================
        # GEMINI
        # ==========================================

        elif self.provider == "gemini":

            response = (
                self.client.models.generate_images(
                    model=self.model,
                    prompt=prompt
                )
            )

            image_bytes = (
                response.generated_images[0]
                .image
                .image_bytes
            )

        # ==========================================
        # ASSETS
        # ==========================================

        elif self.provider == "assets":

            filename = os.path.basename(
                filepath
            ).lower()

            # --------------------------------------
            # COVER
            # --------------------------------------

            if "cover" in filename:

                asset_name = "cover.png"

            # --------------------------------------
            # CLOSING
            # --------------------------------------

            elif "closing" in filename:

                asset_name = "closing.png"

            # --------------------------------------
            # ACTORS
            # --------------------------------------

            elif filename.startswith(
                "actor"
            ):

                actor_files = [
                    "actor1.png",
                    "actor2.png",
                    "actor3.png"
                ]

                asset_name = actor_files[
                    self._actor_counter
                    % len(actor_files)
                ]

                self._actor_counter += 1

            # --------------------------------------
            # FALLBACK
            # --------------------------------------

            else:

                asset_name = "cover.png"

            source_file = os.path.join(
                self.asset_folder,
                asset_name
            )

            if not os.path.exists(
                source_file
            ):

                raise FileNotFoundError(
                    f"Asset image not found: "
                    f"{source_file}"
                )

            shutil.copy(
                source_file,
                filepath
            )

            print(
                f"✅ Copied asset image "
                f"({asset_name}) -> "
                f"{filepath}"
            )

            return filepath

        # ==========================================
        # SAVE FILE
        # ==========================================

        with open(
            filepath,
            "wb"
        ) as f:

            f.write(image_bytes)

        print(
            f"✅ Saved image: "
            f"{filepath}"
        )

        return filepath

    # ==================================================
    # STRING REPRESENTATION
    # ==================================================

    def __repr__(self):

        return (
            f"ImageGenerator("
            f"provider={self.provider}, "
            f"model={self.model})"
        )