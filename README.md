# PYTHON ROBOT FRAMEWORK APPLICATION
This application is made for learning about PyQt5, signal, file, thread, process handle

## Install & Setup Environment
### 1. Node.js
```powershell
    # Download and install Chocolatey:
    powershell -c "irm https://community.chocolatey.org/install.ps1|iex"

    # Download and install Node.js:
    choco install nodejs --version="24.14.0"

    # Verify the Node.js version:
    node -v # Should print "v24.14.0".

    # Verify npm version:
    npm -v # Should print "11.9.0".
```
### 2. Appium
```powershell
    npm i --location=global appium
```

### 3. Appium Inspector
Find your suitable appium version and [download](https://github.com/appium/appium-inspector/releases?page=2) (I recommend not to use the latest version)

### 4. Uiautomator2 driver
```powershell
    appium driver install uiautomator2
```

### 5. Create environment variable for ANDROID_HOME

name: ANDROID_HOME
value: C:\Users\campfire\AppData\Local\Android\Sdk

