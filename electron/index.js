const { app, BrowserWindow, Menu } = require('electron')
const path = require('path')

//completely destroys the default application menu that electron provides
Menu.setApplicationMenu(null)
const createWindow = () => {
    const window = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js')
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