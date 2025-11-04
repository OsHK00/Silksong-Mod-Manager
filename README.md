# 🦋 Silksong Mod Manager (BepInEx)

Un gestor de mods ligero y moderno para Hollow Knight: Silksong Desarrollado en Python con CustomTkinter.

## Características

* **Diseño Oscuro:** Interfaz limpia y moderna usando CustomTkinter.
* **Activación/Desactivación Rápida:** Mueve los mods entre las carpetas `plugins/` y `disableds/`.
* **Organización Automática:** Los archivos DLL sueltos se envuelven automáticamente en una carpeta al activarse/desactivarse.
* **Búsqueda Rápida:** Filtrado de mods en tiempo real para listas grandes.
* **Portable:** Distribución como un solo archivo ejecutable (`.exe`).

## Descarga y Uso

La forma más sencilla es descargar el ejecutable listo para usar desde la pestaña **[Releases]**.

### Ejecutable para Windows (.exe)

1.  Ve a la pestaña [Releases] en este repositorio.
2.  Descarga el archivo `SilksongModManager.exe` bajo el último *release*.
3.  Ejecuta el `.exe` y establece tu ruta base de `BepInEx`.

## Para Desarrolladores (Ejecutar desde el código fuente)

Si deseas ejecutar o modificar el código, sigue estos pasos:

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://docs.github.com/es/repositories/creating-and-managing-repositories/quickstart-for-repositories](https://docs.github.com/es/repositories/creating-and-managing-repositories/quickstart-for-repositories)
    cd SilksongModManager
    ```
2.  **Instalar dependencias:** (Necesitas Python 3.x)
    ```bash
    pip install -r requirements.txt
    ```
3.  **Ejecutar:**
    ```bash
    python mod_manager_gui.py
    ```
