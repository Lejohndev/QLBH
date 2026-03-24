using System.ComponentModel.DataAnnotations.Schema;

namespace MyWebApp.Models
{
    public class OrderModel
    {
        public int Id { get; set; }
        public string OrderCode { get; set; }
        public string UserName { get; set; }
        public DateTime CreatedDate { get; set; }
        public int Status { get; set; }
        public long PayOSOrderCode { get; set; }
        public ICollection<OrderDetails>? OrderDetails { get; set; } = new List<OrderDetails>();
        public ICollection<OrderAddress>? OrderAddresses { get; set; } = new List<OrderAddress>();
        [NotMapped]
        public decimal? Total { get; set; }
    }
}
