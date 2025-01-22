import asyncio
import logging
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureTextToImage
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.contents.chat_history import ChatHistory
from Plugins.TimePlugin import TimePlugin
from Plugins.GeocodingPlugin import GeocodingPlugin
from Plugins.WeatherPlugin import WeatherPlugin
from Plugins.GenerateImage import GenerateImage
from Plugins.SearchPlugin import SearchPlugin

# for automated function calling
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    AzureChatPromptExecutionSettings,
)
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.functions.kernel_arguments import KernelArguments

from dotenv import load_dotenv
import os

load_dotenv()
# Add Logger 
logger = logging.getLogger(__name__)

# Retrieve the chat completion service by id
# chat_completion_service = kernel.get_service(service_id="my-service-id")
# Retrieve the default inference settings
#execution_settings = kernel.get_prompt_execution_settings_from_service_id("my-service-id")

#Challenge 03 and 04 - Services Required

async def main() -> None:
    print(
        "Welcome to the chat bot!\n"
    )
    chat_history = ChatHistory()
    while True:
        user_input = input("You: ")
        if user_input == "exit":
            break
        chat_history.add_user_message(user_input)
        
        try:
            response = await chat_completion_service.get_chat_message_content(
                chat_history=chat_history,
                settings=execution_settings,
                kernel=kernel,
                arguments=KernelArguments(),
            )
        except Exception as e:
            print(f"Error: {e}")
            continue

        print(f"User query: {chat_history.messages[-1]}")
        print(f"Chat bot response: {response}")


    #Challenge 05 - Register Azure OpenAI Text Embeddings Generation


    # Challenge 05 - Register Search Index


    


def add_plugins():
    global kernel
    # Challenge 03 - Add Time Plugin
    # Placeholder for time plugin
    time_plugin = TimePlugin(logger=logger)
    kernel.add_plugin(time_plugin, plugin_name="TimePlugin")
    logger.log(logging.INFO, "Time Plugin added")

    kernel.add_plugin(GeocodingPlugin(), plugin_name="GeoLocation")
    kernel.add_plugin(WeatherPlugin(), plugin_name="WeatherPlugin")
    # Challenge 04 - Import OpenAPI Spec
    # Placeholder for OpenAPI plugin

    # Challenge 05 - Add Search Plugin
    # Placeholder for search plugin
    kernel.add_plugin(SearchPlugin(), plugin_name="SearchPlugin")

    # Challenge 07 - Add Azure OpenAI Text To Image
    # Placeholder for text-to-image plugin
    kernel.add_plugin(GenerateImage(), plugin_name="GenerateImage")

# Start Challenge 02 - Sending a message to the chat completion service
#Challene 02 - Add Kernel
kernel = Kernel()

#Challenge 02 - Chat Completion Service
chat_completion_service = AzureChatCompletion(service_id="my-service-id",
                                              api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                                              endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                                              deployment_name=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"))

kernel.add_service(chat_completion_service)



add_plugins()

# Retrieve the chat completion service by type
chat_completion_service = kernel.get_service(type=ChatCompletionClientBase)

# for automated function calling
execution_settings = AzureChatPromptExecutionSettings()
execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

if __name__ == "__main__":
    asyncio.run(main())

# prompt for challenge 7 - create a beautiful image depicting current weather in vancuover, canada
# prompt for challenge 7 - Wear the hat of a product designer and think about suitable product name, description, and logo for a handheld teleporting device. For logo, visual representation is preferred. Also think about how we can depict this product, feel free to create images to share the concept.