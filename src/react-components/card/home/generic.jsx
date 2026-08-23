import react from "react";
import ActionButton from "../../utils/actionButton";

export default function Card ({title, description, inputComp, actionComp}) {
    return (
        <div className="card">
            <h3 className="card-title">{title}</h3>
            <div className="card-info">{description}</div>
            {inputComp}
            {actionComp}
        </div>
    )
}