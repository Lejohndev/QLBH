using System.Diagnostics;
using System.Security.Claims;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using MyWebApp.Models;
using MyWebApp.Repository;
using MyWebApp.Services;

namespace MyWebApp.Controllers;

public class HomeController : Controller
{
    private readonly DataContext _dataContext;
    private readonly ILogger<HomeController> _logger;
    private readonly HRecommendationService _recommendationService;

    public HomeController(ILogger<HomeController> logger, DataContext context, HRecommendationService recommendationService)
    {
        _logger = logger;
        _dataContext = context;
        _recommendationService = recommendationService;
    }

    public async Task<IActionResult> Index()
    {
        var products = await _dataContext.Products
            .Include(p => p.Category)
            .Include(p => p.Brand)
            .ToListAsync();

        var recommendedProducts = new List<ProductModel>();
        var hasUserPurchased = false;

        // Kiểm tra user đã login
        if (User.Identity?.IsAuthenticated == true)
        {
            // Lấy email từ claims (đó là cách CheckoutController lưu UserName)
            var userEmail = User.FindFirstValue(ClaimTypes.Email);
            _logger.LogInformation($"DEBUG: User email from claims: {userEmail}");

            if (!string.IsNullOrEmpty(userEmail))
            {
                // Kiểm tra user có lịch sử mua hàng không (dùng email)
                hasUserPurchased = await _dataContext.OrderDetails
                    .AsNoTracking()
                    .AnyAsync(od => od.UserName == userEmail);

                _logger.LogInformation($"DEBUG: User has purchased (by email): {hasUserPurchased}");

                // Nếu user đã mua hàng, lấy recommended products
                if (hasUserPurchased)
                {
                    _logger.LogInformation($"DEBUG: Getting recommended products for user email: {userEmail}");
                    recommendedProducts = await _recommendationService.GetRecommendedProductsByUserAsync(userEmail);
                    _logger.LogInformation($"DEBUG: Recommended products count: {recommendedProducts.Count}");
                }
            }
        }
        else
        {
            _logger.LogInformation("DEBUG: User not authenticated");
        }

        ViewBag.RecommendedProducts = recommendedProducts;
        ViewBag.HasUserPurchased = hasUserPurchased;
        return View(products);
    }

    public IActionResult Privacy()
    {
        return View();
    }

    [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
    public IActionResult Error()
    {
        return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
    }
}