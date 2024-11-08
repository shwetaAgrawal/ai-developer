### [< Back to Challenge 0](../../Challenge-00.md)

# Setting up the .NET Aspire SDK
The instructions in this document will help you install .NET Aspire SDK. There are a few pre-requisites we assume you have installed bellow:

- [.NET 8 SDK](https://dotnet.microsoft.com/download/dotnet/8.0)
- Visual Studio Code and the C# Dev Kit Extension:
  - [Visual Studio Code](https://code.visualstudio.com/download)
  - [C# Dev Kit Extension](https://marketplace.visualstudio.com/items?itemName=ms-dotnettools.csdevkit)

## Install the .NET Aspire SDK

Open your preferred CLI (Powershell, Bash, or Terminal) and ensure you have the .NET CLI setup in your path by typing `dotnet --version`. You should see a result that looks like the image below:

![dotnet version](../images/dotnet_version.png)

next up, we need to ensure we have the latest .NET Workload metadata, so that we are installing the correct verson of Aspire:

```shell
dotnet workload update
```

Next you want to install the .NET Aspire workload:

```shell
dotnet workload install aspire
```

:bulb: Congrats! You're ready for the workshop! :bulb: [Click Here](../../Challenge-00.md) to return to Challenge 0!