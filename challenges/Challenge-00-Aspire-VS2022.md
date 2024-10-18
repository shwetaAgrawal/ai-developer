### [< Back to Challenge 0](./Challenge-00.md)

# Setting up the .NET Aspire SDK
The instructions in this document will help you install .NET Aspire SDK. There are a few pre-requisites we assume you have installed bellow:

- [.NET 8 SDK](https://dotnet.microsoft.com/download/dotnet/8.0)
- Visual Studio 17.10 or newer:
  - [Visual Studio 2022](https://visualstudio.microsoft.com/vs/)
- .NET Aspire 8.2 SDK

## Install the .NET Aspire SDK
To install the .NET Aspire workload into Visual Studio 2022, launch the Visual Studio installer.
1. Open the Visual Studio Installer. (Search for `Visual Studio Installer` from your Start Menu)
1. Ensure you are on 17.10. If you are not, select `Update` first before continuing.
1. Select **Modify** next to Visual Studio 2022.
1. Select **Individual Components** from the ribbon along the top.
1. Search for `Aspire` and select the `.NET Aspire SDK`
1. Click the **Modify** button at the bottom and wait until the installer is complete.

:bulb: If you already have .NET Aspire SDK :bulb:
Make sure you are running the latest version of the .NET Aspire SDK:
1. Open your terminal, and run `dotnet workload list`.
1. If your Aspire version number is lower than `8.2.0`, run `dotnet workload update` to ensure that you get the latest updates.


:bulb: Congrats! You're ready for the Hackathon! :bulb: [Click Here](./Challenge-00.md) to return to Challenge 0!