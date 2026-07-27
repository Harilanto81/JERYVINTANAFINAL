[app]
title = Jery Vintana
package.name = jeryvintana
package.domain = org.harilanto
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3==3.11.15,hostpython3==3.11.15,kivy==2.3.0

# Permissions requises
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Configuration Android
orientation = portrait
fullscreen = 0
android.accept_sdk_license = True

# Support de plusieurs architectures (pour plus de compatibilité)
android.archs = arm64-v8a,armeabi-v7a

# API
android.api = 34
android.minapi = 24
android.ndk = 26c

# Features optionnelles
android.features = android.hardware.touchscreen

# Gradle et compilation
android.gradle_dependencies = 
p4a.compiler_flags = -Wno-incompatible-function-pointer-types
p4a.python_modules_blacklist = grp,spwd,pwd

# Icône et splash
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/icon.png

# Version de Gradle
android.gradle_version = 8.0

[buildozer]
log_level = 2
warn_on_root = 1
