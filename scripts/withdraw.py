import os
import sys
import asyncio
import random
from web3 import Web3
from eth_account import Account
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Border width
BORDER_WIDTH = 80

# Constants
RPC_URL_SEPOLIA = "https://ethereum-sepolia-rpc.publicnode.com"  
RPC_URL_T1 = "https://rpc.v006.t1protocol.com"
CHAIN_ID_SEPOLIA = 11155111
CHAIN_ID_T1 = 299792
ROUTER_T1 = Web3.to_checksum_address("0x627B3692969b7330b8Faed2A8836A41EB4aC1918")
EXPLORER_URL_T1 = "https://explorer.v006.t1protocol.com/tx/0x"

BRIDGE_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "_to", "type": "address"},
            {"internalType": "uint256", "name": "_value", "type": "uint256"},
            {"internalType": "bytes", "name": "_message", "type": "bytes"},
            {"internalType": "uint256", "name": "_gasLimit", "type": "uint256"},
            {"internalType": "uint64", "name": "_destChainId", "type": "uint64"},
            {"internalType": "address", "name": "_callbackAddress", "type": "address"}
        ],
        "name": "sendMessage",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    }
]

# Bilingual vocabulary
LANG = {
    'vi': {
        'title': 'RÚT ETH - T1 DEVNET → SEPOLIA',
        'info': 'Thông tin',
        'found': 'Tìm thấy',
        'wallets': 'ví',
        'processing_wallet': 'ĐANG XỬ LÝ VÍ',
        'checking_balance': 'Đang kiểm tra số dư...',
        'insufficient_balance': 'Số dư không đủ',
        'preparing_bridge': 'Đang chuẩn bị rút...',
        'sending_bridge': 'Đang thực hiện rút...',
        'success': 'Rút thành công: {amount:.6f} ETH',
        'failure': 'Rút thất bại',
        'address': 'Địa chỉ',
        'amount': 'Số lượng',
        'gas': 'Gas',
        'block': 'Khối',
        'balance': 'Số dư',
        'pausing': 'Tạm dừng',
        'seconds': 'giây',
        'completed': 'HOÀN THÀNH: {successful}/{total} GIAO DỊCH THÀNH CÔNG',
        'error': 'Lỗi',
        'connect_success': 'Thành công: Đã kết nối với T1 Devnet',
        'connect_error': 'Không thể kết nối với RPC',
        'web3_error': 'Kết nối Web3 thất bại',
        'pvkey_not_found': 'Không tìm thấy tệp pvkey.txt',
        'pvkey_empty': 'Không tìm thấy khóa riêng hợp lệ',
        'pvkey_error': 'Không thể đọc pvkey.txt',
        'invalid_key': 'không hợp lệ, đã bỏ qua',
        'warning_line': 'Cảnh báo: Dòng',
        'amount_prompt': 'Nhập số lượng ETH để rút',
        'invalid_amount': 'Số lượng không hợp lệ, vui lòng nhập số lớn hơn 0',
        'times_prompt': 'Nhập số lần rút',
        'invalid_times': 'Số không hợp lệ, vui lòng nhập số nguyên dương',
    },
    'en': {
        'title': 'WITHDRAW ETH - T1 DEVNET → SEPOLIA',
        'info': 'Info',
        'found': 'Found',
        'wallets': 'wallets',
        'processing_wallet': 'PROCESSING WALLET',
        'checking_balance': 'Checking balance...',
        'insufficient_balance': 'Insufficient balance',
        'preparing_bridge': 'Preparing withdrawal...',
        'sending_bridge': 'Sending withdrawal...',
        'success': 'Withdrawal successful: {amount:.6f} ETH',
        'failure': 'Withdrawal failed',
        'address': 'Address',
        'amount': 'Amount',
        'gas': 'Gas',
        'block': 'Block',
        'balance': 'Balance',
        'pausing': 'Pausing',
        'seconds': 'seconds',
        'completed': 'COMPLETED: {successful}/{total} TRANSACTIONS SUCCESSFUL',
        'error': 'Error',
        'connect_success': 'Success: Connected to T1 Devnet',
        'connect_error': 'Failed to connect to RPC',
        'web3_error': 'Web3 connection failed',
        'pvkey_not_found': 'pvkey.txt file not found',
        'pvkey_empty': 'No valid private keys found',
        'pvkey_error': 'Failed to read pvkey.txt',
        'invalid_key': 'is invalid, skipped',
        'warning_line': 'Warning: Line',
        'amount_prompt': 'Enter ETH amount to withdraw',
        'invalid_amount': 'Invalid amount, please enter a number greater than 0',
        'times_prompt': 'Enter number of withdrawals',
        'invalid_times': 'Invalid number, please enter a positive integer',
    }
}

# Display functions
def print_border(text: str, color=Fore.CYAN, width=BORDER_WIDTH):
    text = text.strip()
    if len(text) > width - 4:
        text = text[:width - 7] + "..."
    padded_text = f" {text} ".center(width - 2)
    print(f"{color}┌{'─' * (width - 2)}┐{Style.RESET_ALL}")
    print(f"{color}│{padded_text}│{Style.RESET_ALL}")
    print(f"{color}└{'─' * (width - 2)}┘{Style.RESET_ALL}")

def print_separator(color=Fore.MAGENTA):
    print(f"{color}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")

# Utility functions
def is_valid_private_key(key: str) -> bool:
    key = key.strip()
    if not key.startswith('0x'):
        key = '0x' + key
    try:
        bytes.fromhex(key.replace('0x', ''))
        return len(key) == 66
    except ValueError:
        return False

def load_private_keys(file_path: str = "pvkey.txt", language: str = 'en') -> list:
    try:
        if not os.path.exists(file_path):
            print(f"{Fore.RED}  ✖ {LANG[language]['pvkey_not_found']}{Style.RESET_ALL}")
            with open(file_path, 'w') as f:
                f.write("# Add private keys here, one per line\n# Example: 0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef\n")
            sys.exit(1)
        
        valid_keys = []
        with open(file_path, 'r') as f:
            for i, line in enumerate(f, 1):
                key = line.strip()
                if key and not key.startswith('#'):
                    if is_valid_private_key(key):
                        if not key.startswith('0x'):
                            key = '0x' + key
                        valid_keys.append((i, key))
                    else:
                        print(f"{Fore.YELLOW}  ⚠ {LANG[language]['warning_line']} {i} {LANG[language]['invalid_key']}: {key}{Style.RESET_ALL}")
        
        if not valid_keys:
            print(f"{Fore.RED}  ✖ {LANG[language]['pvkey_empty']}{Style.RESET_ALL}")
            sys.exit(1)
        
        return valid_keys
    except Exception as e:
        print(f"{Fore.RED}  ✖ {LANG[language]['pvkey_error']}: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

def connect_web3(rpc_url: str, language: str = 'en'):
    try:
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        if not w3.is_connected():
            print(f"{Fore.RED}  ✖ {LANG[language]['connect_error']}{Style.RESET_ALL}")
            sys.exit(1)
        print(f"{Fore.GREEN}  ✔ {LANG[language]['connect_success']} │ Chain ID: {w3.eth.chain_id}{Style.RESET_ALL}")
        return w3
    except Exception as e:
        print(f"{Fore.RED}  ✖ {LANG[language]['web3_error']}: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

def check_balance(w3: Web3, address: str, language: str = 'en') -> float:
    try:
        balance = w3.eth.get_balance(address)
        return float(w3.from_wei(balance, 'ether'))
    except Exception as e:
        print(f"{Fore.YELLOW}  ⚠ {LANG[language]['error']}: {str(e)}{Style.RESET_ALL}")
        return -1

def display_balances(w3_sepolia: Web3, w3_t1: Web3, address: str, language: str = 'en'):
    print_border(f"{LANG[language]['balance']}", Fore.CYAN)
    sepolia_balance = check_balance(w3_sepolia, address, language)
    t1_balance = check_balance(w3_t1, address, language)
    print(f"{Fore.YELLOW}  - Sepolia ETH: {sepolia_balance:.6f}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}  - T1 ETH: {t1_balance:.6f}{Style.RESET_ALL}")

async def withdraw(w3: Web3, private_key: str, wallet_index: int, amount: int, withdraw_times: int, language: str = 'en'):
    account = Account.from_key(private_key)
    sender_address = account.address
    contract = w3.eth.contract(address=ROUTER_T1, abi=BRIDGE_ABI)
    successful_withdrawals = 0
    nonce = w3.eth.get_transaction_count(sender_address, 'pending')

    for i in range(withdraw_times):
        print_border(f"Withdrawal {i+1}/{withdraw_times}: {amount / 10**18:.6f} ETH", Fore.YELLOW)
        print(f"{Fore.CYAN}  > {LANG[language]['checking_balance']}{Style.RESET_ALL}")

        eth_balance = float(w3.from_wei(w3.eth.get_balance(sender_address), 'ether'))
        if eth_balance < amount / 10**18:
            print(f"{Fore.RED}  ✖ {LANG[language]['insufficient_balance']}: {eth_balance:.6f} ETH{Style.RESET_ALL}")
            break

        print(f"{Fore.CYAN}  > {LANG[language]['preparing_bridge']}{Style.RESET_ALL}")
        gas_price = int(w3.eth.gas_price * random.uniform(1.03, 1.1))

        try:
            tx_params = contract.functions.sendMessage(
                sender_address,
                amount,
                b"",
                0,
                CHAIN_ID_SEPOLIA,
                sender_address
            ).build_transaction({
                'nonce': nonce,
                'from': sender_address,
                'value': amount,
                'chainId': CHAIN_ID_T1,
                'gasPrice': gas_price,
                'gas': 500000
            })

            print(f"{Fore.CYAN}  > {LANG[language]['sending_bridge']}{Style.RESET_ALL}")
            signed_tx = w3.eth.account.sign_transaction(tx_params, private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            tx_link = f"{EXPLORER_URL_T1}{tx_hash.hex()}"

            receipt = await asyncio.get_event_loop().run_in_executor(None, lambda: w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180))

            if receipt.status == 1:
                successful_withdrawals += 1
                eth_balance_after = float(w3.from_wei(w3.eth.get_balance(sender_address), 'ether'))
                print(f"{Fore.GREEN}  ✔ {LANG[language]['success'].format(amount=amount/10**18)} │ Tx: {tx_link}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}    {LANG[language]['address']:<12}: {sender_address}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}    {LANG[language]['block']:<12}: {receipt['blockNumber']}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}    {LANG[language]['gas']:<12}: {receipt['gasUsed']}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}    {LANG[language]['balance']:<12}: {eth_balance_after:.6f} ETH{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}  ✖ {LANG[language]['failure']} │ Tx: {tx_link}{Style.RESET_ALL}")
                break

            nonce += 1
            if i < withdraw_times - 1:
                delay = random.uniform(5, 15)
                print(f"{Fore.YELLOW}    {LANG[language]['pausing']} {delay:.2f} {LANG[language]['seconds']}{Style.RESET_ALL}")
                await asyncio.sleep(delay)
        except Exception as e:
            print(f"{Fore.RED}  ✖ {LANG[language]['failure']}: {str(e)}{Style.RESET_ALL}")
            break

    return successful_withdrawals

async def run_withdraw(language: str = 'en'):
    print()
    print_border(LANG[language]['title'], Fore.CYAN)
    print()

    private_keys = load_private_keys('pvkey.txt', language)
    print(f"{Fore.YELLOW}  ℹ {LANG[language]['info']}: {LANG[language]['found']} {len(private_keys)} {LANG[language]['wallets']}{Style.RESET_ALL}")
    print()

    if not private_keys:
        return

    w3_sepolia = connect_web3(RPC_URL_SEPOLIA, language)
    w3_t1 = connect_web3(RPC_URL_T1, language)
    print()

    total_withdrawals = 0
    successful_withdrawals = 0

    random.shuffle(private_keys)
    for i, (profile_num, private_key) in enumerate(private_keys, 1):
        print_border(f"{LANG[language]['processing_wallet']} {profile_num} ({i}/{len(private_keys)})", Fore.MAGENTA)
        account = Account.from_key(private_key)
        print(f"{Fore.YELLOW}  {LANG[language]['address']}: {account.address}{Style.RESET_ALL}")
        display_balances(w3_sepolia, w3_t1, account.address, language)
        print_separator()

        t1_balance = check_balance(w3_t1, account.address, language)
        print()
        while True:
            print(f"{Fore.CYAN}{LANG[language]['amount_prompt']} {Fore.YELLOW}(Max: {t1_balance:.4f} ETH){Style.RESET_ALL}")
            try:
                amount_input = float(input(f"{Fore.GREEN}  > {Style.RESET_ALL}"))
                if amount_input > 0 and amount_input <= t1_balance:
                    amount = int(amount_input * 10**18)
                    break
                print(f"{Fore.RED}  ✖ {LANG[language]['invalid_amount']} or exceeds balance{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}  ✖ {LANG[language]['invalid_amount']}{Style.RESET_ALL}")

        print()
        while True:
            print(f"{Fore.CYAN}{LANG[language]['times_prompt']}:{Style.RESET_ALL}")
            try:
                withdraw_times = int(input(f"{Fore.GREEN}  > {Style.RESET_ALL}"))
                if withdraw_times > 0:
                    break
                print(f"{Fore.RED}  ✖ {LANG[language]['invalid_times']}{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}  ✖ {LANG[language]['invalid_times']}{Style.RESET_ALL}")

        print()
        withdrawals = await withdraw(w3_t1, private_key, profile_num, amount, withdraw_times, language)
        successful_withdrawals += withdrawals
        total_withdrawals += withdraw_times

        if i < len(private_keys):
            delay = random.uniform(10, 30)
            print(f"{Fore.YELLOW}  ℹ {LANG[language]['pausing']} {delay:.2f} {LANG[language]['seconds']}{Style.RESET_ALL}")
            await asyncio.sleep(delay)
        print_separator()

    print()
    print_border(f"{LANG[language]['completed'].format(successful=successful_withdrawals, total=total_withdrawals)}", Fore.GREEN)
    print()

if __name__ == "__main__":
    asyncio.run(run_withdraw('en'))
