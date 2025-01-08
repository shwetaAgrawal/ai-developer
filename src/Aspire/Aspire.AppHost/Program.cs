var builder = DistributedApplication.CreateBuilder(args);

var workitems = builder.AddProject("workitems-api", @"..\..\WorkItems\WorkItems.csproj");

builder.AddProject<Projects.BlazorAI>("blazor-aichat")
    .WithExternalHttpEndpoints()
    .WithReference(workitems);

builder.Build().Run();
