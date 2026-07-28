[app]
title = Jery Vintana
package.name = jeryvintana
package.domain = org.harilanto
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json
version = 1.0.0

# Requirements épurés
requirements = python3,kivy==2.3.0,kivymd,pillow,openssl

orientation = portrait
fullscreen = 0

# Utiliser la branche master de p4a pour inclure les patchs Harfbuzz / NDK 25b
p4a.branch = master

# --- CONFIGURATION ANDROID ---
android.accept_sdk_license = True
android.archs = arm64-v8a
android.api = 33
android.minapi = 24
android.ndk = 25b

android.permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 1
