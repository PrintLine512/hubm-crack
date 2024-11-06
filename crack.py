import shutil
import subprocess
import sys
import os


def unpack_upx(file_path):
    """Распаковывает исполняемый файл с помощью upx"""
    subprocess.run([ "/app/upx/upx", "-d", file_path ], check=True)


def repack_upx(file_path):
    """Сжимает исполняемый файл с помощью upx"""
    subprocess.run([ "/app/upx/upx", "-9", file_path ], check=True)


def replace_string_in_file(filename, old_str, new_str):
    """Заменяет строку в файле"""
    with open(filename, "rb+") as f:
        content = f.read()
        index = content.find(old_str.encode())

        if index == -1:
            print("Строка не найдена в файле.")
            return False

        # Подгоняем длину строки
        if len(new_str) < len(old_str):
            new_str = new_str.ljust(len(old_str), '\x00')
        elif len(new_str) > len(old_str):
            new_str = new_str[ :len(old_str) ]  # Обрезаем новую строку, если она длиннее

        # Заменяем строку
        f.seek(index)
        f.write(new_str.encode())
        print("Строка заменена успешно.")
    return True


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: crack.py <new_string>")
        sys.exit(1)


    orig_file_path = '/app/file'
    file_path = '/app/out/file'
    new_string = sys.argv[ 1 ]
    old_string = '/sys/class/dmi/id/product_uuid'  # Исправлено

    if not os.path.isfile(orig_file_path):
        print(f"Файл не найден: {file_path}")
        sys.exit(1)
    shutil.copy(orig_file_path, file_path)
    try:
        print("Добавление флага 'исполняемый'...")
        result = subprocess.run([ 'chmod', '+x', file_path ], capture_output=True, text=True)
        if result.returncode != 0:
            print("Ошибка при установке прав на файл:")
            print(result.stderr)
            sys.exit(1)

        print("Распаковка файла с помощью UPX...")
        unpack_upx(file_path)

        print("Замена строки...")
        if not replace_string_in_file(file_path, old_string, new_string):
            print("Замена строки не удалась.")
            sys.exit(1)

        print("Сжатие файла обратно с помощью UPX...")
        repack_upx(file_path)

        print("Обработка завершена успешно.")
        print(f"Создайте файл {new_string} и добавьте в него строку '03d40274-0435-0549-2506-820700080009' без кавычек.\n"
              f"В конфигурации сервера используйте 'License=03d40274-0435-0549-2506-820700080009,0,MCACDhf5Fve1ROuGyx8tA5OlAg4ypJivw6hytRlYUz5arA==' без кавычек.")

    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")
        sys.exit(1)
