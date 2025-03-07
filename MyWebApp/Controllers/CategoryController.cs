using Microsoft.AspNetCore.Mvc;

namespace MyWebApp.Controllers
{
    public class CategoryController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }
    }
}
