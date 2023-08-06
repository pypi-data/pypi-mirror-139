from importlib.util import module_from_spec, spec_from_file_location

def path_import(_name, _path):
    try:
        spec = spec_from_file_location(_name, _path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
    except FileNotFoundError: raise Exception(f'Module Not Imported! File Not Found: "{_path}"')
    return module