using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using MyWebApp.Repository;
using System.Collections.Generic;
using MyWebApp.Models;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;

namespace MyWebApp.Controllers
{

    public class VietQRController : Controller
    {
        private readonly DataContext _dataContext;
        private readonly ILogger<VietQRController> _logger;
        private const string BankId = "970416"; // ACB
        private const string AccountNumber = "0349528312";
        private const string Template = "print";

        public VietQRController(DataContext context, ILogger<VietQRController> logger)
        {
            _dataContext = context;
            _logger = logger;
        }

        public async Task<IActionResult> GenerateQrCode(int i)
        {
            var order = await _dataContext.Orders.Include(o => o.OrderDetails).FirstOrDefaultAsync(o => o.Id == i);

            if (order == null)
            {
                // Handle order not found
                return View("Error"); // Or a specific view for this case
            }

            var amount = order.OrderDetails.Sum(d => d.Price * d.Quantity);
            var orderCode = order.OrderCode;

            var addInfo = orderCode;
            var qrCodeUrl = $"https://img.vietqr.io/image/{BankId}-{AccountNumber}-{Template}.png?amount={amount}&addInfo={addInfo}";
            ViewBag.QrCodeUrl = qrCodeUrl;
            ViewBag.OrderCode = orderCode;
            ViewBag.Amount = amount;
            ViewBag.BankAccountNumber = AccountNumber;
            ViewBag.BankName = "Ngân hàng ACB"; // Or fetch dynamically if needed
            return View();
        }

        [HttpPost]
        [AllowAnonymous]
        public async Task<IActionResult> PaymentNotification([FromBody] VietQRPaymentNotification notification)
        {
            _logger.LogInformation("Received VietQR Payment Notification: {@Notification}", notification);

            if (notification == null || string.IsNullOrEmpty(notification.OrderCode))
            {
                _logger.LogWarning("Received invalid payment notification.");
                return BadRequest();
            }

            var order = await _dataContext.Orders.FirstOrDefaultAsync(o => o.OrderCode == notification.OrderCode);

            if (order != null && notification.Success)
            {
                order.Status = 2; // Paid
                _dataContext.Update(order);
                await _dataContext.SaveChangesAsync();
                HttpContext.Session.Remove("Cart");
                _logger.LogInformation("Order {OrderCode} status updated to Paid.", notification.OrderCode);

                return Ok();
            }

            _logger.LogWarning("Payment notification for order {OrderCode} failed or order not found.", notification.OrderCode);
            return BadRequest();
        }
        [HttpGet]
        public async Task<IActionResult> CheckPaymentStatus(string orderCode)
        {
            var order = await _dataContext.Orders.FirstOrDefaultAsync(o => o.OrderCode == orderCode);
            if (order != null)
            {
                return new JsonResult(new { status = order.Status });
            }
            return new JsonResult(new { status = 0 });
        }
    }

}


    
