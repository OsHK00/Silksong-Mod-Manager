import os
import shutil
from typing import List, Tuple, Optional

DEFAULT_BASE_PATH = r"C:\Program Files (x86)\Steam\steamapps\common\Hollow Knight Silksong\BepInEx"
PLUGINS_FOLDER = "plugins"
DISABLEDS_FOLDER = "disableds"
MOD_EXTENSION = ".dll"

class PathValidationResult:
    """Resultado de la validación de ruta"""
    def __init__(self, is_valid: bool, error_type: str = None, message: str = None):
        self.is_valid = is_valid
        self.error_type = error_type  # 'no_game', 'no_bepinex', 'no_plugins', 'invalid'
        self.message = message

class ModManagerLogic:
    def __init__(self, base_path: str = DEFAULT_BASE_PATH):
        self._base_path = base_path
        self._plugins_path = os.path.join(self._base_path, PLUGINS_FOLDER)
        self._disableds_path = os.path.join(self._base_path, DISABLEDS_FOLDER)
        # NO crear carpetas automáticamente
        
    @property
    def base_path(self) -> str:
        return self._base_path
    
    def _ensure_disabled_folder_exists(self):
        """Crea la carpeta disableds solo si BepInEx ya existe"""
        if not os.path.exists(self._disableds_path):
            try:
                os.makedirs(self._disableds_path)
            except:
                pass

    def validate_path(self, path: str) -> PathValidationResult:

        # Caso 1: Ruta vacía o inválida
        if not path or not os.path.isabs(path):
            return PathValidationResult(
                False, 
                'invalid',
                'invalid_path_format'
            )
        
        # Caso 2: Verificar si la ruta apunta a BepInEx
        if path.endswith('BepInEx'):
            bepinex_path = path
            game_path = os.path.dirname(path)
        else:
            # Asumir que la ruta apunta al juego
            game_path = path
            bepinex_path = os.path.join(path, 'BepInEx')
        
        # Verificar existencia del directorio del juego
        if not os.path.exists(game_path):
            return PathValidationResult(
                False,
                'no_game',
                'game_not_found'
            )
        
        # Verificar si existe BepInEx
        if not os.path.exists(bepinex_path):
            return PathValidationResult(
                False,
                'no_bepinex',
                'bepinex_not_installed'
            )
        
        # Verificar si existe la carpeta plugins
        plugins_path = os.path.join(bepinex_path, PLUGINS_FOLDER)
        if not os.path.exists(plugins_path):
            return PathValidationResult(
                False,
                'no_plugins',
                'plugins_folder_missing'
            )
        
        
        return PathValidationResult(True)

    def set_base_path(self, new_path: str) -> Tuple[bool, Optional[PathValidationResult]]:

        validation = self.validate_path(new_path)
        
        if validation.is_valid:
            # Ajustar la ruta para que apunte a BepInEx si es necesario
            if new_path.endswith('BepInEx'):
                self._base_path = new_path
            else:
                self._base_path = os.path.join(new_path, 'BepInEx')
            
            self._plugins_path = os.path.join(self._base_path, PLUGINS_FOLDER)
            self._disableds_path = os.path.join(self._base_path, DISABLEDS_FOLDER)
            self._ensure_disabled_folder_exists()
            return True, validation
        
        return False, validation

    def get_installed_mods(self) -> Tuple[List[dict], List[dict]]:

        active_mods = []
        disabled_mods = []
        
        def scan_folder(folder_path):
            mods = []
            if os.path.exists(folder_path):
                try:
                    for item in os.listdir(folder_path):
                        full_path = os.path.join(folder_path, item)
                        
                        if os.path.isdir(full_path):
                            # Caso 1: Mod en Carpeta (Comprobar si contiene un DLL)
                            try:
                                if any(file.endswith(MOD_EXTENSION) for file in os.listdir(full_path)):
                                    mods.append({'name': item, 'is_folder': True})
                            except:
                                pass
                        
                        elif os.path.isfile(full_path) and item.lower().endswith(MOD_EXTENSION):
                            # Caso 2: Mod DLL Suelto
                            mod_name = item[:-len(MOD_EXTENSION)]
                            mods.append({'name': mod_name, 'is_folder': False})
                except Exception as e:
                    print(f"Error al escanear {folder_path}: {e}")
            return mods

        active_mods = scan_folder(self._plugins_path)
        disabled_mods = scan_folder(self._disableds_path)

        return active_mods, disabled_mods

    def _move_mod(self, mod_data: dict, source_path: str, dest_path: str) -> bool:

        mod_name = mod_data['name']
        is_folder = mod_data['is_folder']

        if is_folder:
            # Mover la carpeta completa
            source = os.path.join(source_path, mod_name)
            destination = os.path.join(dest_path, mod_name)
            try:
                shutil.move(source, destination)
                return True
            except Exception as e:
                print(f"Error al mover la carpeta {mod_name}: {e}")
                return False
        else:
            # Mover DLL suelto y envolverlo en una carpeta en el destino
            dll_filename = mod_name + MOD_EXTENSION
            source_dll = os.path.join(source_path, dll_filename)
            
            # Crear la carpeta de destino con el nombre del mod
            target_mod_folder = os.path.join(dest_path, mod_name)
            if not os.path.exists(target_mod_folder):
                try:
                    os.makedirs(target_mod_folder)
                except Exception as e:
                    print(f"Error al crear carpeta {mod_name}: {e}")
                    return False
            
            target_dll_path = os.path.join(target_mod_folder, dll_filename)
            
            try:
                shutil.move(source_dll, target_dll_path)
                return True
            except Exception as e:
                print(f"Error al mover el DLL {dll_filename}: {e}")
                return False

    def activate_mod(self, mod_data: dict) -> bool:

        return self._move_mod(mod_data, self._disableds_path, self._plugins_path)

    def disable_mod(self, mod_data: dict) -> bool:

        return self._move_mod(mod_data, self._plugins_path, self._disableds_path)
    
    def add_mod(self, mod_path: str, mod_name: str) -> Tuple[bool, str]:

        if not mod_path.lower().endswith(MOD_EXTENSION):
            return False, "El archivo debe ser un .dll"

        target_mod_folder = os.path.join(self._plugins_path, mod_name)
        target_dll_path = os.path.join(target_mod_folder, os.path.basename(mod_path))

        try:
            # Verificar si ya existe
            if os.path.exists(target_mod_folder) or os.path.exists(os.path.join(self._plugins_path, mod_name + MOD_EXTENSION)):
                return False, f"Ya existe un mod con el nombre '{mod_name}'"

            os.makedirs(target_mod_folder)
            shutil.copy(mod_path, target_dll_path)
            return True, "Mod añadido con éxito"
        except Exception as e:
            return False, f"Error al añadir el mod: {e}"

if __name__ == '__main__':
    # Pruebas de validación
    manager = ModManagerLogic()
    
    test_paths = [
        DEFAULT_BASE_PATH,
        r"C:\Program Files (x86)\Steam\steamapps\common\Hollow Knight Silksong",
        r"C:\InvalidPath",
    ]
    
    for path in test_paths:
        result = manager.validate_path(path)
        print(f"\nRuta: {path}")
        print(f"Válida: {result.is_valid}")
        if not result.is_valid:
            print(f"Error: {result.error_type} - {result.message}")