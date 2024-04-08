import flet as ft

async def main(page: ft.Page) -> None:

    page.title = "Hello World App"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = '#141221'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    score = ft.Text(value="0", size=100, data=0)

    

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER, port=8000)