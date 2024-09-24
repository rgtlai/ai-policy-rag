from ragas.testset.generator import TestsetGenerator
from ragas.testset.evolutions import simple, reasoning, multi_context
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
#from langchain.embeddings import HuggingFaceEmbeddings
import sys
import os
from dotenv import load_dotenv
load_dotenv()
current_dir = os.path.dirname(os.path.abspath(__file__))
sys_dir = os.path.abspath(os.path.join(current_dir, '../..'))
sys.path.append(sys_dir)
from src.vectorstore.chunk_upload import read_files_in_folder
PDF_FOLDER = os.path.abspath(os.path.join('..', 'vectorstore', 'pdfs'))

documents = read_files_in_folder(PDF_FOLDER)


generator_llm = ChatOpenAI(model="gpt-3.5-turbo")
critic_llm = ChatOpenAI(model="gpt-4o-mini")
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
#3embeddings_ft = HuggingFaceEmbeddings(model_name="rgtlai/ai-policy-ft")

generator = TestsetGenerator.from_langchain(
    generator_llm,
    critic_llm,
    embeddings
)

distributions = {
    simple: 0.5,
    multi_context: 0.4,
    reasoning: 0.1
}