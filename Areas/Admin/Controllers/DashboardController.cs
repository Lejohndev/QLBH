using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using MyWebApp.Models;
using MyWebApp.Repository;

namespace MyWebApp.Areas.Admin.Controllers
{

    [Area("Admin")]
    [Route("Admin")]
    //[Authorize(Roles = "Admin,Seller")]
    public class DashboardController : Controller
    {
        private readonly DataContext _dataContext;
        private readonly IWebHostEnvironment _webHostEnvironment;
        public DashboardController(DataContext context, IWebHostEnvironment webHostEnvironment)
        {
            _dataContext = context;
            _webHostEnvironment = webHostEnvironment;
        }
        public IActionResult Index()
        {

            var count_product = _dataContext.Products.Count();
            var count_order = _dataContext.Orders.Count();
            var count_category = _dataContext.Categories.Count();
            var count_user = _dataContext.Users.Count();
            ViewBag.CountProduct = count_product;
            ViewBag.CountOrder = count_order;
            ViewBag.CountCategory = count_category;
            ViewBag.CountUser = count_user;
            return View();
        }
        [HttpPost]
        public async Task<IActionResult> GetCharData()
        {
            var data = _dataContext.Statistical
                .Select(s => new
                {
                    data = s.DateCrated.ToString("yyyy-MM--dd"),
                    sold = s.Sold,
                    quantity = s.Revenue,
                    profit = s.Profit
                })
                .ToList();
            return Json(data);
        }
    }
}
