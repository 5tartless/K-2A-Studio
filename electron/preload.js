const { contextBridge } = require('electron')

contextBridge.exposeInMainWorld("test", () => "it works!")