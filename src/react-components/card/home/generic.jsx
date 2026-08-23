import react from "react";
import MenuButton from "../../utils/linkButton";

export default function HomeCard ({type, title, to}) {
    return (
        <div className="card">
            {/* {type === 'import' && (
                <div className="card-icon">
                    this is import.
                </div>  
            )} */}
            <div className="card-info">
                {type === 'import' ?
                <p>
                    Try importing an existing project from a github repository
                    or from your local computer.
                </p>:
                <p>
                    Create with AI assistance your own project structure that can later
                    be moved into a github repository with just one order.
                </p>}
            </div>
            <MenuButton to={to} title={title}/>
        </div>
    )
}