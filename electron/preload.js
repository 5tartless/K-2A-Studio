const { contextBridge } = require('electron')

contextBridge.exposeInMainWorld("test", () => console.log("it works!"))