import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import electron from 'vite-plugin-electron'

export default defineConfig({
    plugins: [
        react(),
        electron({
            entry: 'electron/index.js',
            vite: {
                build: {
                    watch: {
                        exclude: ['src/**/*', 'index.html']
                    }
                }
            }
        })
    ]
})
