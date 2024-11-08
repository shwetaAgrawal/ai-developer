### [< Previous Challenge](./Challenge-03.md) - **[Home](../README.md)** - [Next Challenge >](./Challenge-05.md)

# Challenge 04 -  Create a workflow plugin using Logic Apps

## Introduction

As developers we already use developer tools like Azure DevOps and GitHub. So why not see what cool things we can by integrating Semantic Kernel into our developers workflow. In this challenge, you will learn how to create a workflow plugin using Azure Logic Apps and how to integrate it with Azure OpenAI to build powerful AI infused applications. Using Logic Apps brings together over 1400 connectors (APIs) to help you integrate with other services and applications. Logic Apps is a powerful tool that can be used to automate workflows and business processes. Using Semantic Kernel, you can chain together multiple prompts to create a more complex conversation with the AI that is interconnected to multiple APIs and services.

## Pre-requisites

:exclamation: Pre-requisites must be done in sequence as they are dependent on each other.

1. [Setup Azure DevOps](./Resources/Supporting%20Challenges/Challenge-04-Prereq-ADO.md)
1. [Setup Azure Logic Apps](./Resources/Supporting%20Challenges/Challenge-04-Prereq-LogicApp.md)

>NOTE: These pre-requisites are required to complete the challenges in this module. If you have not completed the pre-requisites, please do so before proceeding with the challenges. Most of the challenges in this module will require the Azure DevOps project and Azure Logic App created in the pre-requisites.

### Challenges

This challenge will introduce you to how to import OpenAPI API as Semantic Kernels Plugins in C#, and how to chain plugins using the Auto Function Calling capabilities of Semantic Kernel.

1. Launch your AI Chat app, and ask the bot `What are my work items?`
    - Test the prompt "What are my work items?" see how it responds.
1. In addition to Challenge 3, you will be adding a new plugin to your Semantic Kernel using the Logic App you created in the pre-req.
    - Import your Logic App from the pre-req into Semantic Kernel.

        :bulb: [Integrate Logic App workflows as plugins with Semantic Kernel: Step-by-step guide](https://techcommunity.microsoft.com/t5/azure-integration-services-blog/integrate-logic-app-workflows-as-plugins-with-semantic-kernel/ba-p/4210854)

        :bulb: [Add Logic Apps as plugins](https://learn.microsoft.com/en-us/semantic-kernel/concepts/plugins/adding-logic-apps-as-plugins)

        :exclamation: We have created a `HttpClient` instance that will reuse your app login. When you are configuring the `OpenApiFunctionExecutionParameters`, instead of setting your own `HttpClient`, you can use our provided client by setting it to `kernel.Services.GetRequiredService<IHttpClientFactory>().CreateClient("LogicAppHttpClient")`

        :exclamation: Semantic Kernel SDK for OpenAPI's - your plugin name must be 64 characters or less. Then name of your logic app, the name of your trigger, and the name of your plugin will be concatenated together. So please keep your plugin name short or rename your logic app trigger to a shorter name.

    - Test the prompt "What are my work items?" see how it responds.
1. _(Optional)_ Create 2 additional Logic Apps Workflows to chained together to create a more complex conversation with the AI.

## Success Criteria

1. Your chat bot should be able to answer the question "What are my work items?" with a list of work items from Azure DevOps.
1. You can ask the bot to filter, sort, group, or change the display format of the work items.

## Additional Learning Resources

[Add plugins from OpenAPI specifications](https://learn.microsoft.com/en-us/semantic-kernel/concepts/plugins/adding-openapi-plugins?pivots=programming-language-csharp)

[OpenApiFunctionExecutionParameters](https://learn.microsoft.com/en-us/dotnet/api/microsoft.semantickernel.plugins.openapi.openapifunctionexecutionparameters?view=semantic-kernel-dotnet)

[ImportPluginFromOpenApiAsync](https://learn.microsoft.com/en-us/dotnet/api/microsoft.semantickernel.plugins.openapi.openapikernelextensions.importpluginfromopenapiasync?view=semantic-kernel-dotnet)

### [< Previous Challenge](./Challenge-03.md) - **[Home](../README.md)** - [Next Challenge >](./Challenge-05.md)
