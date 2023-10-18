import openai
import streamlit as st
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredFileLoader
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
import os
os.environ['OPENAI_API_KEY'] = 'sk-FW6IidwCYtWfWZxM3fRDT3BlbkFJr7JjMEEcFS6BFbbDh'
@st.cache_data
def setup_documents(file_path,chunk_size,chunk_overlap):
    loader = UnstructuredFileLoader(file_path)
    docs_raw = loader.load()
    docs_raw_text = [doc.page_content for doc in docs_raw]
    text_splitter= RecursiveCharacterTextSplitter(chunk_size=chunk_size,
                                                  chunk_overlap=chunk_overlap)
    docs = text_splitter.create_documents(docs_raw_text)

    return docs
    

def custom_summary(docs,llm,custom_prompt):
    custom_prompt=custom_prompt + """:\n {text}"""
    COMBINE_PROMPT = PromptTemplate(template=custom_prompt, input_variables=["text"])
    Map_Prompt = PromptTemplate(template="Summarize:/n {text}",input_variables=["text"])
    chain = load_summarize_chain(llm,chain_type="map_reduce")
    summary_output= chain.run(docs)
    return summary_output
    

def main():
    st.set_page_config(layout="wide")
    st.title("Custom Summarization App")
    llm =st. sidebar.selectbox("LLM",["ChatGPT","GPT4","Default"])
    chunk_size = st.sidebar.slider("Chunk Size", min_value=10, max_value=10000,
                                   step=10, value=500)
    chunk_overlap=st.sidebar.slider("Chunk Overlap", min_value=5, max_value=5000,
                                    step=10, value=0)
    file_path = st.text_input("Enter the File Path ( e.g., ./Name_of_file.format)")
    st.write("Note: Put procecssing file in project directory")
    user_prompt = st.text_input("Enter the Custom Summary Prompt")
    st.write("Note: It may take max 55s appox. to sumarize")
    tempature= st.sidebar.number_input("Set the ChatGPT Temperature",
                                       min_value=0.0,
                                       max_value=1.0,
                                       step=0.1,
                                       value=0.5)
    num_summaries= st.sidebar.number_input("Number of Summaries",
                                           min_value=1,
                                           max_value=10,
                                           step=1,
                                           value=1)
    
    if file_path!="":
        docs=setup_documents(file_path,chunk_size,chunk_overlap)
        st.write("File loaded sucessfully")
    if llm=="ChatGPT":
        llm=ChatOpenAI(temperature=tempature)
    elif llm=="GPT4":
        llm=ChatOpenAI(tiktoken_model_name="gpt-4",temperature=tempature)
    else:
        llm=ChatOpenAI(temperature=tempature)
    
    if st.button("Summarize"):
        result=custom_summary(docs,llm,user_prompt)
        st.write("Summary:",result)


    



if __name__=="__main__":
    main()
