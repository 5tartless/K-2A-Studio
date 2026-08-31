import react from "react"

export default function ActionLine({ title, actions }) {
    return (
        <div className="action-line">
            <span className="action-line-title">{title}</span>
            <div className="action-line-content">
                {actions}
            </div>
        </div>
    )
}