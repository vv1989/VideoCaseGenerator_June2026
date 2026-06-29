
from app.pipelines.case_pipeline import CasePipeline
from infrastructure.llm.local_llm import LocalLLM
from infrastructure.llm.openai_llm import OpenAILLM
from infrastructure.config.settings import settings

import os
print("🚨 RUNNING CLI MAIN:", os.path.abspath(__file__))

def get_llm():
    if settings.LLM_PROVIDER == "openai":
        return OpenAILLM(settings.OPENAI_API_KEY, settings.OPENAI_BASE_URL)
    return LocalLLM(settings.LOCAL_BASE_URL)

def main():
    llm = get_llm()
    pipeline = CasePipeline(llm)

    topic = input("Enter topic: ")
    dilemmas = pipeline.generate_dilemmas(topic)

    print("\nSuggested Dilemmas:")
    for i, d in enumerate(dilemmas):
        print(f"{i+1}. {d}")

    choice = int(input("Select dilemma (1-5): ")) - 1
    case = pipeline.generate_case(topic, dilemmas[choice])

    print("\nGenerated Case:\n")
    print(case)

if __name__ == "__main__":
    main()
