import streamlit as st
import os
import base64
import traceback
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from pypdf import PdfReader, PdfWriter
import io
from streamlit_pdf_viewer import pdf_viewer
from st_copy_to_clipboard import st_copy_to_clipboard

from dotenv import load_dotenv

load_dotenv()

st.set_page_config(layout="wide")

llm = GoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)

st.title("PDF Topic Extraction and Summarization")


def display_pdf(file_path, start_page, end_page):
    try:
        with open(file_path, "rb") as f:
            pdf_reader = PdfReader(f)
            pdf_writer = PdfWriter()
            for page in range(start_page - 1, end_page):
                pdf_writer.add_page(pdf_reader.pages[page])

            output_stream = io.BytesIO()
            pdf_writer.write(output_stream)
            pdf_bytes = output_stream.getvalue()

        pdf_viewer(file_path, pages_to_render=list(range(start_page, end_page)))

    except Exception as error:
        st.error(f"Error displaying PDF: {str(error)}")
        st.code(traceback.format_exc())


uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    try:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getvalue())

        pdf_reader = PdfReader("temp.pdf")
        total_pages = len(pdf_reader.pages)

        st.write(f"Total pages: {total_pages}")
        st.subheader("Select Pages")
        page_input = st.text_input("Enter page range (e.g., 1-5 or 1,3,5)", value="1-" + str(total_pages))

        try:
            if '-' in page_input:
                start, end = map(int, page_input.split('-'))
                page_range = range(start, end + 1)
            else:
                page_range = list(map(int, page_input.split(',')))

            start_page, end_page = min(page_range), max(page_range)
        except:
            st.error("Invalid page range. Using default.")
            start_page, end_page = 1, total_pages

        st.slider("Adjust page range", 1, total_pages, (start_page, end_page), key="page_slider")

        col1, col2 = st.columns(2)


        # Merge the selected pages into a single text
        selected_pages = pdf_reader.pages[st.session_state.page_slider[0] - 1:st.session_state.page_slider[1]]
        merged_text = "\n".join([page.extract_text() for page in selected_pages])

        # Initialize llm outside of button click events
        with col1:
            if st.button("Extract Topics"):
                try:
                    topic_extraction_prompt_template = """Extract only the main topic names discussed in the following text. List each topic name on a new line without any additional formatting or numbering:
                    {text}
                    """
                    topic_extraction_prompt = PromptTemplate(
                        input_variables=["text"], template=topic_extraction_prompt_template
                    )

                    topic_chain = (
                            {"text": RunnablePassthrough()}
                            | topic_extraction_prompt
                            | llm
                    )

                    result = topic_chain.invoke(merged_text)
                    topics = result.strip().split('\n')

                    st.session_state.topics = topics  # Store topics in session state

                except Exception as e:
                    st.error(f"An error occurred during topic extraction: {str(e)}")
                    st.code(traceback.format_exc())

            # Display topics and generate summaries
            if 'topics' in st.session_state:
                st.subheader("Main Topics Discussed:")
                for topic in st.session_state.topics:
                    if st.button(topic, key=topic):
                        try:
                            summarization_prompt_template = f"""Generate a concise summary for educational purposes on the topic of "{topic}" based on the following text:
                            {{text}}
                            """
                            summarization_prompt = PromptTemplate(
                                input_variables=["text"], template=summarization_prompt_template
                            )
                            summarization_chain = (
                                    {"text": RunnablePassthrough()}
                                    | summarization_prompt
                                    | llm
                            )
                            summary = summarization_chain.invoke(merged_text)
                            st.write(summary)
                            st_copy_to_clipboard(summary)

                            # Add copy to clipboard button
                            if st.button("Copy Summary to Clipboard", key=f"copy_{topic}"):
                                st_copy_to_clipboard(summary)

                        except Exception as e:
                            st.error(f"An error occurred during summary generation: {str(e)}")
                            st.code(traceback.format_exc())
        with col2:
            st.subheader("Selected Pages")
            display_pdf("temp.pdf", st.session_state.page_slider[0], st.session_state.page_slider[1])



    except Exception as e:
        st.error(f"Error reading the PDF: {str(e)}")
        st.code(traceback.format_exc())
        st.info("The PDF file might be corrupted or in an unsupported format. Please try another file.")

    finally:
        if os.path.exists("temp.pdf"):
            os.remove("temp.pdf")

# Add JavaScript to enable clipboard functionality
st.markdown("""
<script>
const streamlitDoc = window.parent.document;

const buttons = streamlitDoc.querySelectorAll('button');
buttons.forEach(button => {
    if (button.innerText.includes('Copy Summary to Clipboard')) {
        button.addEventListener('click', function() {
            const summary = streamlitDoc.querySelector('.stMarkdown p').innerText;
            navigator.clipboard.writeText(summary).then(function() {
                console.log('Summary copied to clipboard successfully!');
            }, function(err) {
                console.error('Could not copy text: ', err);
            });
        });
    }
});
</script>
""", unsafe_allow_html=True)
