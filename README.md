# Codera AI 🚀
## Introduction 📜

This project aims to modernize legacy codebases by transforming them into modern, efficient, and maintainable code. Through an AI-driven analysis and transformation process, legacy systems can be upgraded to meet current standards and technologies.

**Product demo: https://codera-ai.vercel.app/chat**

**Google Colab AI Prototype: https://colab.research.google.com/drive/1XaA3BmUssSqr9G4l3EeKW05fx0eOYf8V?usp=sharing**


## Implementation Plan 🛠️

### 1. Parser 📑
- Creates a single file (e.g., JSON) containing all code from the legacy project.

### 2. Code Analyser 🔍
- Reads the code archive.
- Summarizes the code to create a prompt for further actions.

### 3. Code Suggestions 💡
- Generates code suggestions based on the summary, which can either be presented as text or used to directly overwrite the existing files.

### 4. Personalized Prompts 👤
- Tailors prompts based on the user's role (Developer, DevOps) and experience.

### 5. Authentication and WebClient 🔐
- Manages user sessions and interactions through a web interface.

### 6. Image Design from Code Summary 🎨
- Converts code summaries into visual representations.

### 7. Textual Advice from Code Summary 📝
- Provides written advice based on the code analysis.

## Workflow 🔄

1. **User Registration:** Users sign up on the platform and set their role and experience level.
2. **Repository Upload:** Users upload their GitHub repository (archive or files) to the platform.
3. **Code Segmentation:** The system creates a JSON file containing the entire codebase, which is then used for analysis.
4. **Code Analysis:** The code is analyzed by the Code Analyser, interacting with an LLM to produce a logic summary.
5. **Agent Creation:** Based on the logic summary, various agents (Developer, UX/UI, etc.) are created to provide specific recommendations and actions.
6. **Personalized Recommendations:** Users receive suggestions tailored to their role, which can be used to directly modify and update the code.

## Getting Started 🌟

Follow these instructions to set up and run the project on your local machine for development and testing purposes.

### Prerequisites 📋

- Node.js and npm (for the Next.js project)
- Docker (for running Dockerized services)

### Setting up and running the React project 🖥️

1. Clone the repository to your local machine.
2. Install the dependencies.
    ```bash
        npm install
    ```
3. Start the development server.
    ```bash
        npm run dev
    ```

### Building and running the Server Docker image 🐳

1. Navigate to the directory containing the Server `Dockerfile`.
2. Build the Docker image.
    ```bash
        docker build -t server-image .
    ```
3. Run the Docker container.
    ```bash
        docker run -p 8000:8000 server-image
    ```

### Building and running the LLM Docker image 🐳

1. Navigate to the directory containing the LLM `Dockerfile`.
2. Build the Docker image.
    ```bash
        docker build -t llm-image .
    ```
3. Run the Docker container.
    ```bash
        docker run -p 11434:11434 llm-image
    ```

## Contributing 🤝

Guidelines for contributing to the project, including coding standards, pull request process, etc.

## License 📄

Information about the project's license.

## Contact 📬

How to get in touch with the project team.
