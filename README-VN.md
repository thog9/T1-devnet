# T1 Testnet Scripts

Kho lưu trữ này chứa một bộ sưu tập các tập lệnh Python được thiết kế để tương tác với **T1 Devnet**, một mạng thử nghiệm blockchain để bắc cầu chuỗi chéo. Các tập lệnh này cho phép người dùng bắc cầu ETH giữa Sepolia Testnet và T1 Devnet, tạo điều kiện thuận lợi cho việc gửi tiền (Sepolia → T1) và rút tiền (T1 → Sepolia) bằng cách sử dụng các hợp đồng bộ định tuyến cầu nối T1. Mỗi tập lệnh được xây dựng bằng thư viện `web3.py` và cung cấp hỗ trợ song ngữ (tiếng Anh và tiếng Việt) để người dùng tương tác.

Faucet: [Sepolia Faucet](https://sepoliafaucet.com/)  
Bridge: [T1 Devnet Bridge](https://devnet.t1protocol.com/bridge)

### Tính năng chung

- **Hỗ trợ nhiều tài khoản**: Đọc khóa riêng từ `pvkey.txt` để thực hiện các hành động trên nhiều tài khoản.
- **CLI đầy màu sắc**: Sử dụng `colorama` để có đầu ra hấp dẫn về mặt hình ảnh với văn bản và đường viền có màu.
- **Thực thi không đồng bộ**: Được xây dựng với `asyncio` để tương tác blockchain hiệu quả.
- **Xử lý lỗi**: Bắt lỗi toàn diện cho các giao dịch blockchain và sự cố RPC.
- **Hỗ trợ song ngữ**: Hỗ trợ cả đầu ra tiếng Việt và tiếng Anh dựa trên lựa chọn của người dùng.

### Các tập lệnh được bao gồm

1. **deposit.py**: Cầu nối ETH từ Sepolia Testnet đến T1 Devnet bằng hợp đồng bộ định tuyến cầu nối T1.
2. **withdraw.py**: Cầu nối ETH từ T1 Devnet trở lại Sepolia Testnet bằng hợp đồng bộ định tuyến cầu nối T1.
3. **sendtx.py**: Gửi các giao dịch ETH ngẫu nhiên hoặc đến các địa chỉ từ address.txt trên T1 Testnet.
4. **deploytoken.py**: Triển khai hợp đồng thông minh mã thông báo ERC20 trên T1 Testnet.
5. **sendtoken.py**: Gửi mã thông báo ERC20 đến các địa chỉ ngẫu nhiên hoặc từ addressERC20.txt trên T1 Testnet.
6. **nftcollection.py**: Triển khai và quản lý hợp đồng thông minh NFT (Tạo, Đúc, Đốt) trên T1 Testnet.

## Điều kiện tiên quyết

Trước khi chạy các tập lệnh, hãy đảm bảo bạn đã cài đặt các phần sau:

- Python 3.8 trở lên
- `pip` (trình quản lý gói Python)
- **Phụ thuộc**: Cài đặt qua `pip install -r requirements.txt` (đảm bảo `web3.py`, `colorama`, `asyncio`, `eth-account` và `inquirer` được bao gồm).
- **pvkey.txt**: Thêm khóa riêng (mỗi dòng một khóa) để tự động hóa ví.
- Truy cập vào Sepolia Testnet RPC (ví dụ: `https://ethereum-sepolia-rpc.publicnode.com`).
- Truy cập vào T1 Devnet RPC (`https://rpc.v006.t1protocol.com`).

## Cài đặt

1. **Clone this repository:**
- Mở cmd hoặc Shell, sau đó chạy lệnh:
```sh
git clone https://github.com/thog9/T1-devnet.git
```
```sh
cd T1-devnet
```
2. **Install Dependencies:**
- Mở cmd hoặc Shell, sau đó chạy lệnh:
```sh
pip install -r requirements.txt
```
3. **Prepare Input Files:**
- Mở `pvkey.txt`: Thêm khóa riêng của bạn (mỗi dòng một khóa) vào thư mục gốc.
```sh
nano pvkey.txt
```
- Mở `address.txt`(tùy chọn): Thêm địa chỉ người nhận (mỗi dòng một khóa) cho `sendtx.py`, `deploytoken.py`, `sendtoken.py`,`nftcollection.py` .
```sh
nano address.txt
```
```sh
nano addressERC20.txt
```
```sh
nano contractERC20.txt
```
```sh
nano contractNFT.txt
```
4. **Run:**
- Mở cmd hoặc Shell, sau đó chạy lệnh:
```sh
python main.py
```
- Chọn ngôn ngữ (Tiếng Việt/Tiếng Anh).

## Liên hệ

- **Telegram**: [thog099](https://t.me/thog099)
- **Channel**: [CHANNEL](https://t.me/thogairdrops)
- **Group**: [GROUP CHAT](https://t.me/thogchats)
- **X**: [Thog](https://x.com/thog099) 
