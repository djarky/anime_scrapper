import os
from playwright.async_api import async_playwright  # Usamos la API asincrónica
from my_script import my_script  # Importamos la función my_script

def cargar_rutas_de_extensiones(base_path="extensiones"):
    """Busca carpetas con manifest.json dentro de la carpeta 'extensiones/'"""
    extensiones = []
    base_abs = os.path.abspath(base_path)
    for nombre in os.listdir(base_abs):
        ruta = os.path.join(base_abs, nombre)
        if os.path.isdir(ruta) and os.path.exists(os.path.join(ruta, "manifest.json")):
            extensiones.append(ruta)
    return ",".join(extensiones)

async def realizar_automatizacion():
    extension_paths = cargar_rutas_de_extensiones("extensiones")

    async with async_playwright() as p:
        # Iniciamos un contexto persistente con las extensiones cargadas
        context = await p.chromium.launch_persistent_context(
            user_data_dir="/tmp/playwright-profile",  # Cambiar si se necesita un perfil específico
            headless=False,
            args=[
                f"--disable-extensions-except={extension_paths}",
                f"--load-extension={extension_paths}"
            ]
        )

        # Abrimos la página de onboarding de la extensión
        page = await context.new_page()
        await page.goto("https://app.pbapi.xyz/dashboard?onboarding=1")

        # Esperar a que la página se cargue completamente
        await page.wait_for_load_state("domcontentloaded")  # Asegurarse de que la página esté cargada

        # Buscar y hacer clic en el botón "Agree"
        try:
            agree_button = await page.query_selector("button:has-text('Agree')")
            if agree_button:
                await agree_button.click()
                print("✅ Botón 'Agree' clickeado.")
            else:
                print("⚠️ No se encontró el botón 'Agree'.")
        except Exception as e:
            print(f"⚠️ Ocurrió un error al intentar hacer clic en el botón: {e}")

        # Llamar a my_script() de otro archivo (my_script.py) dentro del mismo contexto
        await my_script(page)  # Pasamos la página al script para usarla dentro del mismo contexto

        # Esperar la interacción del usuario para continuar
        input("Presiona Enter para continuar...")

