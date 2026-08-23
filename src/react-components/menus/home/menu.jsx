import react from "react";
import MenuHeader from "../../layouts/menu-header";
import Card from "../../card/home/generic";
import LinkButton from "../../utils/linkButton";

function ImportInfo () {
    return (
        <p>
            Try importing an existing project from a github repository
            or from your local computer.
        </p>
    )
}

function CreateInfo () {
    return (
        <p>
            Create with AI assistance your own project structure that can later
            be moved into a github repository with just one order.
        </p>
    )
}

export default function Home() {
    return (
       <div>
            <div className="main-welcome">
                <span>Welcome to K2A Studio</span><br/>
                <span>An application ready for you to manage your projects as you please.</span>
            </div>
            <div className="card-view">
                <Card
                    description={<ImportInfo/>} 
                    actionComp={
                        <LinkButton title='Import' to='/import'/>
                    }
                    title='Import'
                />
                <Card
                    description={<CreateInfo/>} 
                    actionComp={
                        <LinkButton title='Create' to='/create'/>
                    }
                    title='Create'
                />
            </div>
        </div>
    )
}