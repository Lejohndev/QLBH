using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using MyWebApp.Repository;
using System.Text;
using System.Xml;

namespace MyWebApp.Controllers
{
    public class SitemapController : Controller
    {
        private readonly DataContext _dataContext;
        private readonly IConfiguration _configuration;

        public SitemapController(DataContext dataContext, IConfiguration configuration)
        {
            _dataContext = dataContext;
            _configuration = configuration;
        }

        [Route("/sitemap.xml")]
        public async Task<IActionResult> Index()
        {
            var domain = _configuration["Domain"];
            var sitemapBuilder = new StringBuilder();
            sitemapBuilder.AppendLine("<?xml version=\"1.0\" encoding=\"UTF-8\"?>");
            sitemapBuilder.AppendLine("<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">");

            // Add static URLs
            AddUrl(sitemapBuilder, $"{domain}", "1.0");

            // Add products
            var products = await _dataContext.Products.ToListAsync();
            foreach (var product in products)
            {
                AddUrl(sitemapBuilder, $"{domain}/product/detail/{product.Id}", "0.9");
            }

            // Add categories
            var categories = await _dataContext.Categories.ToListAsync();
            foreach (var category in categories)
            {
                AddUrl(sitemapBuilder, $"{domain}/category/{category.Slug}", "0.8");
            }

            // Add brands
            var brands = await _dataContext.Brands.ToListAsync();
            foreach (var brand in brands)
            {
                AddUrl(sitemapBuilder, $"{domain}/brand/{brand.Slug}", "0.8");
            }


            sitemapBuilder.AppendLine("</urlset>");

            return Content(sitemapBuilder.ToString(), "application/xml", Encoding.UTF8);
        }

        private void AddUrl(StringBuilder sitemapBuilder, string url, string priority)
        {
            sitemapBuilder.AppendLine("  <url>");
            sitemapBuilder.AppendLine($"    <loc>{url}</loc>");
            sitemapBuilder.AppendLine($"    <priority>{priority}</priority>");
            sitemapBuilder.AppendLine("  </url>");
        }
    }
}
