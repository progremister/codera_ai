import os
import threading
import subprocess
import requests
import json
import glob
import concurrent.futures
from typing import List
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document

from crewai import Agent, Task, Crew
from langchain_community.chat_models import ChatOpenAI
from crewai_tools import TXTSearchTool
from langchain.llms import Ollama
from textwrap import dedent

def ollama():
    os.environ['OLLAMA_HOST'] = '0.0.0.0:11434'
    os.environ['OLLAMA_ORIGINS'] = '*'
    subprocess.Popen(["ollama", "serve"])


ollama_thread = threading.Thread(target=ollama)
ollama_thread.start()

ollama_thread = threading.Thread(target=ollama)
ollama_thread.start()

prompt = """
say hi
"""

url = 'http://localhost:11434/api/chat'
payload = {
    "model": "llama2",
    "temperature": 0.6,
    "stream": False,
    "messages": [
        {"role": "system", "content": "You are an AI assistant!"},
        {"role": "user", "content": prompt}
    ]
}

response = requests.post(url, json=payload)
message_str = response.content.decode('utf-8')
message_dict = json.loads(message_str)
print(message_dict['message']['content'])


PERSIST_DIRECTORY = "./db/"

LOADER_MAPPING = {
    ".py": (PythonLoader, {}),
    ".html": (UnstructuredHTMLLoader, {}),
    ".md": (UnstructuredMarkdownLoader, {}),
    ".cpp": (TextLoader, {"encoding": "utf8"}),
    ".hpp": (TextLoader, {"encoding": "utf8"}),
    ".js": (TextLoader, {"encoding": "utf8"}),
    ".rb": (TextLoader, {"encoding": "utf8"}),
    ".rs": (TextLoader, {"encoding": "utf8"}),
    ".java": (TextLoader, {"encoding": "utf8"}),
    ".jar": (TextLoader, {"encoding": "utf8"}),
    ".go": (TextLoader, {"encoding": "utf8"}),
    ".scala": (TextLoader, {"encoding": "utf8"}),
    ".sc": (TextLoader, {"encoding": "utf8"}),
    ".swift": (TextLoader, {"encoding": "utf8"}),
    ".php": (TextLoader, {"encoding": "utf8"}),
    ".tex": (TextLoader, {"encoding": "utf8"}),
}

LANG_MAPPINGS = {
    "py": Language.PYTHON, "cpp": Language.CPP, "hpp": Language.CPP, "js": Language.JS,
    "html": Language.HTML, "md": Language.MARKDOWN, "rb": Language.RUBY, "rs": Language.RUST,
    "java": Language.JAVA, "jar": Language.JAVA, "go": Language.GO, "scala": Language.SCALA,
    "sc": Language.SCALA, "swift": Language.SWIFT, "php": Language.PHP, "latex": Language.LATEX,
}

class Ingestor:
    def __init__(self, cwd: str, db: str, emb_model: str, ignore_folders: List[str]) -> None:
        self.cwd = cwd
        self.db = db
        self.emb_model = emb_model
        self.ignore_folders = ignore_folders
        self.chunk_size = 60
        self.chunk_overlap = 2
        self.threshold = 5242880

    def load_single_document(self, file_path: str) -> Document:
        ext = "." + file_path.rsplit(".", 1)[-1]
        if ext in LOADER_MAPPING:
            loader_class, loader_args = LOADER_MAPPING[ext]
            loader = loader_class(file_path, **loader_args)
            return loader.load()[0]
        raise ValueError(f"Unsupported file extension '{ext}'")

    def load_documents(self, ignored_files: List[str] = []) -> List[Document]:
        all_files = [glob.glob(os.path.join(self.cwd, f"**/*{ext}"), recursive=True) for ext in LOADER_MAPPING]
        filtered_files = [file_path for file_path in all_files if not any(ignore_folder in file_path for ignore_folder in self.ignore_folders)]
        filtered_files = filtered_files if not ignored_files else [file_path for file_path in all_files if file_path not in ignored_files]

        results = []
        with tqdm(total=len(filtered_files), desc="Loading new documents", ncols=80) as pbar:
            for file_path in filtered_files:
                file_size = os.path.getsize(file_path)
                executor = ProcessPoolExecutor() if file_size > self.threshold else ThreadPoolExecutor()
                with executor as executor:
                    future = executor.submit(self.load_single_document, file_path)
                    results.append(future.result())
                pbar.update()
        return results

    def split_docs(self, docs_list: List[Document], language: str) -> List[Document]:
        text_splitter = RecursiveCharacterTextSplitter.from_language(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap, language=language)
        return text_splitter.split_documents(docs_list)

    def process_documents(self, ignored_files: List[str] = []) -> List[Document]:
        doc_dict = {}
        documents = self.load_documents(ignored_files=ignored_files)
        if not documents:
            print("No new documents to load")
            exit(0)
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.split_docs, [doc], language=LANG_MAPPINGS[doc.metadata["source"].split(".")[-1]]) for doc in documents]
            all_docs = [doc for future in concurrent.futures.as_completed(futures) for doc in future.result()]
        return all_docs

    def does_vectorstore_exist(self) -> bool:
        index_path = os.path.join(self.db, "index")
        if os.path.exists(index_path):
            collections_path = os.path.join(self.db, "chroma-collections.parquet")
            embeddings_path = os.path.join(self.db, "chroma-embeddings.parquet")
            if os.path.exists(collections_path) and os.path.exists(embeddings_path):
                index_files = glob.glob(os.path.join(index_path, "*.bin")) + glob.glob(os.path.join(index_path, "*.pkl"))
                if len(index_files) > 3:
                    return True
        return False

    def ingest(self) -> None:
        embeddings = HuggingFaceEmbeddings(model_name=self.emb_model)
        if self.does_vectorstore_exist():
            print(f"Appending to existing vectorstore at {self.db}")
            db = Chroma(persist_directory=self.db, embedding_function=embeddings)
            collection = db.get()
            texts = self.process_documents([metadata["source"] for metadata in collection["metadatas"]])
            db.add_documents(texts)
        else:
            print("Creating new vectorstore")
            texts = self.process_documents()
            db = Chroma.from_documents(texts, embeddings, persist_directory=self.db)
        db.persist()
        db = None
        print("Vectorstore created, you can now run 'eunomia start' to use the LLM to interact with your code!")

"""### Main"""




os.environ["OPENAI_API_BASE"] = 'http://localhost:11434/api/chat'
ollama_openhermes = Ollama(model="llama2")


class MigrationAgents:
    def strategic_analyst(self):
        return Agent(
            role='The Strategic Analyst',
            goal="""Meticulously analyze your current software,
                   business goals, and desired outcomes to recommend
                   the optimal migration type""",
            backstory="""Utilize advanced code analysis tools,
                       business process modeling tools, and machine learning
                       algorithms to provide comprehensive migration
                       recommendations""",
            verbose=True,
            tools=[],
            llm=ollama_openhermes
        )

    def senior_developer(self):
        return Agent(
            role='Senior Developer with experience in the target framework/language',
            goal='To lead the code migration effort, translating code effectively from the old technology stack to the new one, ensuring compatibility and functionality in the new environment.',
            verbose=True,
            llm=ollama_openhermes,
            backstory='Senior Developers possess deep expertise in both the source and target technologies. They have been involved in similar migration projects before and understand best practices for code refactoring and optimization.'
        )

    def data_architect(self):
        return Agent(
            role='Data Architect',
            goal='To design and optimize data models and schemas, ensuring efficient data migration with minimal loss or corruption, while maintaining data integrity and compliance with organizational standards.',
            verbose=True,
            llm=ollama_openhermes,
            backstory='Data Architects are seasoned professionals with a background in database management and data engineering. They excel in understanding complex data relationships and designing robust data architectures.'
        )

    def project_manager(self):
        return Agent(
            role='Project Manager',
            goal='To lead the overall migration effort, ensuring tasks are completed on time and within budget, while meeting predefined objectives and adhering to project timelines and resource allocations.',
            verbose=True,
            llm=ollama_openhermes,
            backstory='Project Managers are seasoned professionals with a strong background in project management methodologies and frameworks. They excel in communication, stakeholder management, and risk mitigation, driving the project forward towards successful completion.'
        )


class MigrationTasks:

    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"





    def strategic_analysis(self, agent):
        return Task(
            description=dedent(f"""
                       Meticulously analyze your code,
                       business goals, and desired outcomes to recommend
                       the optimal migration type. {self.__tip_section()}
                       """),
            expected_output=dedent("""Recommendations regarding the optimal migration type"""),
            agent=agent
        )

    def pre_migration_planning(self, agent):
        """
        This task focuses on planning and preparation before the migration.
        """
        return Task(
            description=dedent(f"""
                       Create a detailed migration plan outlining
                       steps, timelines, resources, rollback strategies,
                       and communication procedures. {self.__tip_section()}
                       """),
            expected_output=dedent("""A comprehensive migration plan"""),
            agent=agent
        )


    def code_migration(self, agent):
        """
        This task focuses on migrating the codebase to the new platform.
        """
        description = "Migrate codebase to the target environment."
        return Task(
            description=description,
            expected_output=dedent("""Migrated codebase in the target environment"""),
            agent=agent,
        )

    def data_migration(self, agent, target_schema=None):
        """
        This task focuses on migrating the data to the new system.
        """
        description = "Migrate data to the target system."
        if target_schema:
            description += f" (Target Schema: {target_schema})"
        return Task(
            description=description,
            expected_output=dedent("""Migrated data in the target system"""),
            agent=agent,
        )

    def testing_and_validation(self, agent):
        """
        This task focuses on comprehensive testing after the migration.
        """
        return Task(
            description=dedent("""
                       Perform thorough testing to validate functionality,
                       data integrity, and performance in the migrated system. {self.__tip_section()}
                       """),
            expected_output=dedent("""Test reports indicating successful migration"""),
            agent=agent
        )

    def post_migration_support(self, agent):
        """
        This task focuses on providing support after the migration
        to ensure a smooth transition.
        """
        return Task(
            description=dedent("""
                       Monitor the migrated system, address any issues,
                       and provide ongoing user support. {self.__tip_section()}
                       """),
            expected_output=dedent("""Stable and operational migrated system"""),
            agent=agent
        )


class MigrationCrew:
    def run(self):
        agents = MigrationAgents()
        tasks = MigrationTasks()

        # Creating agents
        strategic_analyst = agents.strategic_analyst()
        senior_developer = agents.senior_developer()
        data_architect = agents.data_architect()
        project_manager = agents.project_manager()

        # Creating tasks for each agent
        tasks_for_strategic_analyst = [
            tasks.strategic_analysis(strategic_analyst),
            tasks.pre_migration_planning(strategic_analyst),
            tasks.testing_and_validation(strategic_analyst),
            tasks.post_migration_support(strategic_analyst)
        ]

        tasks_for_senior_developer = [
            tasks.code_migration(senior_developer),
            tasks.testing_and_validation(senior_developer),
            tasks.post_migration_support(senior_developer)
        ]

        tasks_for_data_architect = [
            tasks.data_migration(data_architect),
            tasks.testing_and_validation(data_architect),
            tasks.post_migration_support(data_architect)
        ]

        tasks_for_project_manager = [
            tasks.strategic_analysis(project_manager),
            tasks.pre_migration_planning(project_manager),
            tasks.testing_and_validation(project_manager),
            tasks.post_migration_support(project_manager)
        ]

        # Combining all tasks
        all_tasks = (
            tasks_for_strategic_analyst
            + tasks_for_senior_developer
            + tasks_for_data_architect
            + tasks_for_project_manager
        )

        # Creating a crew with essential agents and tasks
        crew = Crew(
            agents=[
                strategic_analyst,
                senior_developer,
                data_architect,
                project_manager,
            ],
            tasks=all_tasks,
            verbose=True,
        )

        result = crew.kickoff()
        return result


custom_crew = MigrationCrew()
result = custom_crew.run()

print("\n\n########################")
print("## Here is your custom crew run result:")
print("########################\n")
print(result)