import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
import os

# Function to get response from Llama 2 model
def getLlamaResponse(input_text, no_words, blog_style):
    # Llama2 model      
    model_path = 'models/llama-2-7b-chat.ggmlv3.q8_0.bin'
    
    # Check if the model path exists
    if not os.path.isfile(model_path):
        print(f"Model path does not exist: {model_path}")
        return "Model file not found."
    
    llm = CTransformers(model=model_path, model_type='llama', config={'max_new_tokens':256, 'temperature':0.01}) 
    
    # Prompt tempelate
    tempelate = """
        Write a blog for {blog_style} job profile for a topic {input_text} within {no_words} words.
        """
    
    prompt=PromptTemplate(input_variables=["blog_style", "input_text", "no_words"], template=tempelate)
    
    # Generate the response from the Llama 2 model
    formatted_prompt = prompt.format(blog_style=blog_style, input_text=input_text, no_words=no_words)
    response = llm.invoke(formatted_prompt)
    print(response)
    return response


st.set_page_config(page_title="Generate Blogs", page_icon='🤖', layout='centered', initial_sidebar_state='collapsed')

st.header("Blog Generator🤖")

input_text = st.text_input("Enter blog topic")

# Creating two more columns for additional 2 fields
col1, col2 = st.columns([5,5])

with col1:
    no_words = st.text_input('No of words')
    
with col2:
    blog_style = st.selectbox('Writing the blog for', ('Researchers', 'Data Scientist', 'Common People'), index=0)

submit = st.button("Generate")

# Final response
if submit:
    st.write(getLlamaResponse(input_text, no_words, blog_style))