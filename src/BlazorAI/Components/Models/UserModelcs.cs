using System.ComponentModel.DataAnnotations;

namespace BlazorAI.Components.Models;

public class UserModel
{
	[Required]
	public string Name { get; set; }

	[Required]
	public int Age { get; set; }
}
