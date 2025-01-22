from semantic_kernel.connectors.ai.open_ai import AzureTextToImage
from semantic_kernel.functions import kernel_function
from typing import Literal, Annotated
import os

class GenerateImage:
    def __init__(self):
        self.dalle3 = AzureTextToImage(service_id="my-service-id1",
                          api_key=os.getenv("AZURE_OPENAI_DALLE_API_KEY"),
                          endpoint=os.getenv("AZURE_OPENAI_DALLE_ENDPOINT"),
                          deployment_name=os.getenv("AZURE_OPENAI_DALLE_DEPLOYMENT_NAME"))

    @kernel_function(description="Generate an image from a description")
    async def generate_image(self, 
                             description: str, 
                             quality: Annotated[Literal["standard", "hd"], "The quality of the generated image usually standard"] = "standard", 
                             style: Annotated[Literal["vivid", "natural"], "The style of the generated image usually natural"] = "natural",
                             width: Annotated[int, "Width of the generated image usually 1024 px"] = 1024, 
                             height: Annotated[int, "Height of the generated image usually 1024 px"] = 1024 
                             ):
        print(f"Generating image from description: {description}")
        if style != "vivid" and style != "natural":
            style = "natural"
        if quality != "standard" and quality != "hd":
            quality = "standard"
        if width != 1024 and width != 1792:
            width = 1024
        if height != 1024 and height != 1792:
            height = 1024
        image = await self.dalle3.generate_image(description=description, width=width, height=height, quality=quality, style=style)
        return image
    