from langchain.prompts import PromptTemplate

def refine_question_prompt():
    return PromptTemplate(
        template="""
        Refine the following question to be more specific and detailed as a legal question , which is detailed and well organied

        Original Question: {user_question}

        Give only the refined question as output , dont give any explanation or comment.
        """,
        input_variables=["user_question"]
    )
