import pathlib
import shutil

from mycfg import meta, const
from mycfg import lib


class Unit:
    def __init__(self, name, cfg):
        self.name = name
        self.cfg = cfg

        self.files = cfg.get("files", [])
        self.home_path = pathlib.Path.home()
        self.glob = sum([[y for y in self.home_path.glob(z)] for z in self.files], [])
        self.install_commands = lib.ensure_list(cfg.get("install-command", []))
        self.install_scripts = lib.ensure_list(cfg.get("install-script", []))

        self.save_scripts_pre = lib.ensure_list(cfg.get("save-scripts-pre", []))
        self.save_scripts_post = lib.ensure_list(cfg.get("save-scripts-post", []))

        self.load_scripts_pre = lib.ensure_list(cfg.get("save-scripts-pre", []))
        self.load_scripts_post = lib.ensure_list(cfg.get("load-scripts-post", []))

        self.required_packages = lib.ensure_list(cfg.get("requires-packages", []))

    def load(self):
        for pkg in self.required_packages:
            if pkg not in meta.get("installed_packages"):
                lib.install_pkg(pkg)
                meta.append("installed_packages", pkg)
        if self.name not in meta.get("installed_units"):
            for cmd in self.install_commands:
                lib.sh(cmd)
            for script in self.install_scripts:
                lib.exec_script(script)
            meta.append("installed_units", self.name)
        for script in self.load_scripts_pre:
            lib.exec_script(script)
        for file in self.glob:
            src_file = const.DOTFILES_SAVE_DIR.joinpath(file.relative_to(self.home_path))
            if src_file.is_file():
                shutil.copy2(src_file, file)
            elif src_file.is_dir():
                shutil.copytree(src_file, file,
                                dirs_exist_ok=True, ignore=shutil.ignore_patterns(*const.IGNORE_PATTERNS))
            else:
                print(f"[{src_file}] not found")
        for script in self.load_scripts_post:
            lib.exec_script(script)
        meta.save()

    def save(self):
        for script in self.save_scripts_pre:
            lib.exec_script(script)
        for file in self.glob:
            if file.is_file():
                shutil.copy2(file, const.DOTFILES_SAVE_DIR.joinpath(file.relative_to(self.home_path)))
            elif file.is_dir():
                shutil.copytree(file, const.DOTFILES_SAVE_DIR.joinpath(file.relative_to(self.home_path)),
                                dirs_exist_ok=True, ignore=shutil.ignore_patterns(*const.IGNORE_PATTERNS))
            else:
                print(f"[{file}] not found")
        for script in self.save_scripts_post:
            lib.exec_script(script)
