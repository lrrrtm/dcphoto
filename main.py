from datetime import datetime

import flet as ft
import os
import shutil
from datetime import datetime


def main(page: ft.Page):
    links = {}
    page.window_width = 750  # window's width is 200 px
    page.window_height = 300  # window's height is 200 px
    page.window_resizable = False  # window is not resizable
    page.title = "Выгрузка фото"
    UPLOAD_PATH = ""
    OUTLOAD_PATH = ""

    def process_1(e: ft.FilePickerResultEvent):
        links['input'] = e.path
        UPLOAD_PATH = e.path
        label_1.value = f"{UPLOAD_PATH}"
        page.update()


    def process_2(e: ft.FilePickerResultEvent):
        links['output'] = e.path
        OUTLOAD_PATH = e.path
        label_2.value = f"{OUTLOAD_PATH}"
        page.update()

    def get_all(e):
        folder_name = str(datetime.now().strftime("%d-%m"))
        if os.path.exists(links['output'] + f"\\{folder_name}"):
            pass
        else:
            os.mkdir(links['output'] + f"\\{folder_name}")
            os.mkdir(links['output'] + f"\\{folder_name}\\photo")
            os.mkdir(links['output'] + f"\\{folder_name}\\video")


        try:
            count_1, count_2 = 0, 0
            for filename in os.listdir(f"{links['input']}\\DCIM\\100MSDCF"):
                if filename.lower().endswith(".jpg"):
                    count_1 += 1

            for filename in os.listdir(f"{links['input']}\\PRIVATE\\M4ROOT\\CLIP"):
                if filename.lower().endswith(".mp4"):
                    count_2 += 1

            all_count = count_1 + count_2
            step = int(100 / all_count)


            for filename in os.listdir(f"{links['input']}\\DCIM\\100MSDCF"):
                if filename.lower().endswith(".jpg"):
                    src_file = os.path.join(f"{links['input']}\\DCIM\\100MSDCF", filename)
                    dst_file = os.path.join(f"{links['output']}\\{folder_name}\\photo\\")
                    shutil.move(src_file, dst_file)
                    progress_bar.value += step
                    page.update()

            for filename in os.listdir(f"{links['input']}\\PRIVATE\\M4ROOT\\CLIP"):
                if filename.lower().endswith(".mp4"):
                    src_file = os.path.join(f"{links['input']}\\PRIVATE\\M4ROOT\\CLIP", filename)
                    dst_file = os.path.join(f"{links['output']}\\{folder_name}\\video")
                    shutil.move(src_file, dst_file)
                    progress_bar.value += step
                    page.update()

            if count_1 == 0 and count_2 == 0:
                page.show_snack_bar(
                    ft.SnackBar(ft.Text(f"Нет файлов для переноса"), open=True)
                )
            else:
                page.show_snack_bar(
                    ft.SnackBar(ft.Text(f"Файлы выгружены (Фото: {count_1}, Видео: {count_2})"), open=True)
                )
        except Exception as e:
            page.show_snack_bar(
                ft.SnackBar(ft.Text(f"Ошибка: {e}"), open=True)
            )
            print(e)



    file_picker_1 = ft.FilePicker(on_result=process_1)
    file_picker_2 = ft.FilePicker(on_result=process_2)
    page.overlay.append(file_picker_1)
    page.overlay.append(file_picker_2)

    label_1 = ft.TextField(label="", read_only=True, width=450)
    label_2 = ft.TextField(label="", read_only=True, width=450)

    row_1 = ft.Row([
        ft.ElevatedButton("Выберите SD", height=50, width=250,
                          on_click=lambda _: file_picker_1.get_directory_path()),
        label_1

    ])

    row_2 = ft.Row([
        ft.ElevatedButton("Выберите папку", height=50, width=250,
                          on_click=lambda _: file_picker_2.get_directory_path()),
        label_2
    ])
    btn_all = ft.ElevatedButton("Выгрузить", height=50, width=750, on_click=get_all, bgcolor="green", color="white")

    progress_bar = ft. ProgressBar(width=750, visible=False)

    page.add(row_1, row_2, btn_all, progress_bar)
    page.update()


ft.app(target=main,
       # view=ft.AppView.WEB_BROWSER
       )
