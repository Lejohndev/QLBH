using MyWebApp.Models;

namespace MyWebApp.Services
{
    public interface IRecommendationService
    {
        Task<List<ProductModel>> GetRecommendedProductsAsync(long productId);
    }
}

