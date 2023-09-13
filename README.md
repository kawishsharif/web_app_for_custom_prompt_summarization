# web_app_for_custom_prompt_summarization
Using LangChain for interactive summarization by using user prompt over documents with a Stream lit interface for optimal user experience  
## installation
        
1. Install the required dependencies:

        pip install -r requirements.txt
	pip3 install streamlit
        pip install "unstructured[all-docs]"

2. Replace the API key in the main.py file with your actual OpenAI API key:

            openai_api_key='YOUR_API_KEY',

3. Run main.py and after that run the Streamlit application by writing this command in command propmt:

        streamlit run file_name_with_extension_name.py
