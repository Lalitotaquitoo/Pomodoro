import flet as ft
import asyncio
from playsound import playsound
import pygame

def main(page: ft.Page):
    page.title = "Pomodoro Timer"
    page.window.width = 500
    page.window.height = 760
    page.window.resizable = False

    # Inicializar mixer de pygame
    pygame.mixer.init()
    
    # Variables de estado para la música y el contador
    music_paused = False
    timer_paused = False

    # --- Botón de muteo (ya compuesto) ---
    # Definir la función toggle_mute antes de crear el botón
    def toggle_mute(e):
        nonlocal music_paused, mute_button
        if pygame.mixer.music.get_pos() > 0:  # Verifica si hay música en curso
            if music_paused:
                pygame.mixer.music.unpause()
                mute_button.icon = ft.icons.VOLUME_UP
                music_paused = False
            else:
                pygame.mixer.music.pause()
                mute_button.icon = ft.icons.VOLUME_OFF
                music_paused = True 
            page.update()

    # Crear el botón de mute y asignar la función toggle_mute
    mute_button = ft.IconButton(
        icon=ft.icons.VOLUME_UP, 
        icon_color=ft.colors.WHITE, 
        bgcolor=ft.colors.BLUE_GREY,
        on_click=toggle_mute
    )
    
    # --- Botón para pausar el contador ---
    # Definir la función para pausar/reanudar el contador
    def toggle_timer_pause(e):
        nonlocal timer_paused, pause_timer_button
        if timer_paused:
            timer_paused = False
            pause_timer_button.icon = ft.icons.PAUSE  # Icono de pausa cuando está corriendo
        else:
            timer_paused = True
            pause_timer_button.icon = ft.icons.PLAY_ARROW  # Icono de play cuando está en pausa
        page.update()
    
    # Crear el botón de pausa del contador
    pause_timer_button = ft.IconButton(
        icon=ft.icons.PAUSE,
        icon_color=ft.colors.WHITE,
        bgcolor=ft.colors.BLUE,
        on_click=toggle_timer_pause
    )
    
    page.fonts = {
        "Press Start 2P": "https://github.com/google/fonts/raw/main/ofl/pressstart2p/PressStart2P-Regular.ttf"
    }
    page.theme = ft.Theme(font_family="Press Start 2P")

    # Componente de texto para el temporizador
    timer_text = ft.Text(
        "25:00",
        size=50,
        color=ft.colors.WHITE,
        font_family="Press Start 2P",
        text_align=ft.TextAlign.CENTER
    )

    timer_text_container = ft.Container(
        content=ft.Container(
            content=timer_text,
            padding=20,
            border_radius=10,
            bgcolor=ft.colors.BLUE_GREY
        ),
        padding=2,
        border_radius=12,
        bgcolor=ft.colors.WHITE
    )

    task_list = ft.Column(scroll=ft.ScrollMode.AUTO)
    tasks = []

    task_input = ft.TextField(
        hint_text="Agregar tarea...",
        width=250,
        bgcolor=ft.colors.with_opacity(0.7, ft.colors.WHITE),
        color=ft.colors.BLACK,
        hint_style=ft.TextStyle(color=ft.colors.BLACK54),
        text_align=ft.TextAlign.CENTER
    )

    task_input_container = ft.Container(
        content=ft.Container(
            content=task_input,
            padding=10,
            border_radius=8,
            bgcolor=ft.colors.WHITE,
        ),
        padding=2,
        border_radius=10,
        bgcolor=ft.colors.BLACK
    )

    def add_task(e):
        if task_input.value:
            task = ft.Checkbox(label=task_input.value)
            tasks.append(task)
            task_list.controls.append(task)
            task_input.value = ""
            page.update()

    async def start_timer():
        if not tasks:
            await countdown(25, 0, "Trabajo")
            await countdown(5, 0, "Descanso")
        else:
            while tasks:
                await countdown(25, 0, "Trabajo")  # 25 minutos de trabajo
                if tasks:
                    tasks.pop(0)
                    task_list.controls.pop(0)
                    page.update()
                await countdown(5, 0, "Descanso")   # 5 minutos de descanso

    async def countdown(minutes, seconds, mode):
        nonlocal music_paused, timer_paused
        
        if mode == "Trabajo":
            # Cargar y reproducir música de fondo en bucle
            pygame.mixer.music.load("C:/Users/52961/Desktop/Pomodoro/src/background_music.mp3")  # Cambia la ruta
            pygame.mixer.music.play(-1)  # -1 para reproducir en bucle
            mute_button.icon = ft.icons.VOLUME_UP
            music_paused = False
        
        while minutes >= 0:
            timer_text.value = f"{mode}: {minutes:02}:{seconds:02}"
            page.update()
            
            # Esperar mientras el contador esté pausado
            while timer_paused:
                await asyncio.sleep(0.1)
            
            await asyncio.sleep(1)
            if seconds == 0:
                if minutes == 0:
                    break
                minutes -= 1
                seconds = 59
            else:
                seconds -= 1

        if mode == "Trabajo":
            pygame.mixer.music.stop()
            await asyncio.to_thread(playsound, "C:/Users/52961/Desktop/Pomodoro/src/work_sound.mp3")
        elif mode == "Descanso":
            await asyncio.to_thread(playsound, "C:/Users/52961/Desktop/Pomodoro/src/break_sound.mp3")

    def go_to_timer(e):
        page.go("/timer")

    def go_back(e):
        page.go("/")

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(
                ft.View(
                    "/",
                    controls=[
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text(
                                        "Pomodoro Timer",
                                        size=40,
                                        color=ft.colors.WHITE,
                                        font_family="Press Start 2P",
                                        text_align=ft.TextAlign.CENTER
                                    ),
                                    ft.ElevatedButton("Entra", on_click=go_to_timer)
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                            width=500,
                            height=700,
                            image_src="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExaW82d21haTkwY3Qyd3hpYWkycnM0bmhvOTlkcml3eW1xN3JncW4xcyZlcD12MV9pbnRlcm5naWZfYnlfaWQmY3Q9Zw/pI43YlhMoPqsE/giphy.gif",
                            image_fit=ft.ImageFit.COVER
                        )
                    ]
                )
            )
        elif page.route == "/timer":
            page.views.append(
                ft.View(
                    "/timer",
                    controls=[
                        ft.Stack(
                            [
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Text(
                                                "Tiempo",
                                                size=30,
                                                color=ft.colors.WHITE,
                                                font_family="Press Start 2P",
                                                text_align=ft.TextAlign.CENTER
                                            ),
                                            timer_text_container,
                                            ft.ElevatedButton("Iniciar", on_click=lambda e: asyncio.run(start_timer())),
                                            ft.Row(
                                                [
                                                    task_input_container,
                                                    ft.ElevatedButton("Agregar", on_click=add_task)
                                                ],
                                                alignment=ft.MainAxisAlignment.CENTER
                                            ),
                                            task_list,
                                            ft.ElevatedButton("Volver", on_click=go_back)
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                    ),
                                    width=500,
                                    height=700,
                                    image_src="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExdjRvYnQ4em1oM2E4eTR0ZDg0d2d5b3JkcHRrcmxjZ2ZpdDdscTNsaiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/1yld7nW3oQ2IyRubUm/giphy.gif",
                                    image_fit=ft.ImageFit.COVER
                                ),
                                # Botón de mute (abajo a la derecha)
                                ft.Container(
                                    content=mute_button,
                                    right=20,
                                    bottom=20,
                                    alignment=ft.alignment.bottom_right
                                ),
                                # Botón para pausar/reanudar el contador (abajo a la izquierda)
                                ft.Container(
                                    content=pause_timer_button,
                                    left=20,
                                    bottom=20,
                                    alignment=ft.alignment.bottom_left
                                )
                            ]
                        )
                    ]
                )
            )
        page.update()

    def on_close(e):
        pygame.mixer.quit()

    page.on_close = on_close
    page.on_route_change = route_change
    page.go("/")
    

ft.app(main)
