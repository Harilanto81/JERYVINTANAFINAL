[app]
title = Jery Vintana
package.name = jeryvintana
package.domain = org.harilanto
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

requirements = python3,kivy

# Ao anatin'ny [buildozer]
log_level = 2
warn_on_root = 1

orientation = portrait
fullscreen = 0

android.archs = armeabi-v7a

# Mandraiky ny licence SDK automatique
android.accept_sdk_license = True
android.ndk = 25b
android.sdk = 25

# Sary icône
icon.filename = %(source.dir)s/icon.png

# Sary splash screen (fakana ny icon.png ho splash)
presplash.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
warn_on_root = 1
