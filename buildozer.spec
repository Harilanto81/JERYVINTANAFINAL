[app]
title = Jery Vintana
package.name = jeryvintana
package.domain = org.harilanto
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

requirements = python3==3.11.15,kivy==2.3.0

orientation = portrait
fullscreen = 0

android.accept_sdk_license = True
android.archs = armeabi-v7a, arm64-v8a
android.api = 34
android.minapi = 24
android.ndk = 25b

icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
warn_on_root = 1
