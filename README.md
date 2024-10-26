# PDF Summary

A Streamlit application for extracting topics and generating summaries from PDF files using Google Gemini.

[![GitHub](https://img.shields.io/github/license/AltynbekKaliakbarov/pdf-summary)](https://github.com/AltynbekKaliakbarov/pdf-summary/blob/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/pdf-summary)](https://pypi.org/project/pdf-summary/)


## Description

This project provides a user-friendly interface to upload a PDF document, select specific pages, extract the main topics discussed, and generate concise summaries for each topic.  It leverages the power of Langchain and Google Gemini for natural language processing tasks.

## Features

* **PDF Upload:** Easily upload PDF files for processing.
* **Page Selection:** Choose specific pages or a range of pages from the PDF.
* **Topic Extraction:**  Intelligently extracts the main topics discussed within the selected pages.
* **Concise Summarization:** Generates clear and concise summaries for each extracted topic.
* **Copy to Clipboard:**  Easily copy generated summaries to your clipboard.
* **Error Handling:** Robust error handling to manage potential issues during PDF processing and API calls.


## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/AltynbekKaliakbarov/pdf-summary.git
cd pdf-summary
```

2. **Create a virtual environment (recommended):**

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies:**

```bash
rye sync
```

4. **Set up your Google Cloud API Key:**

* Obtain a Google Cloud API key with access to the Gemini API.
* Create a `.env` file in the root directory of the project and add your API key:

```
GOOGLE_API_KEY=your_api_key_here
```

## Usage

1. **Run the Streamlit app:**

```bash
streamlit run src/pdf-extract.py
```

2. **Upload your PDF:** Use the file uploader to select the PDF you want to process.
3. **Select Pages:** Specify the pages you want to include in the analysis.
4. **Extract Topics:** Click the "Extract Topics" button to extract the main topics.
5. **Generate Summaries:** Click on each extracted topic to generate a summary.  Use the "Copy Summary to Clipboard" button to copy the summary.

## Technologies Used

* **Streamlit:** For the user interface.
* **Langchain:** For chaining together language models and other utilities.
* **Google Gemini:**  The large language model used for topic extraction and summarization.
* **PyPDF2:** For PDF processing.
* **Python:** The programming language used for the backend.


## Contributing

Contributions are welcome! Please open an issue or submit a pull request.


## License

This project is licensed under the [MIT License](https://github.com/AltynbekKaliakbarov/pdf-summary/blob/main/LICENSE).

