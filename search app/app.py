import streamlit as st
from model import query_chat_gpt, query_llama_3_1, query_distill_bert
from file_utils import get_vectorized_output, get_most_similar_docs_for_user_input, extraxt_top_n_file_content

if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = ""
if 'answers' not in st.session_state:
    st.session_state['answers'] = []
if 'form_disabled' not in st.session_state:
    st.session_state['form_disabled'] = False

st.title("SolTek AI Search")
model_choice = st.selectbox("Choose a Model", ("GPT-3.5", "LLaMA 3.1", "Bert"))
form_disabled = st.session_state['form_disabled']

with st.form(key='search_form'):
    user_ask = st.text_input("Type in your question here")
    submit_button = st.form_submit_button(label='Ask SolTek')

# Process and tokenize the user query
# user_ask = [st.text_input("Type in your question here")]
if submit_button:
    if user_ask:

        st.session_state['conversation_history'] += f"User: {user_ask}\n"
        # Vectorize the user input
        user_y = get_vectorized_output(user_ask)

        # Get similar docs based on user input
        most_similar_files = get_most_similar_docs_for_user_input(user_y)

        if not most_similar_files:
            st.write("No relevant document found")

        else:
            st.session_state['form_disabled'] = True
            extracted_texts = extraxt_top_n_file_content(most_similar_files)
            final_text = "\n\n".join(extracted_texts)
            prompt = st.session_state['conversation_history'] + f"\n\nDocuments:\n{final_text}\n\nAI:"

            # Depending on the model choice, query the respective model
            if model_choice == "GPT-3.5":
                generated_text = query_chat_gpt(user_ask, prompt)
            elif model_choice == "LLaMA 3.1":
                generated_text = query_llama_3_1(user_ask, prompt)
            elif model_choice == "Bert":
                generated_text = query_distill_bert(user_ask, prompt)

            # Store the result in session state
            st.session_state['answers'].insert(0, generated_text)
            if len(st.session_state['answers']) > 4:
                st.session_state['answers'].pop()

            # Display the results
            st.markdown("#### Answer:")
            st.write(generated_text)

            if len(st.session_state['answers']) >= 2:
                st.markdown("#### Previous Conversation History:")
                for i, answer in enumerate(st.session_state['answers'][1:]):
                    st.markdown(f"**Answer {i + 1}:** {answer}")
                    st.markdown("---")

            st.markdown("#### Most Relevant Documents:")
            for file in most_similar_files:
                st.markdown(f"- {file}")

    else:
        st.write("⚠️ **Please enter your search phrase.**")
