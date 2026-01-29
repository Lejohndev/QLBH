using Microsoft.AspNetCore.Mvc;
using MyWebApp.Models;
using MyWebApp.Models.ViewModels;
using MyWebApp.Repository;
using System.Security.Claims;
namespace MyWebApp.Controllers
{
  public class CartController : Controller
  {
    private readonly DataContext _dataContext;
    public CartController(DataContext _context)
    {
      _dataContext = _context;
    }

    public IActionResult Index()
    {
      List<CartItemModel> cartItems = HttpContext.Session.GetJson<List<CartItemModel>>("Cart") ?? new List<CartItemModel>();
      CheckoutViewModel vm = new()
      {
        CartItems = cartItems,
        GrandTotal = cartItems.Sum(x => x.Quantity * x.Price)
      };
      
      var userEmail = User.FindFirstValue(System.Security.Claims.ClaimTypes.Email);
      if (userEmail != null)
      {
          vm.Address.Email = userEmail;
      }

      return View(vm);
    }
    public IActionResult Checkout()
    {
      return RedirectToAction("Index", "Checkout");
    }
    public async Task<IActionResult> Add(long Id, int quantity = 1)
    {
        ProductModel product = await _dataContext.Products.FindAsync(Id);
        List<CartItemModel> cart = HttpContext.Session.GetJson<List<CartItemModel>>("Cart") ?? new List<CartItemModel>();
        CartItemModel cartItem = cart.FirstOrDefault(c => c.ProductId == Id);

        if (cartItem == null)
        {
            cart.Add(new CartItemModel(product) { Quantity = quantity });
        }
        else
        {
            cartItem.Quantity += quantity;
        }
        HttpContext.Session.SetJson("Cart", cart);

        if (Request.Headers["X-Requested-With"] == "XMLHttpRequest")
        {
            return Json(new { 
                success = true, 
                message = "Item has been added to cart successfully", 
                totalItems = cart.Sum(x => x.Quantity) 
            });
        }

        TempData["success"] = " Item has been added to cart successfully";
        return Redirect(Request.Headers["referer"].ToString());
    }

    public async Task<IActionResult> BuyNow(long Id, int quantity = 1)
    {
        ProductModel product = await _dataContext.Products.FindAsync(Id);
        List<CartItemModel> cart = HttpContext.Session.GetJson<List<CartItemModel>>("Cart") ?? new List<CartItemModel>();
        CartItemModel cartItem = cart.FirstOrDefault(c => c.ProductId == Id);

        if (cartItem == null)
        {
            cart.Add(new CartItemModel(product) { Quantity = quantity });
        }
        else
        {
            cartItem.Quantity += quantity;
        }
        HttpContext.Session.SetJson("Cart", cart);
        
        return RedirectToAction("Index");
    }

    [HttpPost]
    public IActionResult Increase(long Id)
    {
      var cart = HttpContext.Session.GetJson<List<CartItemModel>>("Cart") ?? new List<CartItemModel>();
      var cartItem = cart.FirstOrDefault(c => c.ProductId == Id);
      if (cartItem == null)
      {
        return Json(new { success = false, message = "Item not found" });
      }
      cartItem.Quantity += 1;
      if (cart.Count == 0)
      {
        HttpContext.Session.Remove("Cart");

      }
      else
      {
        HttpContext.Session.SetJson("Cart", cart);
      }
      var itemTotal = cartItem.Quantity * cartItem.Price;
      var grandTotal = cart.Sum(x => x.Quantity * x.Price);
      return Json(new
      {
        success = true,
        quantity = cartItem.Quantity,
        itemTotal,
        grandTotal,
        removed = false
      });

    }
    [HttpPost]
    public IActionResult Decrease(long Id)
    {
      var cart = HttpContext.Session.GetJson<List<CartItemModel>>("Cart") ?? new List<CartItemModel>();
      var cartItem = cart.FirstOrDefault(c => c.ProductId == Id);
      if (cartItem == null)
      {
        return Json(new { success = false, message = "Item not found" });
      }
      if (cartItem.Quantity > 1)
      {
        cartItem.Quantity -= 1;
      }
      else
      {
        cart.RemoveAll(p => p.ProductId == Id);
      }

      if (cart.Count == 0)
      {
        HttpContext.Session.Remove("Cart");
      }
      else
      {
        HttpContext.Session.SetJson("Cart", cart);
      }
      var removed = cart.All(c => c.ProductId != Id);
      var itemTotal = removed ? 0 : cart.First(c => c.ProductId == Id).Quantity * cart.First(c => c.ProductId == Id).Price;
      var grandTotal = cart.Sum(x => x.Quantity * x.Price);

      return Json(new
      {
        success = true,
        quantity = removed ? 0 : cart.First(c => c.ProductId == Id).Quantity,
        itemTotal,
        grandTotal,
        removed
      });


    }
    [HttpPost]
    public IActionResult Remove(long Id)
    {
      var cart = HttpContext.Session.GetJson<List<CartItemModel>>("Cart") ?? new List<CartItemModel>();
      cart.RemoveAll(p => p.ProductId == Id);
      if (cart.Count == 0)
      {
        HttpContext.Session.Remove("Cart");
      }
      else
      {
        HttpContext.Session.SetJson("Cart", cart);

      }

      var grandTotal = cart.Sum(x => x.Quantity * x.Price);
      return Json(new
      {
        success = true,
        grandTotal,
        removed = true
      });
    }
    public async Task<IActionResult> Clear(long Id)
    {
      HttpContext.Session.Remove("Cart");
      TempData["success"] = "Clear all Item of cart Successfully";

      return RedirectToAction("Index");
    }
  }
}
