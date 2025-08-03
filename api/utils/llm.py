from langchain_groq import ChatGroq
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from langchain_community.tools import TavilySearchResults
from langchain.agents import create_react_agent, AgentExecutor  

from api.utils.vector_db import query_vector_db


class QAgent:
    def __init__(self):
        llm = ChatGroq(
            model="llama3-70b-8192",
            temperature=0.3
            )
        tavily_tool = TavilySearchResults(
            
                max_results=5,
                use_cache=False  # disable cache to always search
            )
        tavily_search_tool = Tool(
                name="Tavily Search",
                func=tavily_tool.run,
                description="Use this tool to search the web in real-time via Tavily."
            )
        pdf_context_tool = Tool(
                name="RAG Retriever",
                func=query_vector_db,
                description="Useful for answering questions based on internal documents."
            )

        # Modified hwchase17/react prompt
        agent_prompt = PromptTemplate(
            template="""
                Answer the following questions as best you can. You have access to the following tools:

                - Always try to retrieve context from all relevant tools. tools should not be invoked more than once.
                - Always use preferably 2 relevant tools to confirm accuracy of the tool response. If you cant find get response from tools ignore this instruction.
                - Compare the outputs and use the one that best matches the question. Make sure to mention Discrepancy in the source only if there any.
                - If neither contains enough relevant information, say so.
                - If one tool fails to retrieve anything, issue a warning.
                - If both tool return consistent and relevant information respond with ONLY the answer.

                Tools:
                {tools}

                Use the following format:

                Question: the input question you must answer
                Thought: think step-by-step about which tools to use and why
                Action: the action to take, should be one of [{tool_names}]
                Action Input: the input to the action
                Observation: the result of the action
                ... (this Thought/Action/Action Input/Observation can repeat N times)
                Thought: I now know the final answer
                Final Answer: the final answer to the original input question, include warnings if any tool failed or gave irrelevant results

                Begin!

                Question: {input}
                Thought: {agent_scratchpad}

            """)
        
        context_summary_chain = create_react_agent(llm, tools=[pdf_context_tool, tavily_search_tool], prompt=agent_prompt)
        self.agent = AgentExecutor(
            agent=context_summary_chain,
            tools=[pdf_context_tool, tavily_search_tool],
            verbose=True,
            max_iterations=5,
            handle_parsing_errors=True
        )
    
    
    def ask(self, question) -> str:
        """Summarizes the given text using the LLM."""
        if not self.agent:
            raise ValueError("LLM is not initialized. Call init() first.")
        return self.agent.invoke({"input": question})['output']


