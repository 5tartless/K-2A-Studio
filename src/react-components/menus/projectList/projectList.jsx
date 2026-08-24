import react, { version } from "react";
import MenuHeader from "../../layouts/menu-header";
import ActionButton from "../../utils/actionButton";
import SearchBar from "../../utils/searchBar";

function Project ({name, path, version}) {
    return (
        <li className="project">
            <div className="project-details">
                <span className="project-name">{name}</span>
                <span className="project-path">Path: {path}</span>
                <span className="project-version">Version: {version}</span>
            </div>
            <ActionButton text='Edit'/>
        </li>
    )
}

export default function ProjectList() {
    // to delete in the future this is only an example:
    const projects = [
        {name: 'K2A-Studio', path: '~/projects/k2a', version: '0.14.1'},
        {name: 'WebProject', path: '~/web-app', version: '2.1'}
    ]
    const projectsElements = projects.map(
        (proj, index) => <Project key={index} name={proj.name} path={proj.path} version={proj.version}/>
    )
    return (
        <>
            <SearchBar placeholderText='Find a project'/>
            <div className="project-list-container">
                <ul className="project-list">
                    {projectsElements}
                </ul>
            </div>
        </>
    )
}