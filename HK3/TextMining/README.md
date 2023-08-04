# Crawler để tìm liên kết GitHub của bài báo

## Hướng dẫn sử dụng:

1. Cài đặt các gói cần thiết bằng cách chạy lệnh sau:
```bash
pip install -r requirements.txt
```

2. Chạy chương trình bằng cách chạy lệnh sau và nhập tên bài báo:
```bash
python find_github.py <Tên bài báo>
```
Lưu ý: Trong mã find_github.py, chúng ta đã sử dụng sys.argv để lấy đối số dòng lệnh (tên bài báo) khi chạy chương trình.

3. Kết quả sẽ xuất ra liên kết GitHub của bài báo nếu có, hoặc thông báo "Không tìm thấy liên kết GitHub trong bài báo" nếu không tìm thấy.
