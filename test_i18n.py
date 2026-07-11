from aiogram_i18n.cores import FluentRuntimeCore
import os

# Попробуем разные варианты путей
paths = ["locales/{locale}", "./locales/{locale}", os.path.abspath("locales/{locale}")]

for p in paths:
    try:
        core = FluentRuntimeCore(path=p, default_locale="en")
        print(f"Path: {p} | Loaded: {core.locales}")
    except Exception as e:
        print(f"Path: {p} | Error: {e}")
