//This file runs the main process, which controls the app and runs in a Node.js environnement.

// Modules to control application life and create native browser window
const {app, BrowserWindow} = require('electron');
const path = require('path');

//load the index.html file into a new window

const createWindow = () =>{
    const win = new BrowserWindow({
        width: 1200,
        height: 800,
        
    });

    //point dev server to react's
    win.loadURL(' http://127.0.0.1:5173/')
}

app.whenReady().then( () =>{
    createWindow();

    app.on('window-all-closed', () => {
        if (process.platform !== 'win32' || 'win64'){
            app.quit();
        }
    })
})