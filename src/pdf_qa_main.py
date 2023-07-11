"""This file creates the pdf chat qa class to help with pdf chat operations."""
import os
from pathlib import Path
from langchain.chains import ConversationalRetrievalChain
# to import open source model in future
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import Chroma
import shutil

class ChatPDF:
    # pylint: disable = too-many-instance-attributes
    """Chatbot class for Q-A over pdf.

    Args:
        model_type: Specifies the type of language model being used.
        api_key: API key required for accessing the language model.
        pdf_path: Path to the user-uploaded PDF file.
    """

    def __init__(self, model_type: str, api_key: str, pdf_path: str) -> None:
        """Instantiate object."""
        self.model_type = model_type
        self.api_key = api_key
        self.pdf_path = pdf_path
        self.query_list: list = []
        self.chat_history: list = []
        self.model = object
        self.embedding = object
        self.bot_init: ConversationalRetrievalChain
        self.answer: dict

    def get_model_embedding(self) -> None:
        """Retrieve type of model and embeddings."""
        if self.model_type == "paid":
            print('api_key', self.api_key)
            self.model = OpenAI(temperature = 0.3, 
                                openai_api_key= self.api_key)
            self.embedding = OpenAIEmbeddings(openai_api_key= self.api_key)

    def remove_vectorstore_pdf(self) -> None:
        """Removes already existing pdf files and vector store database."""
        parent_dir = Path(self.pdf_path).parent
        for file in os.listdir(parent_dir):
            if file == "db":
               shutil.rmtree(str(parent_dir)+'/'+file)

    def initialize_bot(self) -> None:
        """Initialize the bot based on embeddings, dialogue chains."""
        self.remove_vectorstore_pdf()
        print('removed')
        pdf_loader = PyPDFLoader(self.pdf_path)
        pages = pdf_loader.load_and_split()
        self.get_model_embedding()
        vectordb = Chroma.from_documents(
            pages, embedding=self.embedding, persist_directory="db"
        )
        vectordb.persist()
        memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
        self.bot_init = ConversationalRetrievalChain.from_llm(
            llm=self.model,
            retriever=vectordb.as_retriever(
                search_type="similarity", search_kwargs={"k": 3}
            ),
            memory=memory,
            chain_type="stuff",
            get_chat_history=lambda h: h,
        )
    def run_bot(self, query: str)-> str:
        """Run the bot with user query.
        
        Args:
            query: User query with respect to uploaded pdf.
        Returns:
            Response of the bot.
        """
        if not self.query_list:
            self.initialize_bot()
            print('Bot initialized')
        self.answer = self.bot_init(
            {"question": query, "chat_history": self.chat_history}
        )
        print(self.answer["answer"])
        self.chat_history = [(query, self.answer["answer"])]
        self.query_list.append(query)
        return self.answer["answer"]
