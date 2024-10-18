var builder = DistributedApplication.CreateBuilder(args);

builder.AddProject<Projects.BlazorAI>("blazor-aichat")
    .WithExternalHttpEndpoints();

builder.Build().Run();
