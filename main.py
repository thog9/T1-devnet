import os
import sys
import asyncio
from colorama import init, Fore, Style
import inquirer

# Khởi tạo colorama
init(autoreset=True)

# Độ rộng viền cố định
BORDER_WIDTH = 80

# Hàm hiển thị viền đẹp mắt
def print_border(text: str, color=Fore.CYAN, width=BORDER_WIDTH):
    text = text.strip()
    if len(text) > width - 4:
        text = text[:width - 7] + "..."  # Cắt dài và thêm "..."
    padded_text = f" {text} ".center(width - 2)
    print(f"{color}┌{'─' * (width - 2)}┐{Style.RESET_ALL}")
    print(f"{color}│{padded_text}│{Style.RESET_ALL}")
    print(f"{color}└{'─' * (width - 2)}┘{Style.RESET_ALL}")

# Hàm hiển thị banner
def _banner():
    banner = r"""


████████╗░░███╗░░  ████████╗███████╗░██████╗████████╗███╗░░██╗███████╗████████╗
╚══██╔══╝░████║░░  ╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝████╗░██║██╔════╝╚══██╔══╝
░░░██║░░░██╔██║░░  ░░░██║░░░█████╗░░╚█████╗░░░░██║░░░██╔██╗██║█████╗░░░░░██║░░░
░░░██║░░░╚═╝██║░░  ░░░██║░░░██╔══╝░░░╚═══██╗░░░██║░░░██║╚████║██╔══╝░░░░░██║░░░
░░░██║░░░███████╗  ░░░██║░░░███████╗██████╔╝░░░██║░░░██║░╚███║███████╗░░░██║░░░
░░░╚═╝░░░╚══════╝  ░░░╚═╝░░░╚══════╝╚═════╝░░░░╚═╝░░░╚═╝░░╚══╝╚══════╝░░░╚═╝░░░


    """
    print(f"{Fore.GREEN}{banner:^80}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
    print_border("T1 TESTNET", Fore.GREEN)
    print(f"{Fore.YELLOW}│ {'Liên hệ / Contact'}: {Fore.CYAN}https://t.me/thog099{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}│ {'Discord'}: {Fore.CYAN}https://discord.gg/MnmYBKfHQf{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}│ {'Channel Telegram'}: {Fore.CYAN}https://t.me/thogairdrops{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")

# Hàm xóa màn hình
def _clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Các hàm giả lập cho các lệnh mới
async def run_wraparb(language: str):
    from scripts.wraparb import run_wraparb as wraparb_run
    await wraparb_run(language)

async def run_wrapbase(language: str):
    from scripts.wrapbase import run_wrapbase as wrapbase_run
    await wrapbase_run(language)

async def run_bridgearbtobase(language: str):
    from scripts.bridgearbtobase import run_bridgearbtobase as bridgearbtobase_run
    await bridgearbtobase_run(language)

async def run_bridgebasetoarb(language: str):
    from scripts.bridgebasetoarb import run_bridgebasetoarb as bridgebasetoarb_run
    await bridgebasetoarb_run(language)

async def run_bridgewarbtowbase(language: str):
    from scripts.bridgewarbtowbase import run_bridgewarbtowbase as bridgewarbtowbase_run
    await bridgewarbtowbase_run(language)

async def run_bridgewbasetowarb(language: str):
    from scripts.bridgewbasetowarb import run_bridgewbasetowarb as bridgewbasetowarb_run
    await bridgewbasetowarb_run(language)
    
async def cmd_exit(language: str):
    messages = {"vi": "Đang thoát...", "en": "Exiting..."}
    print_border(messages[language], Fore.GREEN)
    sys.exit(0)

# Danh sách lệnh menu
SCRIPT_MAP = {
    "wraparb": run_wraparb,
    "wrapbase": run_wrapbase,
    "bridgearbtobase": run_bridgearbtobase,
    "bridgebasetoarb": run_bridgebasetoarb,
    "bridgewarbtowbase": run_bridgewarbtowbase,
    "bridgewbasetowarb": run_bridgewbasetowarb,
    "exit": cmd_exit
}


# Danh sách script và thông báo theo ngôn ngữ
def get_available_scripts(language):
    scripts = {
        'vi': [
            {"name": "1. Wrap/Unwrap [ ETH → WETH ] → Arbitrum Sepolia  | T1 Testnet", "value": "wraparb", "locked": True},
            {"name": "2. Wrap/Unwrap [ ETH → WETH ] → Base Sepolia  | T1 Testnet", "value": "wrapbase", "locked": True},
            {"name": "3. Bridge ETH từ Arbitrum Sepolia → Base Sepolia | T1 Testnet", "value": "bridgearbtobase", "locked": True},
            {"name": "4. Bridge ETH từ Base Sepolia → Arbitrum Sepolia | T1 Testnet", "value": "bridgebasetoarb", "locked": True},
            {"name": "5. Bridge WETH từ Arbitrum Sepolia → Base Sepolia | T1 Testnet", "value": "bridgewarbtowbase", "locked": True},
            {"name": "6. Bridge WETH từ Base Sepolia → Arbitrum Sepolia | T1 Testnet", "value": "bridgewbasetowarb", "locked": True},

            {"name": "7. Thoát", "value": "exit"},
        ],
        'en': [
            {"name": "1. Wrap/Unwrap [ ETH → WETH ] → Arbitrum Sepolia  | T1 Testnet", "value": "wraparb", "locked": True},
            {"name": "2. Wrap/Unwrap [ ETH → WETH ] → Base Sepolia  | T1 Testnet", "value": "wrapbase", "locked": True},
            {"name": "3. Bridge ETH từ Arbitrum Sepolia → Base Sepolia | T1 Testnet", "value": "bridgearbtobase", "locked": True},
            {"name": "4. Bridge ETH từ Base Sepolia → Arbitrum Sepolia | T1 Testnet", "value": "bridgebasetoarb", "locked": True},
            {"name": "5. Bridge WETH từ Arbitrum Sepolia → Base Sepolia | T1 Testnet", "value": "bridgewarbtowbase", "locked": True},
            {"name": "6. Bridge WETH từ Base Sepolia → Arbitrum Sepolia | T1 Testnet", "value": "bridgewbasetowarb", "locked": True},
            
            {"name": "7. Thoát", "value": "exit"},
        ]
    }
    return scripts[language]

def run_script(script_func, language):
    """Chạy script bất kể nó là async hay không."""
    if asyncio.iscoroutinefunction(script_func):
        asyncio.run(script_func(language))
    else:
        script_func(language)

def select_language():
    while True:
        _clear()
        _banner()
        print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
        print_border("CHỌN NGÔN NGỮ / SELECT LANGUAGE", Fore.YELLOW)
        questions = [
            inquirer.List('language',
                          message=f"{Fore.CYAN}Vui lòng chọn / Please select:{Style.RESET_ALL}",
                          choices=[("1. Tiếng Việt", 'vi'), ("2. English", 'en')],
                          carousel=True)
        ]
        answer = inquirer.prompt(questions)
        if answer and answer['language'] in ['vi', 'en']:
            return answer['language']
        print(f"{Fore.RED}❌ {'Lựa chọn không hợp lệ / Invalid choice':^76}{Style.RESET_ALL}")

def main():
    _clear()
    _banner()
    language = select_language()

    messages = {
        "vi": {
            "running": "Đang thực thi: {}",
            "completed": "Đã hoàn thành: {}",
            "error": "Lỗi: {}",
            "press_enter": "Nhấn Enter để tiếp tục...",
            "menu_title": "MENU CHÍNH",
            "select_script": "Chọn script để chạy",
            "locked": "🔒 Script này bị khóa! Vui lòng vào group hoặc donate để mở khóa."
        },
        "en": {
            "running": "Running: {}",
            "completed": "Completed: {}",
            "error": "Error: {}",
            "press_enter": "Press Enter to continue...",
            "menu_title": "MAIN MENU",
            "select_script": "Select script to run",
            "locked": "🔒 This script is locked! Please join our group or donate to unlock."
        }
    }

    while True:
        _clear()
        _banner()
        print(f"{Fore.YELLOW}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
        print_border(messages[language]["menu_title"], Fore.YELLOW)
        print(f"{Fore.CYAN}│ {messages[language]['select_script'].center(BORDER_WIDTH - 4)} │{Style.RESET_ALL}")

        available_scripts = get_available_scripts(language)
        questions = [
            inquirer.List('script',
                          message=f"{Fore.CYAN}{messages[language]['select_script']}{Style.RESET_ALL}",
                          choices=[script["name"] for script in available_scripts],
                          carousel=True)
        ]
        answers = inquirer.prompt(questions)
        if not answers:
            continue

        selected_script_name = answers['script']
        selected_script = next(script for script in available_scripts if script["name"] == selected_script_name)
        selected_script_value = selected_script["value"]

        if selected_script.get("locked"):
            _clear()
            _banner()
            print_border("SCRIPT BỊ KHÓA / LOCKED", Fore.RED)
            print(f"{Fore.YELLOW}{messages[language]['locked']}")
            print('')
            print(f"{Fore.CYAN}→ Telegram: https://t.me/thogairdrops")
            print(f"{Fore.CYAN}→ Donate: https://buymecafe.vercel.app{Style.RESET_ALL}")
            print('')
            input(f"{Fore.YELLOW}⏎ {messages[language]['press_enter']}{Style.RESET_ALL:^76}")
            continue

        script_func = SCRIPT_MAP.get(selected_script_value)
        if script_func is None:
            print(f"{Fore.RED}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
            print_border(f"{'Chưa triển khai / Not implemented'}: {selected_script_name}", Fore.RED)
            input(f"{Fore.YELLOW}⏎ {messages[language]['press_enter']}{Style.RESET_ALL:^76}")
            continue

        try:
            print(f"{Fore.CYAN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
            print_border(messages[language]["running"].format(selected_script_name), Fore.CYAN)
            run_script(script_func, language)
            print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
            print_border(messages[language]["completed"].format(selected_script_name), Fore.GREEN)
            input(f"{Fore.YELLOW}⏎ {messages[language]['press_enter']}{Style.RESET_ALL:^76}")
        except Exception as e:
            print(f"{Fore.RED}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
            print_border(messages[language]["error"].format(str(e)), Fore.RED)
            print('')
            input(f"{Fore.YELLOW}⏎ {messages[language]['press_enter']}{Style.RESET_ALL:^76}")

if __name__ == "__main__":
    main()
