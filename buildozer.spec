[app]
title = Jery Vintana
package.name = jeryvintana
package.domain = org.harilanto
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

# Ajout de libffi et openssl pour la compatibilité p4a
requirements = python3,hostpython3,kivy==2.3.0,kivymd==1.2.0,pillow,libffi,openssl

orientation = portrait
fullscreen = 0

# Config Android
android.accept_sdk_license = True
android.archs = arm64-v8a
android.api = 33
android.minapi = 24
android.ndk = 25b

[buildozer]
log_level = 2
warn_on_root = 1
