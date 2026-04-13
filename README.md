
# Phiên bản hệ điều hành 
### Ubuntu 20.04 LTS

# Yêu cầu phần cứng và HĐH trên AWS EC2
### Ubuntu 22.04 LTS
### Instance type: t3.small trở lên

# Hướng dẫn 

## Tải về bằng Git:
```bash
git clone https://github.com/CongTaiGao/S2-2025-2026-University-CloudComputing.git
```

Nếu gặp lỗi permission denied trên localhost

```bash
sudo chmod 755 -R ./S2-2025-2026-University-CloudComputing
```

## DOCKER

### Cài đặt

```bash
sudo apt update
sudo apt install ca-certificates curl gnupg lsb-release -y
```

```bash
sudo mkdir -p /etc/apt/keyrings
```

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```


```bash
echo \
"deb [arch=$(dpkg --print-architecture) \
signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```




```bash
sudo apt update
```

```bash
sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y
```

### Test

```bash
docker compose version
```

### Compose

Docker compose: Vào thư mục chính chứa docker-compose.yml sau đó chạy các lệnh sau:
```bash
docker compose build --no-cache
docker compose up -d 
```

Check trạng thái bằng:
```bash
docker ps 
```

Nếu muốn xóa docker:
```bash
docker rm -f $(docker ps -aq)
```
Lệnh khởi động lại:
```bash
docker compose restart
```
### Troubleshooting

Sử dụng lệnh sau để check log của container
```bash
docker logs <tên container>
```

Nếu có ghi nhận Permission Denied (Thường gặp khi triển khai public trên EC2) thì:
```bash
nano docker-compose.yml

#Tìm đoạn container cần fix và thêm
user: "root"
```


## WEB-FRONTENDED-SERVER

Truy cập trên trình duyệt với URL: localhost

## APPLICATION-BACKEND-SERVER

URL: localhost:8085/student

hoặc

localhost/api/student

## DATABASE-SERVER

URL: localhost:8085/students-db

hoặc

localhost/api/students-db

### LỆNH CHECK TRUY VẤN BẢNG

### DATABASE BASIC
```bash
docker run -it --rm --network cloud-net mysql:8 \
sh -lc 'mysql -h relational-database-server -uroot -proot -e "USE minicloud; SHOW TABLES; SELECT * FROM notes;"'
```

### DATABASE STUDENTDB
```bash
docker run -it --rm --network cloud-net mysql:8 \
sh -lc 'mysql -h relational-database-server -uroot -proot -e "USE studentdb; SHOW TABLES; SELECT * FROM students;"'
```


## KEYCLOAK: AUTHENTICATION-SERVER

Truy cập vào URL: localhost:8081

Username: admin
Mật khẩu: admin

Đối với triển khai trên EC2 cần tìm trong `docker-compose.yml` dòng `KC_HOSTNAME` ở keycloak cần chuyển `localhost` thành ip của instance EC2 hoặc xóa luôn `KC_HOSTNAME`

### CÁCH LẤY TOKEN từ Account KeyCloak với realm N08
```bash
docker run --rm -it --network cloud-net curlimages/curl curl -X POST \
http://authentication-identity-server:8080/realms/realm_N08/protocol/openid-connect/token \
-d "client_id=flask-app" \
-d "username=sv02" \
-d "password=123456" \
-d "grant_type=password" | grep -o '"access_token":"[^"]*"' | cut -d':' -f2 | tr -d '"'
```

### XÁC THỰC TOKEN
```bash
curl http://localhost:8085/secure -H "Authorization: Bearer <Dán token vào đây!>"
```


## MINIO-STORAGE-SERVER

Truy cập vào URL: localhost:9001

Username: minioadmin
Mật khẩu: minioadmin

## DNS-SERVER

Sử dụng lệnh sau 
```bash
dig @127.0.0.1 -p 1053 web-frontend-server.cloud.local +short
dig @127.0.0.1 -p 1053 app-backend.cloud.local +short
dig @127.0.0.1 -p 1053 minio.cloud.local +short
dig @127.0.0.1 -p 1053 keycloak.cloud.local +short
```

Kết quả trả về lần lượt: 10.10.10.10, 10.10.10.20, 10.10.10.30, 10.10.10.40

## PROMETHEUS-MONITORING-SERVER

Truy cập vào URL: localhost:9090

Chọn "Status > Target Health" để check tình trạng UP/DOWN

Thử truy vấn bằng cách gõ "node_cpu_seconds_total" trên thanh sau đó nhấn "Execute"

## GRAFANA-DASHBOARD-SERVER

Truy cập vào URL: localhost:3000

Username: admin
Mật khẩu: admin

Chọn mục "Dashboards" ở sidebar bên trái để xem biểu đồ

Nếu không có biểu đồ nào cả thì có thể import lại dashboard "Exporter Full" với ID `1860`

## NGINX-PROXY-SERVER

Thử truy cập trên trình duyệt với URL: localhost/student 

Dùng curl để thử:
```bash
curl -I http://localhost/
curl -s http://localhost/api/hello
curl -I http://localhost/auth
```


## LOAD-BALANCING-ROUND-ROBIN
Thử truy cập vào trình duyệt tại "localhost" hoặc "curl localhost" nhiều lần

Check log trên gateway:
```bash
docker logs api-gateway-proxy-server
```

Phải trả về IP luân phiên giữa 3 server 
##

#### Author: Cao Thông Thái 
#### Last Updated: 13/04/2026

##

#### THỰC HIỆN
- Cao Thông Thái
- Đặng Lâm Anh Vũ
- Nguyễn Thanh Phú



