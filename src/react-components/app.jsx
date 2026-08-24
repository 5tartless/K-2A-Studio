import React from "react";
import { HashRouter, Routes, Route, Link } from "react-router-dom";
import ProjectList from "./menus/projectList/projectList";
import Home from "./menus/home/menu";
import Import from "./menus/home/import";
import Create from "./menus/home/create";

import MenuHeader from "./layouts/menu-header";
export default function App() {
    return (
        <HashRouter>
            <MenuHeader/>
            <main>
                <Routes>
                    <Route path="/" element={<Home/>}/>
                    <Route path="/import" element={<Import/>}/>
                    <Route path="/create" element={<Create/>}/>

                    <Route path="/project-list" element={<ProjectList/>}/>
                    {/* <Route path="/settings" element={<Settings/>} /> */}
                </Routes>
            </main>
        </HashRouter>
    )
}