using BlazorAI;
using BlazorAI.Components;
using BlazorAI.Components.Models;
using BlazorAI.Components.Pages.Controls;
using BlazorAI.Extensions;
using BlazorAI.Options;
using Microsoft.FluentUI.AspNetCore.Components;
using Microsoft.Identity.Client;
using Microsoft.Identity.Web;
using Microsoft.Identity.Web.UI;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Plugins.MsGraph;
using Microsoft.SemanticKernel.Plugins.OpenApi;
using System.Net.Http.Headers;
using System.Security.Cryptography.X509Certificates;
using LogLevel = Microsoft.Extensions.Logging.LogLevel;

#pragma warning disable SKEXP0001 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.
#pragma warning disable SKEXP0050 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.
#pragma warning disable SKEXP0010 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.
#pragma warning disable SKEXP0040 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.
#pragma warning disable SKEXP0020 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.

var builder = WebApplication.CreateBuilder(args);

// Add service defaults & Aspire components.
builder.AddServiceDefaults();

var initialScopes = builder.Configuration.GetValue<string>("DownstreamApi:Scopes")?.Split(' ');

builder.Services.AddMicrosoftIdentityWebAppAuthentication(builder.Configuration, "AzureAd")
	.EnableTokenAcquisitionToCallDownstreamApi(initialScopes)
	.AddMicrosoftGraph(builder.Configuration.GetSection("DownstreamApi"))
	.AddInMemoryTokenCaches();


builder.Services.AddLogging(loggingBuilder =>
{
	loggingBuilder.AddConsole();
	loggingBuilder.AddDebug();
});

builder.Services.AddAuthorization(
	options => options.FallbackPolicy = options.DefaultPolicy);


builder.Services.AddRazorPages();
builder.Services.AddRazorComponents()
	.AddInteractiveServerComponents()
	.AddMicrosoftIdentityConsentHandler();

builder.Services.AddControllersWithViews()
	.AddMicrosoftIdentityUI();

builder.Services.AddSignalR();
builder.Services.AddFluentUIComponents();

builder.Services.AddScoped<UserProfileBase>();
builder.Services.AddScoped<AppState>();
builder.Services.AddHttpClient();

var app = builder.Build();
app.UseAuthentication();
app.UseAuthorization();

if (app.Environment.IsDevelopment())
{
	app.UseDeveloperExceptionPage();
}
else
{
	app.UseExceptionHandler("/Error");
	app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();

app.UseRouting();
app.UseAntiforgery();
app.MapBlazorHub(options =>
{
	options.CloseOnAuthenticationExpiration = true;
}).WithOrder(-1);

app.MapDefaultEndpoints();

app.MapRazorComponents<App>().AddInteractiveServerRenderMode();

app.MapControllers();

app.Run();
