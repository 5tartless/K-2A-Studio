import react from "react";
import { Link } from "react-router-dom";

export default function LinkButton({title, to}) {
    return (
        <Link to={to} className="menu-button">
            {title}
        </Link>
    )
}