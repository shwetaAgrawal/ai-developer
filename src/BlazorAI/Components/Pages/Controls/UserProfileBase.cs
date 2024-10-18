using BlazorAI.Components.Models;
using Microsoft.AspNetCore.Components;
using Microsoft.Graph;
using Microsoft.Identity.Client;
using Microsoft.Identity.Web;
using System.Security.Cryptography;

namespace BlazorAI.Components.Pages.Controls
{
	/// <summary>
	/// Base class for UserProfile component.
	/// Injects GraphServiceClient and calls Microsoft Graph /me endpoint.
	/// </summary>
	public class UserProfileBase : ComponentBase
	{
		[Inject] private GraphServiceClient GraphClient { get; set; } = null!;

		[Inject] private MicrosoftIdentityConsentAndConditionalAccessHandler ConsentHandler { get; set; } = null!;

		[Inject] private AppState AppState { get; set; } = null!;

		[Inject] private ILogger<UserProfileBase> logger { get; set; } = null!;

		public string? PhotoBytes { get; set; }
		public string UserInitials { get; set; }

		protected User _user = new User();
		protected override async Task OnInitializedAsync()
		{
			await GetUserProfile();
			AppState.OnChange += AppState_OnChange;
		}

		private async void AppState_OnChange()
		{
			await GetUserProfile();
		}

		/// <summary>
		/// Retrieves user information from Microsoft Graph /me endpoint.
		/// </summary>
		/// <returns></returns>
		private async Task GetUserProfile()
		{
			try
			{
				var request = GraphClient.Me.Request();
				_user = await request.GetAsync();

				await GetPhoto();

				// Set user initials
				GetUserInitials(_user.GivenName, _user.Surname);
			}
			catch (ServiceException ex) when (ex.InnerException?.Message?.StartsWith("IDW10502") == true)
			{
				// Handle the Login Required exception. This is thrown when the user is not authenticated.
				ConsentHandler.HandleException(ex);
			}
			catch (Exception ex)
			{
				logger.LogError(ex.Message);
				if (ex.InnerException != null)
				{
					logger.LogError(ex.InnerException.Message);
				}
			}
		}

		private async Task GetPhoto()
		{
			try
			{
				Stream photo = await GraphClient.Me.Photo.Content.Request().GetAsync();
				if (photo != null)
				{
					using (var reader = new StreamReader(new CryptoStream(photo, new ToBase64Transform(), CryptoStreamMode.Read)))
					{
						var photoBytes = await reader.ReadToEndAsync();
						photoBytes = $"data:image/jpeg;base64,{photoBytes}";
						PhotoBytes = photoBytes;
						await InvokeAsync(StateHasChanged);
					}
				}
				else
				{
					PhotoBytes = null;
				}
			}
			catch (ServiceException ex) when (ex.InnerException?.Message?.StartsWith("IDW10502") == true)
			{
				// Handle the Login Required exception. This is thrown when the user is not authenticated.
				ConsentHandler.HandleException(ex);
			}
			catch (ServiceException ex) when (ex.Error.Code == "ImageNotFound")
			{
				// Handle the case where the photo is not found
				PhotoBytes = null;
				logger.LogInformation("User doesn't have a profile photo. Continuing.");
			}
			catch (Exception ex)
			{
				logger.LogError(ex.Message);
				if (ex.InnerException != null)
				{
					logger.LogError(ex.InnerException.Message);
				}
			}
		}

		/// <summary>
		/// Gets the initials from the given name and surname.
		/// </summary>
		/// <param name="givenName">The given name of the user.</param>
		/// <param name="surname">The surname of the user.</param>
		/// <returns>The initials of the user.</returns>
		private void GetUserInitials(string givenName, string surname)
		{
			if (string.IsNullOrWhiteSpace(givenName) || string.IsNullOrWhiteSpace(surname))
			{
				UserInitials = string.Empty;
				return;
			}

			UserInitials = $"{givenName[0]}{surname[0]}".ToUpper();
		}
	}
}
