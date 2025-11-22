using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using MyWebApp.Models;
using MyWebApp.Models.ViewModels;
using MyWebApp.Repository;
using System.Security.Claims;


namespace MyWebApp.Controllers
{
    public class AccountController : Controller
    {
        private UserManager<AppUserModel> _userManager;
        private SignInManager<AppUserModel> _signInManager;
        private readonly DataContext _dataContext;
        public AccountController(SignInManager<AppUserModel> signInManager,
            UserManager<AppUserModel> userManager,
            DataContext context)
        {
            _dataContext = context;
            _userManager = userManager;
            _signInManager = signInManager;
        }
        public IActionResult Login(string returnUrl)
        {
            return View(new LoginViewModel { ReturnUrl = returnUrl});
        }
      
        [HttpPost]
        public async Task<IActionResult> Login (LoginViewModel loginVM)
        {
            if(ModelState.IsValid){
                Microsoft.AspNetCore.Identity.SignInResult result = await _signInManager.PasswordSignInAsync(loginVM.Username, loginVM.Password, false, false);
                if(result.Succeeded){
                    return Redirect(loginVM.ReturnUrl ?? "/");
                }
               ModelState.AddModelError("", "Tên người dùng hoặc mật khẩu không đúng");
            }
            return View(loginVM);
        }
        public IActionResult Create()
        {
            return View();
        }

        [HttpPost]
       public  async Task<IActionResult> Create(UserModel user)
        {
            if (ModelState.IsValid)
            {
                AppUserModel newUser = new AppUserModel { UserName = user.Username, Email = user.Email };
                IdentityResult result = await _userManager.CreateAsync(newUser,user.Password);
                if (result.Succeeded)
                {
                    TempData["sucsess"] = "Tạo Người dùng thành công";
                    return Redirect("/account/login");
                }
                foreach(IdentityError error in result.Errors)
                {
                    ModelState.AddModelError("", error.Description);
                }
            }
            return View(user);
        }

        public async Task<IActionResult> Logout(string returnUrl= "/")
        {
            await _signInManager.SignOutAsync();
            return Redirect(returnUrl);
        }
        public async Task<IActionResult> History()
        {
          if ((bool)!User.Identity?.IsAuthenticated)
			{
				// User is not logged in, redirect to login
				return RedirectToAction("Login", "Account"); // Replace "Account" with your controller name
			}
		
			var userEmail = User.FindFirstValue(ClaimTypes.Email);


            var orders = await _dataContext.Orders
                .Where(o => o.UserName == userEmail)
                .Include(o => o.OrderDetails)           // Load chi tiết đơn
                .ThenInclude(od => od.Product)         // Load thông tin sản phẩm
                .OrderByDescending(o => o.Id)
                .ToListAsync();

            ViewBag.UserEmail = userEmail;
            return View(orders);
        }

        public async Task<IActionResult> CancelOrder(string ordercode)
        {
            if ((bool)!User.Identity.IsAuthenticated)
            {
                return RedirectToAction("Login", "Account");
            }

            try
            {
                var order = await _dataContext.Orders.Where(o => o.OrderCode == ordercode).FirstAsync();
                order.Status = 3;
                _dataContext.Update(order);

                await _dataContext.SaveChangesAsync();


            }
            catch (Exception ex)
            {
                return BadRequest("An error occurred while canceling the order.");
            }
            return RedirectToAction("History", "Account");
        }

    }
}
    


