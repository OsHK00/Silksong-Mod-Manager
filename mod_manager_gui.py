import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import json
import os
from manager_logic import ModManagerLogic, PLUGINS_FOLDER, PathValidationResult


THEME = {
    "bg": "#0d1117",
    "fg": "#c9d1d9",
    "card": "#161b22",
    "card_hover": "#1c2128",
    "accent": "#58a6ff",
    "accent_hover": "#1f6feb",
    "success": "#3fb950",
    "success_hover": "#2ea043",
    "danger": "#f85149",
    "danger_hover": "#da3633",
    "border": "#30363d",
    "text_secondary": "#8b949e",
    "modal_bg": "#0d1117e6"
}

# ==================== IDIOMAS ====================
TRANSLATIONS = {
    "es": {
        "title": "🦋 Silksong Mod Manager",
        "add_mod": "➕ Añadir Mod",
        "about": "Acerca de",
        "base_path": "📁 Ruta Base (BepInEx):",
        "change": "Cambiar",
        "active_mods": "✅ Mods Activos",
        "inactive_mods": "⭕ Mods Inactivos",
        "search": "🔍 Buscar...",
        "no_mods": "No hay mods aquí",
        "disable": "Desactivar",
        "activate": "Activar",
        "add_new_mod": "➕ Añadir Nuevo Mod",
        "mod_name": "Nombre del Mod:",
        "dll_file": "Archivo DLL:",
        "select": "Seleccionar",
        "cancel": "Cancelar",
        "add": "Añadir",
        "not_selected": "Sin seleccionar",
        "placeholder_name": "Ej: CustomCharms",
        "success": "Éxito",
        "error": "Error",
        "invalid_path": "Ruta Inválida",
        "valid_path": "Ruta Válida",
        "path_updated": "Ruta actualizada:",
        "must_contain": "Debe contener la carpeta",
        "enter_name": "Ingresa un nombre para el mod",
        "select_dll": "Selecciona un archivo .dll",
        "mod_activated": "activado",
        "mod_deactivated": "desactivado",
        "could_not": "No se pudo",
        "about_text": "🦋 Silksong Mod Manager v2.0\n\nDesarrollado con Python & CustomTkinter\n\nGestiona mods de Hollow Knight: Silksong\n(compatible con BepInEx)\n\n© 2024 - Optimizado y rediseñado",
        "dll_files": "Archivos DLL",
        "all_files": "Todos los archivos",

        "game_not_found": "❌ No se encontró el juego",
        "game_not_found_msg": "La ruta del juego no existe.\n\nPor favor, selecciona la carpeta donde está instalado Hollow Knight: Silksong.\n\nEjemplo:\nC:\\Program Files (x86)\\Steam\\steamapps\\common\\Hollow Knight Silksong",
        "bepinex_not_installed": "⚠️ BepInEx no está instalado",
        "bepinex_not_installed_msg": "Se encontró el juego pero falta BepInEx.\n\nPara usar mods necesitas instalar BepInEx primero.\n\n¿Deseas abrir la guía de instalación?",
        "plugins_missing": "⚠️ Falta la carpeta 'plugins'",
        "plugins_missing_msg": "BepInEx está instalado pero falta la carpeta 'plugins'.\n\nEjecuta el juego una vez con BepInEx instalado para que se cree automáticamente.",
        "invalid_path_format": "❌ Ruta inválida",
        "invalid_path_msg": "La ruta seleccionada no es válida.\n\nPor favor selecciona una ruta válida.",
        "bepinex_guide": "Guía de BepInEx"
    },
    "en": {
        "title": "🦋 Silksong Mod Manager",
        "add_mod": "➕ Add Mod",
        "about": "About",
        "base_path": "📁 Base Path (BepInEx):",
        "change": "Change",
        "active_mods": "✅ Active Mods",
        "inactive_mods": "⭕ Inactive Mods",
        "search": "🔍 Search...",
        "no_mods": "No mods here",
        "disable": "Disable",
        "activate": "Activate",
        "add_new_mod": "➕ Add New Mod",
        "mod_name": "Mod Name:",
        "dll_file": "DLL File:",
        "select": "Select",
        "cancel": "Cancel",
        "add": "Add",
        "not_selected": "Not selected",
        "placeholder_name": "E.g: CustomCharms",
        "success": "Success",
        "error": "Error",
        "invalid_path": "Invalid Path",
        "valid_path": "Valid Path",
        "path_updated": "Path updated:",
        "must_contain": "Must contain the folder",
        "enter_name": "Enter a name for the mod",
        "select_dll": "Select a .dll file",
        "mod_activated": "activated",
        "mod_deactivated": "deactivated",
        "could_not": "Could not",
        "about_text": "🦋 Silksong Mod Manager v2.0\n\nDeveloped with Python & CustomTkinter\n\nManage Hollow Knight: Silksong mods\n(BepInEx compatible)\n\n© 2024 - Optimized and redesigned",
        "dll_files": "DLL Files",
        "all_files": "All Files",
        
        "game_not_found": "❌ Game not found",
        "game_not_found_msg": "The game path doesn't exist.\n\nPlease select the folder where Hollow Knight: Silksong is installed.\n\nExample:\nC:\\Program Files (x86)\\Steam\\steamapps\\common\\Hollow Knight Silksong",
        "bepinex_not_installed": "⚠️ BepInEx not installed",
        "bepinex_not_installed_msg": "Game found but BepInEx is missing.\n\nYou need to install BepInEx to use mods.\n\nWould you like to open the installation guide?",
        "plugins_missing": "⚠️ 'plugins' folder missing",
        "plugins_missing_msg": "BepInEx is installed but the 'plugins' folder is missing.\n\nRun the game once with BepInEx installed to auto-create it.",
        "invalid_path_format": "❌ Invalid path",
        "invalid_path_msg": "The selected path is not valid.\n\nPlease select a valid path.",
        "bepinex_guide": "BepInEx Guide"
    }
}

class LanguageManager:

    CONFIG_FILE = "mod_manager_config.json"
    
    def __init__(self):
        self.current_lang = self._load_language()
    
    def _load_language(self):

        try:
            if os.path.exists(self.CONFIG_FILE):
                with open(self.CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    return config.get('language', 'es')
        except:
            pass
        return 'es'
    
    def _save_language(self):
        """Guarda el idioma actual"""
        try:
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump({'language': self.current_lang}, f)
        except:
            pass
    
    def toggle_language(self):
        """Cambia entre español e inglés"""
        self.current_lang = 'en' if self.current_lang == 'es' else 'es'
        self._save_language()
        return self.current_lang
    
    def get(self, key):
        """Obtiene una traducción"""
        return TRANSLATIONS[self.current_lang].get(key, key)

class AddModModal(ctk.CTkToplevel):
    """Modal para añadir nuevos mods"""
    def __init__(self, parent, lang_manager):
        super().__init__(parent)
        
        self.lang = lang_manager
        self.title(self.lang.get("add_new_mod").replace("➕ ", ""))
        self.geometry("550x350")
        self.resizable(False, False)
        
        # Centrar modal
        self.transient(parent)
        self.grab_set()
        
        # Variables
        self.mod_name = None
        self.dll_path = None
        self.dll_path_var = ctk.StringVar(value=self.lang.get("not_selected"))
        
        self._create_widgets()
        
        # Centrar en la ventana padre
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
    
    def _create_widgets(self):
        # Frame principal con padding
        main_frame = ctk.CTkFrame(self, fg_color=THEME["card"], corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Frame scrollable interno
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Título
        title = ctk.CTkLabel(
            content_frame,
            text=self.lang.get("add_new_mod"),
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=(0, 25))
        
        # Nombre del mod
        name_label = ctk.CTkLabel(
            content_frame,
            text=self.lang.get("mod_name"),
            font=ctk.CTkFont(size=14)
        )
        name_label.pack(pady=(5, 8), anchor="w")
        
        self.name_entry = ctk.CTkEntry(
            content_frame,
            placeholder_text=self.lang.get("placeholder_name"),
            height=40,
            font=ctk.CTkFont(size=13),
            fg_color=THEME["card_hover"],
            border_color=THEME["border"]
        )
        self.name_entry.pack(pady=(0, 20), fill="x")
        self.name_entry.focus()
        
        # Archivo DLL
        dll_label = ctk.CTkLabel(
            content_frame,
            text=self.lang.get("dll_file"),
            font=ctk.CTkFont(size=14)
        )
        dll_label.pack(pady=(5, 8), anchor="w")
        
        dll_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        dll_frame.pack(pady=(0, 25), fill="x")
        dll_frame.grid_columnconfigure(0, weight=1)
        
        self.dll_display = ctk.CTkLabel(
            dll_frame,
            textvariable=self.dll_path_var,
            anchor="w",
            text_color=THEME["text_secondary"],
            font=ctk.CTkFont(size=12)
        )
        self.dll_display.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        select_btn = ctk.CTkButton(
            dll_frame,
            text=self.lang.get("select"),
            command=self._select_dll,
            width=110,
            height=38,
            fg_color=THEME["accent"],
            hover_color=THEME["accent_hover"],
            font=ctk.CTkFont(size=13)
        )
        select_btn.grid(row=0, column=1)
        
        # Botones
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.pack(pady=(10, 0), fill="x")
        button_frame.grid_columnconfigure((0, 1), weight=1)
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text=self.lang.get("cancel"),
            command=self.destroy,
            height=42,
            fg_color=THEME["card_hover"],
            hover_color=THEME["border"],
            font=ctk.CTkFont(size=13)
        )
        cancel_btn.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        
        add_btn = ctk.CTkButton(
            button_frame,
            text=self.lang.get("add"),
            command=self._add_mod,
            height=42,
            fg_color=THEME["success"],
            hover_color=THEME["success_hover"],
            font=ctk.CTkFont(size=13, weight="bold")
        )
        add_btn.grid(row=0, column=1, sticky="ew", padx=(8, 0))
        
        # Enter para añadir
        self.bind("<Return>", lambda e: self._add_mod())
        self.bind("<Escape>", lambda e: self.destroy())
    
    def _select_dll(self):
        dll_path = filedialog.askopenfilename(
            defaultextension=".dll",
            filetypes=[
                (self.lang.get("dll_files"), "*.dll"),
                (self.lang.get("all_files"), "*.*")
            ]
        )
        if dll_path:
            self.dll_path = dll_path
            filename = dll_path.split('/')[-1].split('\\')[-1]
            self.dll_path_var.set(filename)
    
    def _add_mod(self):
        self.mod_name = self.name_entry.get().strip()
        
        if not self.mod_name:
            messagebox.showerror(
                self.lang.get("error"),
                self.lang.get("enter_name"),
                parent=self
            )
            return
        
        if not self.dll_path:
            messagebox.showerror(
                self.lang.get("error"),
                self.lang.get("select_dll"),
                parent=self
            )
            return
        
        self.destroy()

class ModManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Inicializar gestor de idiomas
        self.lang = LanguageManager()
        
        # Configuración inicial
        self.title(self.lang.get("title"))
        self.geometry("950x700")
        
        # Aplicar tema oscuro
        ctk.set_appearance_mode("Dark")
        self.configure(fg_color=THEME["bg"])
        
        # Inicializar lógica
        self.mod_manager = ModManagerLogic()
        
        # Variables de caché EN MEMORIA
        self.all_active_mods = []
        self.all_disabled_mods = []
        self.is_loading = False
        
        # Configuración del layout
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Crear widgets
        self._create_header()
        self._create_path_frame()
        self._create_mod_lists()
        
        # Validación inicial de la ruta
        self._validate_initial_path()

    def _validate_initial_path(self):
        """Valida la ruta al iniciar la aplicación"""
        success, validation = self.mod_manager.set_base_path(self.mod_manager.base_path)
        
        if not success:
            # Mostrar error específico
            self.after(500, lambda: self._show_path_error(validation))
            # No cargar mods si la ruta es inválida
        else:
            # Solo cargar mods si la ruta es válida
            self._async_refresh_mod_lists()

    def _create_header(self):
        """Header con título y botones"""
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, padx=20, pady=(15, 10), sticky="ew")
        header.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(
            header, 
            text=self.lang.get("title"),
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=THEME["fg"]
        )
        title.grid(row=0, column=0, sticky="w", padx=10)
        
        # Botón de idioma (Muestra el idioma CONTRARIO al actual)
        lang_text = "EN" if self.lang.current_lang == "es" else "ES"
        self.lang_btn = ctk.CTkButton(
            header,
            text=lang_text,
            width=50,
            height=38,
            command=self._toggle_language,
            fg_color=THEME["card"],
            hover_color=THEME["card_hover"],
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.lang_btn.grid(row=0, column=1, padx=5)
        
        # Botón añadir mod
        self.add_btn = ctk.CTkButton(
            header,
            text=self.lang.get("add_mod"),
            command=self._open_add_mod_modal,
            height=38,
            fg_color=THEME["success"],
            hover_color=THEME["success_hover"],
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.add_btn.grid(row=0, column=2, padx=5)
        
        # Botón about con icono centrado
        self.about_btn = ctk.CTkButton(
            header,
            text="ℹ",
            width=45,
            height=38,
            command=self._show_about_dialog,
            fg_color=THEME["card"],
            hover_color=THEME["card_hover"],
            font=ctk.CTkFont(size=20)
        )
        self.about_btn.grid(row=0, column=3, padx=5)

    def _create_path_frame(self):
        """Frame de configuración de ruta"""
        path_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=THEME["card"])
        path_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 15), sticky="ew")
        
        path_control = ctk.CTkFrame(path_frame, fg_color="transparent")
        path_control.pack(fill="x", padx=15, pady=15)
        path_control.grid_columnconfigure(0, weight=1)
        
        self.path_label = ctk.CTkLabel(
            path_control,
            text=self.lang.get("base_path"),
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=THEME["fg"]
        )
        self.path_label.grid(row=0, column=0, columnspan=2, pady=(0, 8), sticky="w")
        
        self.path_var = ctk.StringVar(value=self.mod_manager.base_path)
        self.path_entry = ctk.CTkEntry(
            path_control,
            textvariable=self.path_var,
            state="readonly",
            height=35,
            fg_color=THEME["card_hover"],
            border_color=THEME["border"]
        )
        self.path_entry.grid(row=1, column=0, padx=(0, 10), sticky="ew")
        
        self.change_btn = ctk.CTkButton(
            path_control,
            text=self.lang.get("change"),
            command=self._change_base_path,
            width=100,
            height=35,
            fg_color=THEME["accent"],
            hover_color=THEME["accent_hover"]
        )
        self.change_btn.grid(row=1, column=1)

    def _create_mod_lists(self):
        """Crea las listas de mods con búsqueda"""
        # Activos
        active_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=THEME["card"])
        active_frame.grid(row=2, column=0, padx=(20, 10), pady=(0, 20), sticky="nsew")
        active_frame.grid_rowconfigure(2, weight=1)
        active_frame.grid_columnconfigure(0, weight=1)
        
        self.active_title = ctk.CTkLabel(
            active_frame,
            text=self.lang.get("active_mods"),
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=THEME["fg"]
        )
        self.active_title.grid(row=0, column=0, padx=15, pady=(15, 10))
        
        self.search_var_active = ctk.StringVar()
        self.search_var_active.trace_add("write", lambda *args: self._filter_active_mods())
        
        self.search_active = ctk.CTkEntry(
            active_frame,
            placeholder_text=self.lang.get("search"),
            textvariable=self.search_var_active,
            height=35,
            fg_color=THEME["card_hover"],
            border_color=THEME["border"]
        )
        self.search_active.grid(row=1, column=0, padx=15, pady=(0, 10), sticky="ew")
        
        self.active_listbox = ctk.CTkScrollableFrame(
            active_frame,
            fg_color="transparent",
            scrollbar_button_color=THEME["border"],
            scrollbar_button_hover_color=THEME["card_hover"]
        )
        self.active_listbox.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="nsew")
        
        # Inactivos
        disabled_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=THEME["card"])
        disabled_frame.grid(row=2, column=1, padx=(10, 20), pady=(0, 20), sticky="nsew")
        disabled_frame.grid_rowconfigure(2, weight=1)
        disabled_frame.grid_columnconfigure(0, weight=1)
        
        self.disabled_title = ctk.CTkLabel(
            disabled_frame,
            text=self.lang.get("inactive_mods"),
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=THEME["fg"]
        )
        self.disabled_title.grid(row=0, column=0, padx=15, pady=(15, 10))
        
        self.search_var_disabled = ctk.StringVar()
        self.search_var_disabled.trace_add("write", lambda *args: self._filter_disabled_mods())
        
        self.search_disabled = ctk.CTkEntry(
            disabled_frame,
            placeholder_text=self.lang.get("search"),
            textvariable=self.search_var_disabled,
            height=35,
            fg_color=THEME["card_hover"],
            border_color=THEME["border"]
        )
        self.search_disabled.grid(row=1, column=0, padx=15, pady=(0, 10), sticky="ew")
        
        self.disabled_listbox = ctk.CTkScrollableFrame(
            disabled_frame,
            fg_color="transparent",
            scrollbar_button_color=THEME["border"],
            scrollbar_button_hover_color=THEME["card_hover"]
        )
        self.disabled_listbox.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="nsew")

    def _render_mod_list(self, listbox: ctk.CTkScrollableFrame, mods_list: list, action_type: str):
        """Renderiza la lista de mods de forma optimizada"""
        for widget in listbox.winfo_children():
            widget.destroy()
        
        if not mods_list:
            empty_label = ctk.CTkLabel(
                listbox,
                text=self.lang.get("no_mods"),
                text_color=THEME["text_secondary"],
                font=ctk.CTkFont(size=13)
            )
            empty_label.pack(pady=30)
            return
        
        if action_type == "disable":
            btn_text = self.lang.get("disable")
            btn_fg = THEME["danger"]
            btn_hover = THEME["danger_hover"]
        else:
            btn_text = self.lang.get("activate")
            btn_fg = THEME["success"]
            btn_hover = THEME["success_hover"]
        
        for mod_data in mods_list:
            frame = ctk.CTkFrame(
                listbox,
                corner_radius=8,
                fg_color=THEME["card_hover"],
                border_width=1,
                border_color=THEME["border"]
            )
            frame.pack(fill="x", padx=5, pady=4)
            frame.columnconfigure(0, weight=1)
            
            mod_name = mod_data['name']
            icon = "📁" if mod_data['is_folder'] else "📄"
            label_text = f"{icon} {mod_name}"
            
            if not mod_data['is_folder']:
                label_text += " (DLL)"
            
            mod_label = ctk.CTkLabel(
                frame,
                text=label_text,
                anchor="w",
                font=ctk.CTkFont(size=13),
                text_color=THEME["fg"]
            )
            mod_label.grid(row=0, column=0, padx=12, pady=10, sticky="ew")
            
            action_btn = ctk.CTkButton(
                frame,
                text=btn_text,
                width=100,
                height=32,
                fg_color=btn_fg,
                hover_color=btn_hover,
                font=ctk.CTkFont(size=12),
                command=lambda m=mod_data: self._handle_mod_action(m, action_type)
            )
            action_btn.grid(row=0, column=1, padx=12, pady=10)

    def _filter_active_mods(self):
        """Filtra mods activos"""
        if self.is_loading:
            return
        
        search_term = self.search_var_active.get().strip().lower()
        filtered = [m for m in self.all_active_mods if search_term in m['name'].lower()]
        self._render_mod_list(self.active_listbox, filtered, "disable")

    def _filter_disabled_mods(self):
        """Filtra mods inactivos"""
        if self.is_loading:
            return
        
        search_term = self.search_var_disabled.get().strip().lower()
        filtered = [m for m in self.all_disabled_mods if search_term in m['name'].lower()]
        self._render_mod_list(self.disabled_listbox, filtered, "activate")

    def _async_refresh_mod_lists(self):
        """Carga los mods de forma asíncrona"""
        if self.is_loading:
            return
        
        self.is_loading = True
        
        def load_mods():
            try:
                active, disabled = self.mod_manager.get_installed_mods()
                self.all_active_mods = active
                self.all_disabled_mods = disabled
                
                self.after(0, self._update_lists_after_load)
            except Exception as e:
                print(f"Error cargando mods: {e}")
                self.is_loading = False
        
        thread = threading.Thread(target=load_mods, daemon=True)
        thread.start()

    def _update_lists_after_load(self):
        """Actualiza las listas después de la carga asíncrona"""
        self.is_loading = False
        self._filter_active_mods()
        self._filter_disabled_mods()

    def _toggle_language(self):
        """Cambia el idioma de la aplicación"""
        self.lang.toggle_language()
        self._refresh_ui_texts()
    
    def _refresh_ui_texts(self):
        """Actualiza todos los textos de la interfaz"""
        # Título de la ventana
        self.title(self.lang.get("title"))
        
        # Botón de idioma (muestra el idioma al que CAMBIARÁ)
        lang_text = "EN" if self.lang.current_lang == "es" else "ES"
        self.lang_btn.configure(text=lang_text)
        
        # Header
        self.add_btn.configure(text=self.lang.get("add_mod"))
        
        # Path frame
        self.path_label.configure(text=self.lang.get("base_path"))
        self.change_btn.configure(text=self.lang.get("change"))
        
        # Títulos de listas
        self.active_title.configure(text=self.lang.get("active_mods"))
        self.disabled_title.configure(text=self.lang.get("inactive_mods"))
        
        # Placeholders de búsqueda
        self.search_active.configure(placeholder_text=self.lang.get("search"))
        self.search_disabled.configure(placeholder_text=self.lang.get("search"))
        
        # Re-renderizar listas para actualizar botones
        self._filter_active_mods()
        self._filter_disabled_mods()

    def _change_base_path(self):
        """Cambia la ruta base con validación mejorada"""
        new_path = filedialog.askdirectory(initialdir=self.mod_manager.base_path)
        
        if new_path:
            success, validation = self.mod_manager.set_base_path(new_path)
            
            if success:
                messagebox.showinfo(
                    self.lang.get("valid_path"),
                    f"{self.lang.get('path_updated')}\n{new_path}"
                )
                self.path_var.set(self.mod_manager.base_path)
                self._async_refresh_mod_lists()
            else:
                # Mostrar error específico según el tipo
                self._show_path_error(validation)
    
    def _show_path_error(self, validation: PathValidationResult):
        """Muestra un error específico según el problema detectado"""
        import webbrowser
        
        if validation.error_type == 'no_game':
            messagebox.showerror(
                self.lang.get("game_not_found"),
                self.lang.get("game_not_found_msg")
            )
        
        elif validation.error_type == 'no_bepinex':
            # Preguntar si quiere abrir la guía
            result = messagebox.askyesno(
                self.lang.get("bepinex_not_installed"),
                self.lang.get("bepinex_not_installed_msg")
            )
            if result:
                # Abrir guía de instalación de BepInEx
                webbrowser.open("https://www.nexusmods.com/hollowknightsilksong/mods/26")
        
        elif validation.error_type == 'no_plugins':
            messagebox.showwarning(
                self.lang.get("plugins_missing"),
                self.lang.get("plugins_missing_msg")
            )
        
        else:
            messagebox.showerror(
                self.lang.get("invalid_path_format"),
                self.lang.get("invalid_path_msg")
            )

    def _open_add_mod_modal(self):
        """Abre el modal para añadir un mod"""
        modal = AddModModal(self, self.lang)
        self.wait_window(modal)
        
        if modal.mod_name and modal.dll_path:
            success, message = self.mod_manager.add_mod(modal.dll_path, modal.mod_name)
            
            if success:
                messagebox.showinfo(self.lang.get("success"), message)
                self._async_refresh_mod_lists()
            else:
                messagebox.showerror(self.lang.get("error"), message)

    def _handle_mod_action(self, mod_data: dict, action: str):
        """
        Maneja activación/desactivación de mods CON OPTIMIZACIÓN EN MEMORIA.
        No recarga del disco, solo actualiza las listas en memoria.
        """
        success = False
        
        if action == "disable":
            success = self.mod_manager.disable_mod(mod_data)
            action_text = self.lang.get("mod_deactivated")
        else:
            success = self.mod_manager.activate_mod(mod_data)
            action_text = self.lang.get("mod_activated")
        
        if success:
            # OPTIMIZACIÓN: Mover en memoria sin recargar del disco
            if action == "disable":
                self.all_active_mods = [m for m in self.all_active_mods if m['name'] != mod_data['name']]
                self.all_disabled_mods.append(mod_data)
            else:
                self.all_disabled_mods = [m for m in self.all_disabled_mods if m['name'] != mod_data['name']]
                self.all_active_mods.append(mod_data)
            
            # Actualizar SOLO la UI, sin recargar del disco
            self._filter_active_mods()
            self._filter_disabled_mods()
            
            messagebox.showinfo(
                self.lang.get("success"),
                f"'{mod_data['name']}' {action_text}"
            )
        else:
            messagebox.showerror(
                self.lang.get("error"),
                f"{self.lang.get('could_not')} {action} '{mod_data['name']}'"
            )

    def _show_about_dialog(self):
        """Muestra información sobre la app"""
        messagebox.showinfo(
            self.lang.get("about"),
            self.lang.get("about_text")
        )

if __name__ == "__main__":
    app = ModManagerApp()
    app.mainloop()