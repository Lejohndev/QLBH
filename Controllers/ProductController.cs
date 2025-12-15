using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using MyWebApp.Models;
using MyWebApp.Repository;
using MyWebApp.Services;

namespace MyWebApp.Controllers
{

    public class ProductController : Controller
    {
        private readonly DataContext _dataContext;
        private readonly IRecommendationService _recommendationService;

        public ProductController(DataContext context, IRecommendationService recommendationService)
        {
            _dataContext = context;
            _recommendationService = recommendationService;
        }
        public IActionResult Index()
        {
            return View();
        }
        public async Task<IActionResult> Search(string searchTerm)
        {
            var products = await _dataContext.Products
            .Where(p => p.Name.Contains(searchTerm) || p.Description.Contains(searchTerm))
            .ToListAsync();
            ViewBag.Keyword = searchTerm;
            return View(products);
        }
        public async Task<IActionResult> Detail(long Id)
        {
            if (Id == null) return RedirectToAction("Index");

            var productsById = await _dataContext.Products
                .Include(p => p.Category)
                .Include(p => p.Brand)
                .Where(p => p.Id == Id)
                .FirstOrDefaultAsync();

            if (productsById == null) return RedirectToAction("Index");

            var relatedProducts = await _dataContext.Products
                .Include(p => p.Category)
                .Include(p => p.Brand)
                .Where(p => p.CategoryId == productsById.CategoryId && p.Id != productsById.Id)
                .Take(4)
                .ToListAsync();

            // Get recommended products based on association rules
            var recommendedProducts = await _recommendationService.GetRecommendedProductsAsync(Id);

            // Debug: Ensure we have recommended products
            if (recommendedProducts == null || !recommendedProducts.Any())
            {
                // If no recommendations, you might want to show related products as fallback
                // or leave it empty
            }

            ViewBag.RelatedProducts = relatedProducts;
            ViewBag.RecommendedProducts = recommendedProducts ?? new List<ProductModel>();
            return View(productsById);
        }

    }
}
