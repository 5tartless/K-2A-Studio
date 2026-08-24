import "@fontsource/jetbrains-mono/400.css"
import "@fontsource/jetbrains-mono/700.css"
import "./style/index.css"

import React from "react";
import { createRoot } from "react-dom/client";
import App from "./react-components/app";

const root = createRoot(document.getElementById('root'))
root.render(
    <React.StrictMode>
        <App/>
        {/* <h1>{test()}</h1> */}
    </React.StrictMode>
)
