import random
import time
from playwright.async_api import async_playwright

async def humanize_interaction(page):
    """
    Función para agregar interacciones humanizadas al navegador.
    """
    # Realizar una espera aleatoria entre 1 y 3 segundos
    await page.wait_for_timeout(random.randint(1000, 3000))

    # Desplazar la página hacia abajo para simular el desplazamiento de un usuario
    await page.evaluate("window.scrollBy(0, window.innerHeight);")
    await page.wait_for_timeout(random.randint(2000, 5000))  # Esperar por un tiempo aleatorio

    # Rellenar el input de búsqueda como lo haría un usuario
    anime_name = "Naruto"  # Puedes cambiar el nombre del anime aquí
    for char in anime_name:
        await page.fill('input#buscanime', anime_name[:anime_name.index(char)+1])
        # Esperar un tiempo aleatorio entre las teclas
        await page.wait_for_timeout(random.randint(150, 400))

    # Realizar clic en el primer enlace después de esperar
    await page.wait_for_selector('li.lista-anime a')
    await page.click('li.lista-anime a')

    # Esperar para ver el resultado antes de cerrar el navegador
    await page.wait_for_timeout(random.randint(3000, 6000))

async def my_script(page):
    # Realizamos la humanización en tu script existente
    await page.goto("https://animeflv.net/")

    # Llamamos a la función de interacción humanizada
    await humanize_interaction(page)

    # Esperar la interacción del usuario antes de cerrar el navegador
    input("Presiona Enter para continuar...")  # Mantener la ventana abierta

