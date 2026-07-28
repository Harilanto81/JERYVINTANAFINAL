[app]
title = Jery Vintana
package.name = jeryvintana
package.domain = org.harilanto
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json
version = 1.0.0

# --- REQUIREMENTS PURGÉS ---
# On laisse Kivy gérer SDL2 en interne sans forcer sdl2_ttf/sdl2_image qui font planter Harfbuzz
requirements = python3,kivy==2.3.0,kivymd,pillow,openssl

orientation = portrait
fullscreen = 0

# --- CONFIGURATION ANDROID ---
android.accept_sdk_license = True
android.archs = arm64-v8a
android.api = 33
android.minapi = 24
android.ndk = 25b

# Permissions de base
android.permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 1
