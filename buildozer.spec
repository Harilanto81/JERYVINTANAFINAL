[app]
title = Jery Vintana
package.name = jeryvintana
package.domain = org.harilanto
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json
version = 1.0.0

# --- REQUIREMENTS OPTIMISÉS ---
# Ajout des recettes natives SDL2 et OpenSSL indispensables pour KivyMD & Pillow
requirements = python3, hostpython3, kivy==2.3.0, kivymd, pillow, sdl2_image, sdl2_ttf, openssl

orientation = portrait
fullscreen = 0

# --- CONFIGURATION ANDROID ---
android.accept_sdk_license = True
android.archs = arm64-v8a
android.api = 33
android.minapi = 24
android.ndk = 25b

# Permissions de base si KivyMD accède à Internet/Stockage
android.permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 1
