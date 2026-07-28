[app]
title = Jery Vintana
package.name = jeryvintana
package.domain = org.harilanto
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

# --- DÉPENDANCES CORRIGÉES ---
# Utlisation de kivymd 1.2.0 avec materialyoucolor pour éviter le crash de p4a
requirements = python3,kivy==2.3.0,kivymd==1.2.0,materialyoucolor,pillow

orientation = portrait
fullscreen = 0

# --- CONFIGURATION ANDROID ---
android.accept_sdk_license = True
android.archs = arm64-v8a
android.api = 33
android.minapi = 24
android.ndk = 25b

# Icônes et Presplash
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
warn_on_root = 1
