[app]

# title of your application
title = "Neonaure"

# project root directory. default = The parent directory of input_file
source_dir = .

# source file entry point path. default = main.py
input_file = main.py

# directory where the executable output is generated
exec_directory = .

# path to the project file relative to project_dir
project_file = 

# application icon
icon = /mnt/c/Users/H/Documents/SAE IHM/Neonaure/.venv/lib/python3.11/site-packages/PySide6/scripts/deploy_lib/pyside_icon.jpg
project_dir = .

[python]

# python path
python_path = /mnt/c/Users/H/Documents/SAE IHM/Neonaure/.venv/bin/python3.11

# python packages to install
packages = Nuitka==4.0

# buildozer = for deploying Android application
android_packages = buildozer==1.5.0,cython==0.29.33

[qt]

# paths to required qml files. comma separated
# normally all the qml files required by the project are added automatically
# design studio projects include the qml files using qt resources
qml_files = 

# excluded qml plugin binaries
excluded_qml_plugins = 

# qt modules used. comma separated
modules = Core,Widgets,Gui

# qt plugins used by the application. only relevant for desktop deployment
# for qt plugins used in android application see [android][plugins]
plugins = 

[android]

# path to pyside wheel
wheel_pyside = /mnt/c/Users/H/Documents/SAE IHM/Neonaure/whl/pyside6-6.11.1-6.11.1-cp311-cp311-android_aarch64.whl

# path to shiboken wheel
wheel_shiboken = /mnt/c/Users/H/Documents/SAE IHM/Neonaure/whl/shiboken6-6.11.1-6.11.1-cp311-cp311-android_aarch64.whl

# plugins to be copied to libs folder of the packaged application. comma separated
plugins = platforms_qtforandroid

[nuitka]

# usage description for permissions requested by the app as found in the info.plist file
# of the app bundle. comma separated
# eg = extra_args = --show-modules --follow-stdlib
macos.permissions = 

# mode of using nuitka. accepts standalone or onefile. default = onefile
mode = onefile

# specify any extra nuitka arguments
extra_args = --quiet --noinclude-qt-translations

[buildozer]

# build mode
# possible values = ["aarch64", "armv7a", "i686", "x86_64"]
# release creates a .aab, while debug creates a .apk
mode = debug

# path to pyside6 and shiboken6 recipe dir
recipe_dir = /mnt/c/Users/H/Documents/SAE IHM/Neonaure/deployment/recipes

# path to extra qt android .jar files to be loaded by the application
jars_dir = /mnt/c/Users/H/Documents/SAE IHM/Neonaure/deployment/jar/PySide6/jar

# if empty, uses default ndk path downloaded by buildozer
ndk_path = /home/h/.pyside6_android_deploy/android-sdk/ndk/26.3.11579264

# if empty, uses default sdk path downloaded by buildozer
sdk_path = /home/h/.pyside6_android_deploy/android-sdk

# other libraries to be loaded at app startup. comma separated.
local_libs = plugins_platforms_qtforandroid

# architecture of deployed platform
arch = aarch64

