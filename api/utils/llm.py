from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

context_summary_chain = None

def init():
   global context_summary_chain
   
   llm = ChatGroq(
       model="llama3-70b-8192",
       temperature=0.3
    )
   summarize_prompt = PromptTemplate(
         input_variables=["question", "context"],
         template="""
            You are a helpful assistant expertised in answering  medical questions based on given context.
            Answer the question based on the provided context only. Use context only if it is necessary.
            You should respond like a seasoned medical professional, providing clear and concise answers.

            If the context does not provide enough information to answer the question, respond with "Unable to answer the question with the given data".
            Question: {question}
            Context: {context}
         """
    )
   
   context_summary_chain = summarize_prompt | llm
   
   
def summarize(question, context_array: list[str]) -> str:
    """Summarizes the given text using the LLM."""
    if not context_summary_chain:
        raise ValueError("LLM is not initialized. Call init() first.")
    
    context = "\n".join(context_array)
    response = context_summary_chain.invoke({
        "question": question,
        "context": context
    }).content
    return response

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    init()
    sample_question = "What is the treatment for diabetes?"
    sample_context = [
        "Diabetes is a chronic disease that occurs when the body cannot produce enough insulin or use it effectively.",
        "Treatment for diabetes includes lifestyle changes, medication, and monitoring blood sugar levels."
    ]
    response = summarize(sample_question, sample_context)
    print(response)