// Modules to control application life and create native browser window
const { app, BrowserWindow, Menu, Tray, ipcMain } = require('electron')
const path = require('path')
app.commandLine.appendSwitch('ignore-certificate-errors');
app.setLoginItemSettings({
  openAtLogin: true,
  args: ['--hidden']
});
const isDev = process.env.NODE_ENV === 'development' ? true : false
let mainWindow = null

if (process.defaultApp) {
  if (process.argv.length >= 2) {
    app.setAsDefaultProtocolClient('collabos', process.execPath, [path.resolve(process.argv[1])])
  }
} else {
  app.setAsDefaultProtocolClient('collabos')
}

// Deep linked url
let deeplinkingUrl

const gotTheLock = app.requestSingleInstanceLock()

if (!gotTheLock) {
  app.quit()
} else {
  app.on('second-instance', (event, commandLine, workingDirectory) => {
    // Someone tried to run a second instance, we should focus our window.
    // Protocol handler for win32
    // argv: An array of the second instance’s (command line / deep linked) arguments
    if (process.platform == 'win32') {
      // Keep only command line / deep linked arguments
      deeplinkingUrl = argv.slice(1)
    }
    logEverywhere('app.makeSingleInstance# ' + deeplinkingUrl)

    if (mainWindow) {
      if (mainWindow.isMinimized()) mainWindow.restore()
      mainWindow.focus()
    }
  })
  // Create mainWindow, load the rest of the app, etc...
  app.whenReady().then(() => {
    createWindow()

  })

  app.on('open-url', (event, url) => {
    dialog.showErrorBox('Welcome Back', `You arrived from: ${url}`)
  })
}




function createWindow() {
  // Create the browser window.
  mainWindow = new BrowserWindow({
    show: false,
    width: 1100,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      enableRemoteModule: true,
      contextIsolation: false,
      preload: path.join(__dirname, 'preload.js')
    }
  })
  // console.log(mainWindow.webContents.getURL())
  // and load the index.html of the app.
  // mainWindow.loadFile(path.join(__dirname, 'build/index.html'))
  console.log(process.env.NODE_ENV)
  const loadURL = isDev ? 'https://localhost:3000' : path.join(__dirname, '../index.html')
  console.log(loadURL)
  mainWindow.loadURL(loadURL)

  // Open the DevTools.
  // mainWindow.webContents.openDevTools()

  // Protocol handler for win32
  if (process.platform == 'win32') {
    // Keep only command line / deep linked arguments
    deeplinkingUrl = process.argv.slice(1)
  }
  logEverywhere('createWindow# ' + deeplinkingUrl)


  //   localStorage.setItem('deeplinking', deeplinkingUrl)
  //   mainWindow.webContents.send('test', deeplinkingUrl)

  mainWindow.on('close', function (event) {
    if (!app.isQuiting) {
      event.preventDefault();
      mainWindow.hide();
    }

    return false;
  });
  if (!app.isPackaged) {
    mainWindow.webContents.openDevTools();
  }
  mainWindow.webContents.on('new-window',
    (event, url, frameName, disposition, options, additionalFeatures) => {
      // This is the name we chose for our window. You can have multiple names for
      // multiple windows and each have their options
      // if (frameName === 'NewWindowComponent ') {
      event.preventDefault();
      Object.assign(options, {
        // This will prevent interactions with the mainWindow
        // parent: mainWindow,
        width: 500,
        height: 600,
        // You can also set `left` and `top` positions
      });
      event.newGuest = new BrowserWindow(options);
      // }
    });
}

const stateList = [
  {
    label: 'offline',
    state: 100,
    subState: 0,
  }, {
    label: 'acceptable',
    state: 101,
    subState: 0,
  }, {
    label: 'away',
    state: 103,
    subState: 0,
    submenu: [
      {
        label: 'acceptableaaaa',
        state: 103,
        subState: 3,
      },
      {
        label: 'acceptablebbbbb',
        state: 103,
        subState: 4,
      }
    ]
  }
]

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
let tray = null
app.whenReady().then(() => {
  createWindow()
  mainWindow.webContents.on('did-finish-load', () => {
    mainWindow.webContents.send('ping', deeplinkingUrl)
  })

  if (!process.argv.includes('--hidden')) {
    mainWindow.show();
  }
  app.on('activate', function () {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
  const trayIconUrl = isDev ? path.join(__dirname, '../public/logo192.png') : path.join(__dirname, '../logo192.png')
  tray = new Tray(trayIconUrl)

  const trayMenuTemplate = [
    {
      label: 'quit app',
      click: function () {
        app.isQuiting = true
        app.quit()
      }
    },
    {
      label: 'change state',
      submenu: stateList.map(state => {
        if (!state.submenu) {
          state.click = () => handleChangeStatus({ state: state.state, subState: state.subState })
        } else {
          state.submenu = state.submenu.map(subState => {
            subState.click = () => handleChangeStatus({ state: subState.state, subState: subState.subState })
            return subState
          })
        }
        return state
      })
    },
  ]

  let trayMenu = Menu.buildFromTemplate(trayMenuTemplate)
  tray.setToolTip('This is my application.')
  tray.setContextMenu(trayMenu)
  tray.setImage(path.join(__dirname, '../src/asset/delete.png'))
  tray.on('click', () => {
    mainWindow.show()
  })


  // notification

  ipcMain.on('open-app', (event, arg) => {
    console.log('new-call')
    mainWindow.show()
  })


  function handleChangeStatus(t) {
    // TODO send status to renderer process
    
    console.log(t)

    // TODO change system tray icon
  }

})

// Quit when fll windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('will-finish-launching', function () {
  // Protocol handler for osx
  app.on('open-url', function (event, url) {
    event.preventDefault()
    deeplinkingUrl = url
    logEverywhere('open-url# ' + deeplinkingUrl);

  })
})

function logEverywhere(s) {
  console.log(s)
  if (mainWindow && mainWindow.webContents) {
    mainWindow.webContents.executeJavaScript(`console.log("${s}")`)
  }
}


app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit()
})

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.