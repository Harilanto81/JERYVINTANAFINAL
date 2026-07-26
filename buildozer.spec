[app]
title = Jery Vintana
package.name = jeryvintana
package.domain = org.harilanto
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

# Mandraiky ny licence SDK automatique
android.accept_sdk_license = True

# Sary icône
icon.filename = %(source.dir)s/icon.png

# Sary splash screen (fakana ny icon.png ho splash)
presplash.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
warn_on_root = 1
