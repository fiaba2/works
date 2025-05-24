[app]
title = WorkTracker
package.name = worktracker
package.domain = org.yourdomain
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,kivymd,pyrebase4,certifi,urllib3,requests
orientation = portrait
fullscreen = 1

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.permissions = INTERNET
