import os
from uuid import uuid4

def run_env() -> None:
    os.environ["GOOGLE_API_KEY"] = "AIzaSyBOT6evi0_a1kiY7SOlqaHj-gaZRFL2LIc"
    unique_id = uuid4().hex[0:8]
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = f"Tracing Walkthrough - {unique_id}"
    os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
    os.environ["LANGCHAIN_API_KEY"] = "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"
    os.environ["GEN_MODEL"] = "gemini-2.0-flash-exp"
    os.environ["LANGCHAIN_ZEP_KEY"] = "z_1dWlkIjoiYjkzZTMwODctOWE3OC00OGQ3LTk0OGEtMzVhZjVmMDc0ZWViIn0.tJLNEkPNqVH8x_ddZKYmO_C9BZnH160BMTghvsNdwXrVOhJYYjMpbEOezSaInb4psia_rduXz60Dg3B33ethHg"
