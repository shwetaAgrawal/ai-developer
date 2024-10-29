using BlazorAI.Components.Models;
using Microsoft.Graph;
using Microsoft.SemanticKernel;
using System.ComponentModel;
using System.Net.Http.Headers;

namespace BlazorAI.Plugins;

public class MsGraphPlugin
{
	private GraphServiceClient _graphServiceClient;
	private IHttpClientFactory _httpClientFactory;
	private AppState _appState;

	public MsGraphPlugin(GraphServiceClient graphServiceClient, IHttpClientFactory httpClientFactory, AppState appState)
	{
		_graphServiceClient = graphServiceClient;
		_httpClientFactory = httpClientFactory;
		_appState = appState;
	}

	[KernelFunction("update_profile_picture")]
	[Description("Updates the user's profile picture in Microsoft Graph.")]
	[return: Description("Response from Microsoft Graph API.")]
	public async Task<string> UpdateUserProfilePictureAsync(string imageBase64)
	{
		try
		{

			// Convert base64 string to byte array
			byte[] imageData = Convert.FromBase64String(imageBase64);

			var response =  await _graphServiceClient.Me.Photo.Content.Request().PutAsync(new MemoryStream(imageData));
			_appState.NotifyStateChanged();
			return "Profile picture updated successfully.";
		}
		catch (Exception ex)
		{
			return $"Could not update profile picture: Error: {ex.Message}";
		}
	}

	[KernelFunction("update_profile_picture_from_url")]
	[Description("Updates the user's profile picture in Microsoft Graph from an image URL.")]
	[return: Description("Response from Microsoft Graph API.")]
	public async Task<string> UpdateUserProfilePictureFromUrlAsync(string imageUrl)
	{
		try
		{
			using HttpClient httpClient = _httpClientFactory.CreateClient();

			// Download image data from the provided URL
			byte[] imageData = await httpClient.GetByteArrayAsync(imageUrl);

			var response = await _graphServiceClient.Me.Photo.Content.Request().PutAsync(new MemoryStream(imageData));
			_appState.NotifyStateChanged();
			return "Profile picture updated successfully.";


		}
		catch (Exception ex)
		{
			return $"Failed to update profile picture. Error: {ex.Message}";
		}
	}
}
