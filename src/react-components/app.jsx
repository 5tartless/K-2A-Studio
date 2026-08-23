import React from "react";
import { HashRouter, Routes, Route, Link } from "react-router-dom";
import ProjectList from "./menus/projectList";
import Home from "./menus/home";


import MenuHeader from "./layouts/menu-header";
export default function App() {
    return (
        <HashRouter>
            <MenuHeader/>
            <main>
                <Routes>
                    <Route path="/" element={<Home/>}/>
                    <Route path="/project-list" element={<ProjectList/>}/>
                    {/* <Route path="/settings" element={<Settings/>} /> */}
                </Routes>
            </main>
        </HashRouter>
    )
}