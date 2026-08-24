import react from "react";
import ActionButton from "./actionButton";

export default function SearchBar({placeholderText}) {
    return (
        <div className="search-bar">
            <input type="text" placeholder={placeholderText}/>
            <ActionButton text={<i className="fa fa-search"/>}/>
        </div>
    )
}
