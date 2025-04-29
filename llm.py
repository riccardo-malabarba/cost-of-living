from langchain.llms import HuggingFaceTextGenInference
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load the local LLM model and tokenizer
model_name = "your-local-llm-model-name"  # Replace with your model name
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Initialize HuggingFaceTextGenInference with the local model
llm = HuggingFaceTextGenInference(model=model, tokenizer=tokenizer)

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import streamlit as st

# Initialize a list to keep track of previously generated fun facts
previous_fun_facts = []

def generate_summary(data, page_context):
    preprompt = """
    You are an expert data analyst. Provide a concise and insightful summary of the following data.
    Consider the context of the analysis, which is focused on {page_context}.
    Ensure the summary is informative and highlights key insights relevant to cost of living and economic indicators.
    """
    prompt_template = PromptTemplate(
        input_variables=["data", "page_context"],
        template=preprompt + "Data:\n{data}\nSummary:"
    )
    chain = LLMChain(llm=llm, prompt=prompt_template)
    return chain.run({"data": data, "page_context": page_context})

def generate_fun_fact(data, page_context):
    global previous_fun_facts

    preprompt = """
    You are a creative assistant. Generate a fun and engaging fact based on the following data.
    Consider the context of the analysis, which is focused on {page_context}.
    Ensure the fun fact is unique and not previously mentioned.
    Previous fun facts: {previous_fun_facts}
    """
    prompt_template = PromptTemplate(
        input_variables=["data", "page_context", "previous_fun_facts"],
        template=preprompt + "Data:\n{data}\nFun fact:"
    )
    chain = LLMChain(llm=llm, prompt=prompt_template)
    fun_fact = chain.run({"data": data, "page_context": page_context, "previous_fun_facts": ", ".join(previous_fun_facts)})

    # Add the new fun fact to the list of previous fun facts
    previous_fun_facts.append(fun_fact)

    return fun_fact

# Example usage in Streamlit app
if page == "Overview":
    page_context = "an overview of average monthly savings across Europe"
    # Generate summary and fun fact based on the filtered data
    filtered_data = merged_eu_data_aggregated[merged_eu_data_aggregated['country'].isin([household_type])]
    st.sidebar.write("### Summary")
    

    st.sidebar.write("### Fun Fact")
    if st.sidebar.button("Generate New Fun Fact"):
        st.sidebar.write(generate_fun_fact(filtered_data.to_string(), page_context))

elif page == "Choose Your Country":
    page_context = "a comparison of monthly budgets between selected countries"
    # Generate summary and fun fact based on the filtered data
    filtered_data = merged_eu_data_aggregated[merged_eu_data_aggregated['country'] == country]
    st.sidebar.write("### Summary")
    st.sidebar.write(generate_summary(filtered_data.to_string(), page_context))

    st.sidebar.write("### Fun Fact")
    if st.sidebar.button("Generate New Fun Fact"):
        st.sidebar.write(generate_fun_fact(filtered_data.to_string(), page_context))
