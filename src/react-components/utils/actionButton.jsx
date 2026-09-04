import react from "react";

export default function ActionButton ({text, onClick}) {
    return (
        <button className="menu-button" onClick={onClick}>
            {text}
        </button>
    )
}