import subprocess, os, sys
import tkinter as tk
import tkinter.filedialog as filedialog

from datetime import datetime

from lib.settings import Settings
from lib.utils.binder import Binder
from lib.utils.events import Events

from lib.components.git import GitCore

class Base:
    def __init__(self, root, *args, **kwargs):
        self.root = root
        self.appdir = root.appdir
        self.settings = Settings(self)
        self.bindings = self.settings.bindings

        self.git_found = False
        self.git = GitCore(self)
        print(self.git.get_version())

        self.active_dir = None
        self.active_file = None

        # Opened files
        # [file, exists]
        self.opened_files = []

        self.events = Events(self)
        self.binder = Binder(base=self)

    def trace(self, e):
        time = datetime.now().strftime('• %H:%M:%S •')
        print(f'TRACE {time} {e}')

    def refresh_dir(self):
        self.root.basepane.top.left.dirtree.create_root(self.active_dir)

    def set_active_file(self, file, exists=True):
        if not file:
            return

        self.active_file = file
        self.trace(f"Active file<{self.active_file}>")

        if not exists or file not in [f[0] for f in self.opened_files]:
            self.add_to_open_files(file, exists)
            self.trace(f"File<{self.active_file}> was added.")
        else:
            self.root.basepane.top.right.editortabs.set_active_tab(file)

    def set_active_dir(self, dir):
        if not os.path.isdir(dir):
            return

        self.active_dir = dir
        self.update_git()
        self.refresh_dir()
        self.clean_opened_files()
        self.trace(self.active_dir)

    def add_to_open_files(self, file, exists):
        self.opened_files.append([file, exists])
        self.trace(f"Opened Files {self.opened_files}")

        self.root.basepane.top.right.editortabs.update_tabs()
    
    def remove_from_open_files(self, file):
        for i in self.opened_files:
            if i[0] == file:
                self.opened_files.remove(i)
                self.root.basepane.top.right.editortabs.update_tabs()
        self.trace(self.opened_files)
    
    def get_opened_files(self):
        return self.opened_files
    
    def clean_opened_files(self):
        self.opened_files = []
        self.active_file = None
        self.trace(f"<ClearOpenFilesEvent>({self.opened_files})")
    
    def open_in_new_window(self, dir):
        subprocess.Popen(["python", sys.argv[0], dir])

        self.trace(f'Opened in new window: {dir}')
    
    def open_new_window(self):
        subprocess.Popen(["python", sys.argv[0]])

        self.trace(f'Opened new window')
    
    def update_git(self):
        self.git.open_repo()

        self.update_statusbar_git_info()
    
    def update_statusbar_git_info(self):
        self.root.statusbar.set_git_info(self.git.get_active_branch())

    def update_statusbar_ln_col_info(self):
        active_text = self.root.basepane.top.right.editortabs.get_active_tab().text
        self.root.statusbar.set_line_col_info(active_text.line, active_text.column, active_text.get_selected_count())