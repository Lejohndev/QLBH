using MyWebApp.Models;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

public class OrderAddress
{
    public int Id { get; set; }

    public int OrderId { get; set; }
    [ForeignKey("OrderId")]

    public string Email { get; set; }

 
    public string FullName { get; set; }

    
    public string Address1 { get; set; }

    public string Address2 { get; set; }

   
    public string ZipCode { get; set; }


    public string Country { get; set; }

   
    public string State { get; set; }

    
    public string Phone { get; set; }

    public string Note { get; set; }

    public OrderModel Order { get; set; }

}
