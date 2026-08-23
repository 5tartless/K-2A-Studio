import react from "react";
import MenuHeader from "../../layouts/menu-header";
import Card from "../../card/home/generic";
import InputArea from "../../utils/inputArea";
import ActionButton from "../../utils/actionButton";

function LocalImportDesc() {
    return (
        <p>
            Browse your local files and find your main project root directory folder.
        </p>
    )
}

export default function Import () {
    return (
       <div>
            <div className="main-welcome">
                <span>Import a project</span><br/>
                <span>With this next step empower your project with AI Assistance</span>
            </div>
            <div className="card-view">
                <Card 
                    title='Import from github'
                    inputComp={
                        <InputArea
                            labelText='Repository URL:'
                            placeholderText='https://github.com/user/repo'
                        />
                    }
                    actionComp={
                        <ActionButton text='Confirm and Import'/>
                    }
                />
                <Card
                    title='Import from you computer'
                    description={<LocalImportDesc/>}
                    actionComp={
                        <ActionButton text='Browse'/>
                    }
                />
            </div>
        </div>
    )
}