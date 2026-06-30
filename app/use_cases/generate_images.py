import os

class GenerateImages:

    def __init__(self, image_generator):

        self.image_generator = image_generator

    # ==================================================
    # 🎨 IMAGE GENERATION
    # ==================================================

    def execute(self, case):

        print("\n🎨 ===== GENERATING IMAGES =====")

        output_dir = os.path.join(
            "generated_cases",
            case.case_id,
            "images"
        )

        os.makedirs(
            output_dir,
            exist_ok=True
        )

        visual_plan = case.visual_plan

        # ------------------------------------------
        # Cover image
        # ------------------------------------------

        cover_prompt = visual_plan.get(
            "cover_image"
        )

        if cover_prompt:

            filepath = os.path.join(
                output_dir,
                "cover.png"
            )

            self.image_generator.generate_and_save(
                prompt=cover_prompt,
                filepath=filepath,
                image_type="cover",
                template=case.template
            )
            case.generated_images["cover"] = filepath

            print(
                f"✅ Cover image saved: {filepath}"
            )

        # ------------------------------------------
        # Actor images
        # ------------------------------------------

        for actor in visual_plan.get(
            "actors",
            []
        ):

            actor_name = actor.get(
                "name"
            )

            generated_actor = next(
                a for a in case.actors
                if a.name == actor_name
            )

            prompt = actor.get(
                "image_prompt"
            )

            if not prompt:
                continue

            safe_name = (
                actor_name
                .lower()
                .replace(" ", "_")
            )

            filepath = os.path.join(
                output_dir,
                f"actor_{safe_name}.png"
            )

            self.image_generator.generate_and_save(
                prompt=prompt,
                filepath=filepath,
                image_type=generated_actor.template_actor_id,
                template=case.template
            )
            case.generated_images[
                f"actor_{safe_name}"
            ] = filepath

            print(
                f"✅ Actor image saved: {filepath}"
            )

        closing_prompt = visual_plan.get(
            "closing_image"
        )

        if closing_prompt:

            filepath = os.path.join(
                output_dir,
                "closing.png"
            )

            self.image_generator.generate_and_save(
                prompt=closing_prompt,
                filepath=filepath,
                image_type="closing",
                template=case.template
            )
            case.generated_images[
                "closing"
            ] = filepath

            print(
                f"✅ Closing image saved: {filepath}"
            )

        print(
            "\n🎉 All images generated successfully"
        )

        print(
            f"📂 Saved to: {output_dir}"
        )

