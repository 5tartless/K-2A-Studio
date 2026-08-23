import react from "react";
import Card from "../../card/home/generic";
import InputArea from "../../utils/inputArea";
import ActionButton from "../../utils/actionButton";

function FrameworkDescription () {
    return (
        <p>
            Search for your desired framework. If it doesn't appear here,
            dont worry; you could manually add it later.
        </p>
    )
}

function CreateInputs () {
    return (
        <div className="create-inputs">
            <InputArea labelText='Project Name:' placeholderText='Let the inspiration come in...'/>
            <div className="create-input-container">
                <InputArea labelText='Path:' placeholderText='~/Projects/...'/>
                <ActionButton text='Browse Path'/>
            </div>
            <hr/>

            <Card
                title='Framework'
                description={<FrameworkDescription/>}
            />

            <hr />            
            <div className="create-input-container">
                <InputArea labelText='README:'/>
                <ActionButton text='Browse README'/>
            </div>
        </div>
    )
}

function CreateActions () {
    return (
        <div className="create-action-container">
            <ActionButton text='Create'/>
            <ActionButton text='Cancel'/>
        </div>
    )
}

export default function Create () {
    return (
        <div className="card-view">
            <Card 
                title='Create Project'
                inputComp={<CreateInputs/>}
                actionComp={<CreateActions/>}
            />
        </div>
    )
}