# 🚀 SourceSense AI – Intelligent source-based Q&A

SourceSense AI is an **AI-powered research assistant agent** that extracts and analyzes content from multiple news article URLs. Users can dynamically add URLs, process the content, and then ask questions based on the aggregated information.

---

## 📌 **Features**
- **Dynamic URL Input:** Add or remove multiple news article URLs  
- **AI-Powered Q&A:** Ask questions and get answers based on the provided URLs  
- **FAISS Indexing:** Efficient storage and retrieval for fast search  
- **Automatic Text Extraction:** Extracts key information from web pages  
- **Optimized Error Handling:** Prevents crashes due to missing URLs or invalid inputs  
- **User-Friendly UI:** Interactive Streamlit interface  

---

## 🎯 **How It Works**
1. **Enter URLs**: Users can input multiple URLs dynamically  
2. **Process URLs**: The AI extracts and processes content into a knowledge base  
3. **Ask Questions**: Users ask questions, and the AI retrieves answers from indexed sources  
4. **Get Sources**: Answers are backed by sources from the processed URLs  

---

## 📦 **Installation**
Make sure you have Python installed. Then, clone the repository and install dependencies:

```bash
git clone https://github.com/mayurdalvi5/SourceSense-AI-Agent.git
cd SourceSense-AI-Agent
pip install -r requirements.txt
```
---

## 🚀 Run the Application
Start the Streamlit app by running:

```bash
streamlit run main.py
```
---

## ⚙️ Tech Stack

- Python – Core language
- Streamlit – UI framework
- LangChain – AI-powered document processing
- OpenAI API – Language model for Q&A
- BeautifulSoup & Requests – Web scraping
- FAISS – Efficient document retrieval

---

## 🛠 Usage Guide

1. Enter URLs

- Click "Add URL" to add multiple article links
- Click "Remove Last URL" to delete unwanted links

2. Process Data
- Click "Process URLs" to extract and index data

3. Ask Questions
- Type your query and click "Submit Question"

4. View Answers & Sources
- AI provides an answer along with sources

---

## OpenAI API Key

- Create .env file where you will store openai api key

```bash
OPENAI_API_KEY=your_openai_api_key
```

---
## Output

![image](https://github.com/user-attachments/assets/5667940f-0436-4094-8096-4467027c655c)

