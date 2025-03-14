using Microsoft.AspNetCore.Identity;

namespace MyWebApp.Models
{
    public class AppUserModel: IdentityUser
    {
        public string Occupation { get; set; }
    }
}
