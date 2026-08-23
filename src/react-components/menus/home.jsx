import react from "react";
import MenuHeader from "../layouts/menu-header";
import HomeCard from "../card/home/generic";

export default function Home() {
    return (
       <div className="main-welcome">
            <div className="main-welcome">
                <span>Welcome to K2A Studio</span><br/>
                <span>An application ready for you to manage your projects as you please.</span>
            </div>
            <div className="card-view">
                <HomeCard type='import' to='/import' title='Import'/>
                <HomeCard type='create' to='/create' title='Create'/>
            </div>
        </div>
    )
}