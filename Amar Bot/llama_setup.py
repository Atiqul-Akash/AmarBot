from llama_cpp import Llama

llm = Llama(
    model_path=r"YOUR_MODEL_PATH_HERE",
    n_ctx=8192, #Token Size
    verbose=False #Logs ON/OFF
)
