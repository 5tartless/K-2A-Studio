const { app, BrowserWindow, Menu} = require('electron')
const path = require('path')

//completely destroys the default application menu that electron provides
const createWindow = () => {
    const window = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js')
        }
    })

    const menu = Menu.buildFromTemplate([
        {
            label: 'View',
            submenu: [
                {
                    click: () => window.webContents.send('view:toggle-chat'),
                    label: 'Toggle Chat',
                    accelerator: 'CommandOrControl+Alt+C'
                }
            ]
        }
    ])
    Menu.setApplicationMenu(menu)

    window.webContents.on('before-input-event', (event, input) => {
        if (input.type === 'keyDown' && input.key === 'F12') {
            window.webContents.toggleDevTools()
            event.preventDefault()
        }

        if (input.type === 'keyDown' && input.control && input.key.toLowerCase() === 'r') {
            window.webContents.reload()
            event.preventDefault()
        }
    })

    if (process.env.VITE_DEV_SERVER_URL) {
        window.loadURL(process.env.VITE_DEV_SERVER_URL)
    } else {
        console.log("ERROR LOADING VITE -> REACT")
        // window.loadFile('../index.html')
    }
}
app.whenReady().then(() => {
    createWindow()
})

app.on("window-all-closed", () => {
    if (process.platform !== 'darwin') {
        app.quit()
    }
})

app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow()
    }
})