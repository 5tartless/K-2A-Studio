import react from "react";

export default function ActionButton ({text, clicked}) {
    return (
        <button className="menu-button" onClick={clicked}>
            {text}
        </button>
    )
}