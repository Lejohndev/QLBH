﻿using System.ComponentModel.DataAnnotations;

namespace MyWebApp.Models
{
    public class CategoryModel
    {
        [Key]
        public int Id { get; set; }
        [Required,MinLength(4, ErrorMessage ="Yêu cầu nhập Tên danh mục")]
        public string Name { get; set; }
        [Required, MinLength(4, ErrorMessage = "Yêu cầu nhập Tên danh mục")]    

        public string Description { get; set; }
        [Required]
        public string Slug { get; set; }
        public int Status { get; set; }

    }
}
