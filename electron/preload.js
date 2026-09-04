const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld("electronAPI", {
    onToggleChat: (callback) =>  ipcRenderer.on('view:toggle-chat', (_event) => callback()),

})