using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace MyWebApp.Migrations
{
    /// <inheritdoc />
    public partial class mewadd2 : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.RenameColumn(
                name: "id",
                table: "OrderAddresses",
                newName: "Id");

            migrationBuilder.RenameColumn(
                name: "Address",
                table: "OrderAddresses",
                newName: "ZipCode");

            migrationBuilder.AddColumn<string>(
                name: "Address1",
                table: "OrderAddresses",
                type: "nvarchar(max)",
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "Address2",
                table: "OrderAddresses",
                type: "nvarchar(max)",
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "Note",
                table: "OrderAddresses",
                type: "nvarchar(max)",
                nullable: true);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "Address1",
                table: "OrderAddresses");

            migrationBuilder.DropColumn(
                name: "Address2",
                table: "OrderAddresses");

            migrationBuilder.DropColumn(
                name: "Note",
                table: "OrderAddresses");

            migrationBuilder.RenameColumn(
                name: "Id",
                table: "OrderAddresses",
                newName: "id");

            migrationBuilder.RenameColumn(
                name: "ZipCode",
                table: "OrderAddresses",
                newName: "Address");
        }
    }
}
