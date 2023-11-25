import os
import shutil
import tempfile
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def print_colored_text(text, color='white', style='normal', gradient=False, rgb=None):
    color_codes = {'black': '30', 'red': '31', 'green': '32', 'yellow': '33', 'blue': '34', 'purple': '35', 'cyan': '36', 'white': '37'}
    style_codes = {'normal': '0', 'bold': '1', 'underline': '4', 'blink': '5', 'reverse': '7', 'concealed': '8'}

    if rgb: color_code = f'38;2;{rgb[0]};{rgb[1]};{rgb[2]}'
    else: color_code = color_codes.get(color, '37')

    style_code = style_codes.get(style, '0')

    formatted_text = ''
    step = 255 // len(text)
    for i, char in enumerate(text):
        gradient_color = str(255 - i * step)
        formatted_text += f'\033[{style_code};{color_code};0m{char}\033[0m' if gradient else f'\033[{style_code};{color_code}m{text}\033[0m'

    print(formatted_text)

def delete_temporary_contents():
    temp_dir = tempfile.gettempdir()
    print_colored_text(f"Temporary directory: {temp_dir}", rgb=(124, 165, 243), style="bold", gradient=False)

    deleted_count, total_deleted_size = 0, 0

    for item in os.listdir(temp_dir):
        item_path = os.path.join(temp_dir, item)
        try:
            if os.path.isfile(item_path):
                file_size = os.path.getsize(item_path)
                os.remove(item_path)
                print_colored_text(f"Deleted file: {item_path}", color="green", style="bold", gradient=False)
                deleted_count += 1
                total_deleted_size += file_size
            elif os.path.isdir(item_path):
                dir_size = sum(f.stat().st_size for f in os.scandir(item_path) if f.is_file())
                shutil.rmtree(item_path)
                print_colored_text(f"Deleted directory: {item_path}", rgb=(255, 80, 90), style="bold", gradient=False)
                deleted_count += 1
                total_deleted_size += dir_size
        except Exception as e:
            print_colored_text(f"Failed to delete {item_path}: {e}", rgb=(255, 80, 90), style="bold", gradient=False)

    print_colored_text(f"Deleted {deleted_count} items, Total size: {total_deleted_size / (1024 * 1024):.2f} MB", color="yellow", style="underline", gradient=False)

if __name__ == "__main__":
    if not is_admin():
        print_colored_text("This script needs administrator privileges. Do you want to continue? (y/n): ", color="yellow", style="bold", gradient=False)
        user_input = input().lower()
        if user_input != 'y':
            print_colored_text("Exiting...", color="red", style="bold", gradient=False)
            exit()

    delete_temporary_contents()
