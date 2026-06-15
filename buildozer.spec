[app]
title = Neonaure
package.name = Neonaure
package.domain = org.Neonaure
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,qml,js,json
version = 0.1
requirements = python3==3.11.11,hostpython3==3.11.11, shiboken6,PySide6, numpy
orientation = portrait
osx.python_version = 3
osx.kivy_version = 1.9.1
fullscreen = 0
android.archs = arm64-v8a
android.allow_backup = True
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0
ios.codesign.allowed = false
android.ndk_path = /home/h/.pyside6_android_deploy/android-sdk/ndk/26.3.11579264
android.sdk_path = /home/h/.pyside6_android_deploy/android-sdk
p4a.bootstrap = qt
p4a.local_recipes = /home/h/Neonaure/deployment/recipes
p4a.branch = master
android.permissions = android.permission.WRITE_EXTERNAL_STORAGE, android.permission.INTERNET
android.add_jars = /home/h/Neonaure/deployment/jar/PySide6/jar/Qt6AndroidBindings.jar,/home/h/Neonaure/deployment/jar/PySide6/jar/Qt6Android.jar
p4a.extra_args = --qt-libs=Widgets,Core,Gui --load-local-libs=plugins_platforms_qtforandroid --init-classes=
icon.filename = /mnt/c/Users/H/Documents/SAE IHM/Neonaure/.venv/lib/python3.11/site-packages/PySide6/scripts/deploy_lib/pyside_icon.jpg

[buildozer]
log_level = 2
warn_on_root = 1
bin_dir = /home/h/Neonaure

