using Microsoft.AspNetCore.Mvc;

namespace MyWebApp.Controllers
{
    public class ProductController : Controller
    {
        public IActionResult Index()
        { 
             return View();
        }
        public IActionResult Details()
        {
            return View();
        }
    }
}
