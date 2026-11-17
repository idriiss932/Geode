import re,shutil,os,sys
run=os.environ.get('RUN_NUMBER','1')
p='android/app/build.gradle'
g=open(p).read()
if 'signingConfigs.geode' not in g:
    g=g.replace("buildTypes {","signingConfigs {\n        geode {\n            storeFile file('geode.keystore')\n            storePassword 'geodepass'\n            keyAlias 'geode'\n            keyPassword 'geodepass'\n        }\n    }\n    buildTypes {",1)
    g=g.replace("release {","release {\n            signingConfig signingConfigs.geode",1)
g=re.sub(r"versionCode \d+","versionCode "+run,g,1)
g=re.sub(r'versionName "[^"]*"','versionName "2.0"',g,1)
open(p,'w').write(g)
shutil.copy('geode.keystore','android/app/geode.keystore')
shutil.copytree('res','android/app/src/main/res',dirs_exist_ok=True)
n=0
for d,_,fs in os.walk('android/app/src/main/res'):
    for f in fs:
        if f=='splash.png':shutil.copy('splash.png',os.path.join(d,f));n+=1
print('splash replaced',n)
# nom + notification icon
s='android/app/src/main/res/values/strings.xml'
t=open(s).read();t=re.sub(r'<string name="app_name">[^<]*</string>','<string name="app_name">Géode</string>',t);t=re.sub(r'<string name="title_activity_main">[^<]*</string>','<string name="title_activity_main">Géode</string>',t);open(s,'w').write(t)
m='android/app/src/main/AndroidManifest.xml'
x=open(m).read()
if 'android:screenOrientation' not in x:
    x=x.replace('android:launchMode="singleTask"','android:launchMode="singleTask"\n            android:screenOrientation="portrait"',1)
if 'POST_NOTIFICATIONS' not in x:
    x=x.replace('</manifest>','    <uses-permission android:name="android.permission.POST_NOTIFICATIONS"/>\n</manifest>')
open(m,'w').write(x)
print('patched')
