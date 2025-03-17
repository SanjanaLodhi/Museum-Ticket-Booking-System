# EcoAssist - E-Commerce Chatbot

EcoAssist is a multilingual e-commerce chatbot built using Python and Flask. It supports both text interactions and can answer FAQs, provide product information, and assist with order tracking.

## Features
- **Multilingual Support**: Answers queries in English and Urdu.
- **Knowledge Base**: Uses a predefined JSON knowledge base for FAQs.
- **Ollama Integration**: Leverages the Ollama API for generating responses.
- **Caching**: Frequently asked questions are cached for faster responses.

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Ollama server running locally or remotely

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/umairalamchaudhry/ai-chatbot.git
   cd ecoassist-chatbot

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
3. Start the Ollama server
   ```bash
   ollama serve
4. Run the Flask application
   ```bash
   python app.py
5. Access the chatbot
 - Open your browser and navigate to http://localhost:5000 to interact with the chatbot.

## Usage
### Interacting with the Chatbot
 - Enter your query:
    Type your question or query in the input box.
    Press "Enter" or click the "Send" button to submit your query.
 - Select language:
    Use the language dropdown to select either English or Urdu for the chatbot's response.
 - View the response:
    The chatbot will generate a response based on your query and display it in the chat window.
### Example Queries
 - "What are your business hours?"
 - "How can I track my order?"
 - "Do you offer international shipping?"

 ## Knowledge Base
  - Please review the knowledge base (knowledge_base.json) and update it as per your requirements. Add more questions and their answers as per your requirements.