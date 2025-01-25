"""
信号选择器界面模块
"""

import os
import sys
import shutil
from typing import List, Dict, Tuple

from ..core.signal_manager import SignalManager


def select_signals() -> List[str]:
    """交互式选择信号类型"""
    # 获取终端大小
    try:
        terminal_width = shutil.get_terminal_size().columns
    except:
        terminal_width = 80

    box_width = min(terminal_width - 4, 76)

    signals = SignalManager.get_available_signals()
    selected_signals = []
    all_signals = []
    signal_map = {}

    # 定义颜色代码
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    END = '\033[0m'

    # 清屏
    os.system('cls' if os.name == 'nt' else 'clear')

    # 标题
    title = "OSC 信号选择器 v1.0"
    padding = (box_width - len(title)) // 2
    print(f"\n{BOLD}{BLUE}╔{'═' * box_width}╗{END}")
    print(f"{BOLD}{BLUE}║{' ' * padding}{YELLOW}{title}{END}{' ' * (box_width - padding - len(title))}{BOLD}{BLUE}║{END}")
    print(f"{BOLD}{BLUE}╚{'═' * box_width}╝{END}\n")

    # 计算信号显示宽度
    max_signal_length = max(len(signal) for signal_list in signals.values() for signal in signal_list)
    desc_width = box_width - max_signal_length - 15

    # 显示信号类别和选项
    for category, signal_list in signals.items():
        print(f"{CYAN}┌{'═' * box_width}┐{END}")
        print(f"{CYAN}║{END} {BOLD}{MAGENTA}{category}{' ' * (box_width - len(category) - 2)}{END}{CYAN}║{END}")
        print(f"{CYAN}╟{'─' * box_width}╢{END}")

        for signal in signal_list:
            idx = len(all_signals) + 1
            display_signal = f"/{signal}"
            description = SignalManager.get_signal_description(signal)

            if len(description) > desc_width:
                description = description[:desc_width - 3] + "..."

            line = f"{CYAN}║{END} [{YELLOW}{idx:2d}{END}] {display_signal:<{max_signal_length}} {GREEN}→{END} {description:<{desc_width}}{CYAN}║{END}"
            print(line)

            all_signals.append(signal)
            signal_map[idx] = (category, signal)
        print(f"{CYAN}└{'═' * box_width}┘{END}\n")

    # 操作指南
    print(f"{BOLD}{BLUE}╔{'═' * box_width}╗{END}")
    print(f"{BOLD}{BLUE}║{END}{' ' * ((box_width - 8) // 2)}{YELLOW}操作指南{END}{' ' * ((box_width - 8) // 2)}{BOLD}{BLUE}║{END}")
    print(f"{BOLD}{BLUE}╠{'═' * box_width}╣{END}")

    guides = [
        "• 输入序号选择信号（多个序号用空格分隔）",
        "• 直接回车选择所有信号",
        "• 输入 'q' 退出程序",
        "• 输入 'h' 显示帮助信息"
    ]

    for guide in guides:
        padding = box_width - len(guide) - 2
        print(f"{BOLD}{BLUE}║{END} {guide}{' ' * padding}{BOLD}{BLUE}║{END}")

    print(f"{BOLD}{BLUE}╚{'═' * box_width}╝{END}\n")

    while True:
        try:
            choice = input(f"{BOLD}{CYAN}请选择 >{END} ").strip().lower()

            if choice == 'q':
                print(f"\n{YELLOW}✨ 程序已退出{END}")
                sys.exit(0)
            elif choice == 'h':
                print(f"\n{BOLD}{BLUE}╔══ 帮助信息 ══╗{END}")
                print(f"{CYAN}┃{END} • EEG信号：用于采集脑电数据")
                print(f"{CYAN}┃{END} • 生理信号：包含PPG等生理指标")
                print(f"{CYAN}┃{END} • 运动数据：记录设备运动状态")
                print(f"{BOLD}{BLUE}╚{'═' * 16}╝{END}\n")
                continue
            elif not choice:
                selected_signals = all_signals
                print(f"\n{GREEN}✓ 已选择所有信号{END}")
                break

            try:
                indices = [int(x) for x in choice.split()]
                selected_signals = []
                print(f"\n{BOLD}{BLUE}═══ 已选择信号 ═══{END}")
                for idx in indices:
                    if idx in signal_map:
                        category, signal = signal_map[idx]
                        selected_signals.append(signal)
                        print(f"{GREEN}✓{END} [{category}] {signal}")
                    else:
                        print(f"{YELLOW}✗{END} 序号 {idx} 无效，已忽略")

                if selected_signals:
                    confirm = input(f"\n{BOLD}确认选择吗？(y/n) >{END} ").strip().lower()
                    if confirm == 'y':
                        break
                    else:
                        selected_signals = []
                        print(f"\n{YELLOW}⚠ 已取消选择，请重新选择{END}")
                        continue

            except ValueError:
                print(f"\n{YELLOW}⚠ 输入格式无效，请重新选择{END}")
                continue

        except Exception as e:
            print(f"\n{YELLOW}⚠ 发生错误: {e}{END}")
            print(f"{YELLOW}⚠ 将选择所有信号{END}")
            selected_signals = all_signals
            break

    if not selected_signals:
        print(f"\n{YELLOW}⚠ 未选择任何信号，将选择所有信号{END}")
        selected_signals = all_signals

    print(f"\n{BOLD}{BLUE}╔══ 最终选择 ══╗{END}")
    print(f"{CYAN}┃{END} 共选择了 {GREEN}{len(selected_signals)}{END} 个信号：")
    for signal in selected_signals:
        print(f"{CYAN}┃{END} {GREEN}•{END} {signal}")
    print(f"{BOLD}{BLUE}╚{'═' * 14}╝{END}")
    print(f"\n{BLUE}✨ 正在启动监听...{END}\n")

    return selected_signals 