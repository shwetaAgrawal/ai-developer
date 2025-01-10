import asyncio
import logging
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

# Add Logger 
logger = logging.getLogger(__name__)

#Challene 02 - Add Kernel

#Challenge 02 - Chat Completion Service
#TODO: 
chat_completion_service = AzureChatCompletion(service_id="my-service-id")

# Start Challenge 02 - Sending a message to the chat completion service
kernel = Kernel()
kernel.add_service(chat_completion_service)
#Challenge 03 and 04 - Services Required

async def main() -> None:
    print(
        "Welcome to the chat bot!\n"
    )

    #Challenge 05 - Register Azure OpenAI Text Embeddings Generation


    # Challenge 05 - Register Search Index


    # Challenge 07 - Add Azure OpenAI Text To Image


async def add_plugins(self):
    # Challenge 03 - Add Time Plugin
    # Placeholder for time plugin

    # Challenge 04 - Import OpenAPI Spec
    # Placeholder for OpenAPI plugin

    # Challenge 05 - Add Search Plugin
    # Placeholder for search plugin

    # Challenge 07 - Text To Image Plugin
    # Placeholder for text-to-image plugin

if __name__ == "__main__":
    asyncio.run(main())