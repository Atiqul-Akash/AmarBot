import os
import importlib

def setup(bot):
    commands_dir = os.path.dirname(__file__)
    for filename in os.listdir(commands_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"{__name__}.{filename[:-3]}"
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, "setup"):
                    module.setup(bot)
            except Exception as e:
                print(f"Failed to load command module {module_name}: {e}")
