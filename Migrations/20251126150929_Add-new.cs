using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace MyWebApp.Migrations
{
    /// <inheritdoc />
    public partial class Addnew : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<int>(
                name: "OrderModelId",
                table: "OrderAddresses",
                type: "int",
                nullable: true);

            migrationBuilder.CreateIndex(
                name: "IX_OrderAddresses_OrderModelId",
                table: "OrderAddresses",
                column: "OrderModelId");

            migrationBuilder.AddForeignKey(
                name: "FK_OrderAddresses_Orders_OrderModelId",
                table: "OrderAddresses",
                column: "OrderModelId",
                principalTable: "Orders",
                principalColumn: "Id");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_OrderAddresses_Orders_OrderModelId",
                table: "OrderAddresses");

            migrationBuilder.DropIndex(
                name: "IX_OrderAddresses_OrderModelId",
                table: "OrderAddresses");

            migrationBuilder.DropColumn(
                name: "OrderModelId",
                table: "OrderAddresses");
        }
    }
}
