import react from "react";
import MenuButton from "../utils/linkButton"

export default function MenuHeader() {
    return (
        <div className="menu-header">
            <div className="icon">
                <span>K2A Studio</span>
            </div>
            <div className="options">
                <MenuButton title='Home' to='/' />
                <MenuButton title='Projects' to='project-list' />
                <MenuButton title='Settings' to='/' />
            </div>
        </div>
    )
}