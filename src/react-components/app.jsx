import React from "react";
import { HashRouter, Routes, Route, Link } from "react-router-dom";
import Home from "./menus/home/menu";
import Import from "./menus/home/import";
import Create from "./menus/home/create";
import ProjectList from "./menus/projectList/projectList";
import Editor from "./menus/editor/editor";

import MenuHeader from "./layouts/menu-header";
export default function App() {
    return (
        <main>
            <HashRouter>
                <MenuHeader/>
                <Routes>
                    <Route path="/" element={<Home/>}/>
                    <Route path="/import" element={<Import/>}/>
                    <Route path="/create" element={<Create/>}/>

                    <Route path="/project-list" element={<ProjectList/>}/>

                    {/* <Route path="/settings" element={<Settings/>} /> */}
                    
                    <Route path="/editor" element={<Editor/>}/>
                </Routes>
            </HashRouter>
        </main>
    )
}