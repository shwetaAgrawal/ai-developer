import asyncio
from typing import List, Any
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
# for automated function calling
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    AzureChatPromptExecutionSettings,
)
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.agents import ChatCompletionAgent, AgentGroupChat
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole
from semantic_kernel.agents.strategies.termination.termination_strategy import TerminationStrategy
from semantic_kernel.functions.kernel_function_from_prompt import KernelFunctionFromPrompt
from semantic_kernel.agents.strategies.selection.kernel_function_selection_strategy import (
    KernelFunctionSelectionStrategy,
)
from dotenv import load_dotenv
import os

load_dotenv()

# prompt used for this challenge
# want to create a coloring for 3-5 year old kids, this is going to be a basic app with limited functionality like load template and color it, simple web, html and javascript version is sufficient

kernel = Kernel()
def _create_kernel_with_chat_completion(service_id: str) -> Kernel:
    kernel = Kernel()
    kernel.add_service(AzureChatCompletion(service_id=service_id,api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                                              endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                                              deployment_name=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")))
    return kernel

#Create a Business Analyst Agent [ChatCompletionAgent] and add it to the Agents List.
#ChatCompletionAgent takes Instructions, a Name (No Spaces allowed), and the Kernel.
business_analyst_agent = ChatCompletionAgent(
    service_id="business-analyst-agent",
    kernel=_create_kernel_with_chat_completion("business-analyst-agent"), #adding the kernel to the agent for chat completion, adding as service outside didn't work
    name="BusinessAnalystAgent",
    instructions="""You are a Business Analyst which will take the requirements from the user (also known as a 'customer')
and create a project plan for creating the requested app. The Business Analyst understands the user
requirements and creates detailed documents with requirements and costing. The documents should be 
usable by the SoftwareEngineer as a reference for implementing the required features, and by the 
Product Owner for reference to determine if the application delivered by the Software Engineer meets
all of the user's requirements.""")


# Create a Software Engineer Agent [ChatCompletionAgent] and add it to the Agents List.
# ChatCompletionAgent takes Instructions, a Name (No Spaces allowed), and the Kernel.
software_engineer_agent = ChatCompletionAgent(
    service_id="software-engineer-agent",
    kernel=_create_kernel_with_chat_completion("software-engineer-agent"),
    name="SoftwareEngineerAgent",
    instructions="""You are a Software Engineer, and your goal is create a web app using HTML and JavaScript
by taking into consideration all the requirements given by the Business Analyst. The application should
implement all the requested features. Deliver the code to the Product Owner for review when completed.
You can also ask questions of the BusinessAnalyst to clarify any requirements that are unclear.""")

# Create a Product Owner Agent [ChatCompletionAgent] and add it to the Agents List.
# ChatCompletionAgent takes Instructions, a Name (No Spaces allowed), and the Kernel.
product_owner_agent = ChatCompletionAgent(
    service_id="product-owner-agent",
    kernel=_create_kernel_with_chat_completion("product-owner-agent"),
    name="ProductOwnerAgent",
    instructions="""You are the Product Owner which will review the software engineer's code to ensure all user 
requirements are completed. You are the guardian of quality, ensuring the final product meets
all specifications and receives the green light for release. Once all client requirements are
completed, you can approve the request by just responding "%APPR%". Do not ask any other agent
or the user for approval. If there are missing features, you will need to send a request back
to the SoftwareEngineer or BusinessAnalyst with details of the defect. To approve, respond with
the token %APPR%.""")

# kernel.add_service(AzureChatCompletion(service_id="business-analyst-agent",api_key=os.getenv("AZURE_OPENAI_API_KEY"),
#                                               endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
#                                               deployment_name=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")))
# kernel.add_service(AzureChatCompletion(service_id="software-engineer-agent",api_key=os.getenv("AZURE_OPENAI_API_KEY"),
#                                               endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
#                                               deployment_name=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")))
# kernel.add_service(AzureChatCompletion(service_id="product-owner-agent",api_key=os.getenv("AZURE_OPENAI_API_KEY"),
#                                               endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
#                                               deployment_name=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")))

selection_function = KernelFunctionFromPrompt(
    function_name="selection",
    prompt=f"""
    Determine which participant takes the next turn in a conversation based on the the most recent participant.
    State only the name of the participant to take the next turn.
    No participant should take more than one turn in a row.

    Choose only from these participants:
    - BusinessAnalystAgent
    - SoftwareEngineerAgent
    - ProductOwnerAgent

    Always follow these rules when selecting the next participant:
    - After user input, it is BusinessAnalystAgent's turn.
    - After BusinessAnalystAgent replies, it is SoftwareEngineerAgent's turn.
    - After SoftwareEngineerAgent responds, it is ProductOwnerAgent's turn.

    History:
    {{{{$history}}}}
    """,
)
# kernel.add_service(AzureChatCompletion(service_id="selection",api_key=os.getenv("AZURE_OPENAI_API_KEY"),
#                                               endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
#                                               deployment_name=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")))

user_input = "Create a simple calculator app"

class ApprovalTerminationStrategy(TerminationStrategy):
    """A strategy for determining when an agent should terminate."""
    async def should_agent_terminate(self, agent, history):
        """Check if the agent should terminate."""
        
        if "%APPR%" in history[-1].content:
            return True
        return False



# for automated function calling
execution_settings = AzureChatPromptExecutionSettings()
execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

async def main() -> None:
    print(
        "Welcome to the chat bot!\n"
    )
    # Create Agent Group Chat [AgentGroupChat]
    chat = AgentGroupChat(
        agents=[business_analyst_agent, software_engineer_agent, product_owner_agent],
        termination_strategy=ApprovalTerminationStrategy(
            kernel=_create_kernel_with_chat_completion("termination"),
            agent = [product_owner_agent],
            maximum_iterations=10,
        ),
        selection_strategy=KernelFunctionSelectionStrategy(
            function=selection_function,
            kernel=_create_kernel_with_chat_completion("selection"),
            result_parser=lambda result: str(result.value[0]) if result.value is not None else "BusinessAnalystAgent",
            agent_variable_name="agents",
            history_variable_name="history",
        ),
    )

    while True:
        user_input = input("You: ")
        if user_input == "exit":
            break
        await chat.add_chat_message(ChatMessageContent(role=AuthorRole.USER, content=user_input))

        async for response in chat.invoke():
            print(f"# {response.role} - {response.name or '*'}: '{response.content}'")
        
        if chat.is_complete:
            print("Chat complete")
            break

if __name__ == "__main__":
    asyncio.run(main())

        # response = await chat_completion_service.get_chat_message_content(
        #     chat_history=chat_history,
        #     settings=execution_settings,
        #     kernel=kernel,
        #     arguments=KernelArguments(),
        # )

        # print(f"User query: {chat_history.messages[-1]}")
        # print(f"Chat bot response: {response}")