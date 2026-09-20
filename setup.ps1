# setup.ps1 - Automatic ERPNext Team Member Setup Script

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "🚀 DANG HOAN TAT THIET LAP LING IELTS ERP..." -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# 1. Start Docker Containers
Write-Host "[1/6] Khởi động Docker containers..." -ForegroundColor Yellow
docker compose -f pwd.yml up -d

# 2. Register Custom App
Write-Host "[2/6] Liên kết ứng dụng ling_ielts_erp..." -ForegroundColor Yellow
docker compose -f pwd.yml exec backend /home/frappe/frappe-bench/env/bin/pip install -e /home/frappe/frappe-bench/apps/ling_ielts_erp

# 3. Check and restore database backup if file exists
$backupFile = Get-ChildItem -Path . -Filter "*.sql.gz" | Select-Object -First 1

if ($backupFile) {
    Write-Host "[3/6] Phát hiện file backup ($($backupFile.Name)), tiến hành restore CSDL..." -ForegroundColor Yellow
    docker compose -f pwd.yml cp "./$($backupFile.Name)" backend:/home/frappe/frappe-bench/sites/frontend/private/backups/
    docker compose -f pwd.yml exec backend bench --site frontend --force restore "/home/frappe/frappe-bench/sites/frontend/private/backups/$($backupFile.Name)" --mariadb-root-password admin
} else {
    Write-Host "[3/6] Bỏ qua restore (không thấy file .sql.gz)" -ForegroundColor Gray
}

# 4. Fix MariaDB User Permissions & Config
Write-Host "[4/6] Cấu hình quyền CSDL MariaDB..." -ForegroundColor Yellow
docker compose -f pwd.yml exec db mariadb -u root -padmin -e "ALTER USER '_5e5899d8398b5f7b'@'%' IDENTIFIED BY 'admin'; GRANT ALL PRIVILEGES ON *.* TO '_5e5899d8398b5f7b'@'%'; FLUSH PRIVILEGES;" 2>$null
docker compose -f pwd.yml exec backend bench --site frontend set-config db_password admin 2>$null

# 5. Migrate & Restart Services
Write-Host "[5/6] Đồng bộ hệ thống (Migrate)..." -ForegroundColor Yellow
docker compose -f pwd.yml exec backend bench --site frontend migrate

Write-Host "[6/6] Khởi động lại các dịch vụ..." -ForegroundColor Yellow
docker compose -f pwd.yml restart backend frontend

Write-Host "==================================================" -ForegroundColor Green
Write-Host "🎉 THÀNH CÔNG! ĐÃ HOÀN TẤT THIẾT LẬP!" -ForegroundColor Green
Write-Host "👉 Truy cập web: http://localhost:8080" -ForegroundColor Green
Write-Host "👉 Tài khoản: Administrator / Mật khẩu: admin" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
