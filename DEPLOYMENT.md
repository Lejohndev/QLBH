# Hướng dẫn triển khai MyWebApp lên Azure

Hướng dẫn từng bước theo chuẩn DevOps để đưa project ASP.NET Core lên Azure App Service và gắn tên miền tùy chỉnh.

---

## Phần 1: Chuẩn bị trước khi triển khai

### 1.1. Yêu cầu

- Tài khoản Azure (có thể dùng [Azure Free Trial](https://azure.microsoft.com/free/))
- Azure CLI hoặc dùng Azure Portal
- Tên miền đã mua (ví dụ: `windshop.vn`)
- Git (nếu dùng GitHub Actions để deploy)

### 1.2. Kiểm tra project

- [x] ASP.NET Core 8.0
- [x] SQL Server (Entity Framework Core)
- [x] Identity, Session, PayOS, Mail
- [x] Ảnh sản phẩm lưu tại `wwwroot/media/products` (lưu ý: trên App Service filesystem không persistent, cần chuyển sang Azure Blob Storage sau)

---

## Phần 2: Tạo tài nguyên trên Azure

### Bước 2.1: Đăng nhập Azure

```bash
az login
```

Mở trình duyệt để xác thực nếu cần.

### Bước 2.2: Tạo Resource Group

```bash
az group create --name rg-windshop-prod --location southeastasia
```

- `southeastasia` gần Việt Nam, latency tốt hơn
- Có thể đổi `rg-windshop-prod` theo tên project

### Bước 2.3: Tạo Azure SQL Database

```bash
# Tạo SQL Server (thay YOUR_ADMIN_USER và YOUR_STRONG_PASSWORD)
az sql server create \
  --name sql-windshop-prod \
  --resource-group rg-windshop-prod \
  --location southeastasia \
  --admin-user YOUR_ADMIN_USER \
  --admin-password "YOUR_STRONG_PASSWORD"

# Tạo database
az sql db create \
  --resource-group rg-windshop-prod \
  --server sql-windshop-prod \
  --name MyWebApp \
  --service-objective S0

# Cho phép Azure services kết nối (quan trọng)
az sql server firewall-rule create \
  --resource-group rg-windshop-prod \
  --server sql-windshop-prod \
  --name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0
```

**Lấy connection string:**

```bash
az sql db show-connection-string --client ado.net --server sql-windshop-prod --name MyWebApp
```

Thay `{your_password}` bằng mật khẩu admin đã đặt. Ví dụ:

```
Server=tcp:sql-windshop-prod.database.windows.net,1433;Initial Catalog=MyWebApp;Persist Security Info=False;User ID=YOUR_ADMIN_USER;Password=YOUR_STRONG_PASSWORD;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;
```

### Bước 2.4: Tạo App Service Plan

```bash
az appservice plan create \
  --name plan-windshop-prod \
  --resource-group rg-windshop-prod \
  --location southeastasia \
  --sku B1 \
  --is-linux false
```

- `B1`: Basic tier, phù hợp production nhỏ
- `--is-linux false`: chạy Windows (phù hợp ASP.NET Core classic)

### Bước 2.5: Tạo Web App

```bash
az webapp create \
  --name windshop-prod \
  --resource-group rg-windshop-prod \
  --plan plan-windshop-prod \
  --runtime "DOTNET:8"
```

- `windshop-prod` phải unique toàn Azure → URL: `https://windshop-prod.azurewebsites.net`
- Nếu bị trùng, đổi tên (ví dụ: `windshop-prod-2024`)

---

## Phần 3: Cấu hình App Service

### Bước 3.1: Thiết lập Connection String

Trên Azure Portal:

1. Vào **App Service** → **windshop-prod** → **Configuration** → **Application settings**
2. Thêm **Connection string**:
   - **Name:** `ConnectedDB`
   - **Value:** `Server=tcp:sql-windshop-prod.database.windows.net,1433;Initial Catalog=MyWebApp;Persist Security Info=False;User ID=...;Password=...;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;`
   - **Type:** SQL Azure

Hoặc dùng CLI:

```bash
az webapp config connection-string set \
  --name windshop-prod \
  --resource-group rg-windshop-prod \
  --connection-string-type SQLAzure \
  --settings ConnectedDB="Server=tcp:sql-windshop-prod.database.windows.net,1433;Initial Catalog=MyWebApp;Persist Security Info=False;User ID=YOUR_USER;Password=YOUR_PASSWORD;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;"
```

### Bước 3.2: Thiết lập Application Settings (bí mật)

**Không commit** PayOS, Mail, v.v. vào Git. Đặt qua Azure:

1. **Configuration** → **Application settings** → **New application setting**

Thêm từng cặp key-value:

| Name | Value | Ghi chú |
|------|-------|---------|
| `PayOS__ClientId` | `67537c7d-a050-46ab-92a0-2cf36515abc0` | Thay bằng key thật |
| `PayOS__ApiKey` | `...` | Thay bằng key thật |
| `PayOS__ChecksumKey` | `...` | Thay bằng key thật |
| `MailSettings__Mail` | `lethienhiep28012004@gmail.com` | Email gửi mail |
| `MailSettings__DisplayName` | `WindShop` | Tên hiển thị |
| `MailSettings__Password` | `ukca dlzx sedl leax` | App password Gmail |
| `MailSettings__Host` | `smtp.gmail.com` | |
| `MailSettings__Port` | `587` | |

**Lưu ý:** ASP.NET Core dùng `__` (double underscore) để map nested config. Nếu trong `appsettings.json` là `PayOS:ClientId` thì trên Azure dùng `PayOS__ClientId`.

### Bước 3.3: Bật .NET 8 runtime

```bash
az webapp config set \
  --name windshop-prod \
  --resource-group rg-windshop-prod \
  --net-framework-version "v8.0"
```

---

## Phần 4: Chạy Migration và publish database

### Bước 4.1: Cập nhật database trên Azure SQL

Trên máy local, tạm thời đổi connection string trong `appsettings.json` (hoặc `appsettings.Development.json`) sang Azure SQL, rồi chạy:

```bash
cd d:\MyProject\QLBH
dotnet ef database update
```

Sau khi xong, **đổi lại** connection string về local để tránh nhầm lẫn.

### Bước 4.2: Seed admin (nếu cần)

Nếu `SeedData.SeedAdminAsync` chạy khi app khởi động lần đầu, admin sẽ được tạo tự động sau lần deploy đầu tiên. Nếu không, cần chạy script seed thủ công hoặc tạo user qua Identity UI.

---

## Phần 5: Deploy code lên App Service

### Cách 1: Publish từ Visual Studio / VS Code

1. Chuột phải project → **Publish**
2. Chọn **Azure** → **Azure App Service (Windows)**
3. Đăng nhập Azure, chọn **windshop-prod**
4. Publish

### Cách 2: Publish bằng CLI

```bash
cd d:\MyProject\QLBH
dotnet publish -c Release -o ./publish
```

Sau đó dùng **Zip Deploy**:

```bash
cd publish
zip -r ../deploy.zip .
cd ..
az webapp deployment source config-zip \
  --resource-group rg-windshop-prod \
  --name windshop-prod \
  --src deploy.zip
```

Trên Windows PowerShell:

```powershell
Compress-Archive -Path .\publish\* -DestinationPath deploy.zip
az webapp deployment source config-zip --resource-group rg-windshop-prod --name windshop-prod --src deploy.zip
```

### Cách 3: GitHub Actions (CI/CD)

1. **App Service** → **Deployment Center** → **GitHub** → Authorize
2. Chọn repo, branch (ví dụ `main`)
3. Azure tạo workflow `.github/workflows/xxx.yml` tự động
4. Mỗi lần push lên `main` sẽ deploy

**Quan trọng:** Đảm bảo Connection String và App Settings đã cấu hình trên Azure, không cần (và không nên) đưa vào repo.

---

## Phần 6: Gắn tên miền tùy chỉnh

### Bước 6.1: Thêm custom domain trên App Service

1. **App Service** → **windshop-prod** → **Custom domains**
2. **Add custom domain**
3. Nhập domain: `www.windshop.vn` hoặc `windshop.vn`
4. Azure sẽ gợi ý cấu hình DNS

### Bước 6.2: Cấu hình DNS tại nhà cung cấp domain

Tùy nhà cung cấp (GoDaddy, Cloudflare, Matbao, v.v.):

**Nếu dùng CNAME (khuyến nghị cho subdomain `www`):**

| Type | Name | Value |
|------|------|-------|
| CNAME | www | windshop-prod.azurewebsites.net |

**Nếu dùng A record (cho root domain `windshop.vn`):**

1. Trên Azure, **Custom domains** → **Add custom domain** → chọn `windshop.vn`
2. Azure hiển thị **IP addresses** (ví dụ: `20.xxx.xxx.xxx`)
3. Tại DNS provider, thêm:

| Type | Name | Value |
|------|------|-------|
| A | @ | 20.xxx.xxx.xxx |

4. Thêm CNAME để verify (Azure sẽ hướng dẫn chi tiết)

### Bước 6.3: Bật SSL (HTTPS)

1. **Custom domains** → chọn domain đã thêm
2. **Add binding** → chọn **SNI SSL**
3. Chọn **App Service Managed Certificate** (miễn phí, tự gia hạn)
4. **Validate** → **Add**

Sau khi DNS propagate (5–30 phút), truy cập `https://www.windshop.vn` sẽ dùng HTTPS.

---

## Phần 7: Kiểm tra và vận hành

### 7.1. Kiểm tra sau deploy

- [ ] Trang chủ load được
- [ ] Đăng nhập / đăng ký hoạt động
- [ ] Danh sách sản phẩm hiển thị
- [ ] Thanh toán PayOS (test mode nếu có)
- [ ] Gửi mail (quên mật khẩu, xác nhận đơn, v.v.)

### 7.2. Lưu ý về ảnh sản phẩm

Hiện tại ảnh lưu tại `wwwroot/media/products`. Trên App Service:

- **Filesystem không persistent**: Khi app restart hoặc scale out, ảnh có thể mất
- **Khuyến nghị**: Chuyển sang **Azure Blob Storage** cho ảnh sản phẩm (phase 2)

Để tạm thời ổn định hơn, có thể bật **Always On** và tránh scale out nhiều instance cho đến khi chuyển sang Blob Storage.

### 7.3. Bật Always On (tránh cold start)

```bash
az webapp config set \
  --name windshop-prod \
  --resource-group rg-windshop-prod \
  --always-on true
```

### 7.4. Xem log

- **Log stream**: App Service → **Log stream**
- **Application Insights**: Bật để theo dõi performance, lỗi (khuyến nghị)

---

## Phần 8: Bảo mật và best practices

1. **Không commit** `appsettings.json` có chứa connection string, PayOS key, mail password
2. Dùng **Azure Key Vault** cho secret nhạy cảm (nâng cao)
3. **appsettings.Production.json** không nên chứa secret thật; dùng Azure App Settings
4. Bật **HTTPS Only** trong App Service
5. Cập nhật **AllowedHosts** trong `appsettings.Production.json`: thay `yourdomain.vn` bằng tên miền thật (ví dụ: `windshop.vn;www.windshop.vn`)

---

## Checklist tổng hợp

- [ ] Tạo Resource Group
- [ ] Tạo Azure SQL Server + Database
- [ ] Mở firewall cho Azure services
- [ ] Tạo App Service Plan + Web App
- [ ] Cấu hình Connection String `ConnectedDB`
- [ ] Cấu hình PayOS, MailSettings qua App Settings
- [ ] Chạy `dotnet ef database update` với connection Azure
- [ ] Publish và deploy code
- [ ] Thêm custom domain
- [ ] Cấu hình DNS (CNAME hoặc A record)
- [ ] Bật SSL certificate
- [ ] Bật Always On
- [ ] Kiểm tra toàn bộ luồng chính

---

## Tham khảo

- [Deploy ASP.NET Core to Azure App Service](https://learn.microsoft.com/en-us/aspnet/core/host-and-deploy/azure-apps/)
- [Map custom domain to App Service](https://learn.microsoft.com/en-us/azure/app-service/app-service-web-tutorial-custom-domain)
- [Configure connection strings](https://learn.microsoft.com/en-us/azure/app-service/configure-common?tabs=portal#configure-connection-strings)
