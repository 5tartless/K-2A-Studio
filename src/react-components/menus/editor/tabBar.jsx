import { useEffect, useState } from "react";
import ActionButton from "../../utils/actionButton";

export function Tab ({ title, selected, onSelect, onClose }) {
    return (
        <div className={`tab ${selected && 'tab-selected'}`} onClick={onSelect}>
            <i className="tab-icon"></i>
            <span className="tab-title">{title}</span>
            <ActionButton text={'X'} onClick={onClose}/>
        </div>
    )
}

export function TabBar ({ tabs, onTabClose, selectedTab, onTabSelect }) {
    
    const [tabSelectHistory, setTabSelectHistory] = useState([])
    const onTabSelected = id => {
        onTabSelect(id)
        if ( tabSelectHistory.includes(id) ) {
            setTabSelectHistory([
                ...tabSelectHistory.filter(value => value !== id), id
            ])
        } else setTabSelectHistory([...tabSelectHistory, id])
    }
    const onTabClosed = (event, id) => {
        if (selectedTab === id) {                                 //puts the user into another tab if on it
            onTabSelect(
                tabs.length > 1 && tabSelectHistory.length > 1
                ? tabSelectHistory.slice(-2, -1)[0]
                : -1
            )
        }
        onTabClose(tabs.filter(value => value.id !== id)) //kills the tab
        setTabSelectHistory(tabSelectHistory.filter(value => value !== id)) //removes tab from history

        event.stopPropagation()
    }

    return (
        <div className="tab-bar">
            {
                tabs.map(
                    (value) => <Tab 
                        key={value.id}
                        selected={selectedTab === value.id}
                        title={value.title}
                        onSelect={() => {onTabSelected(value.id)}}
                        onClose={(event) => {onTabClosed(event, value.id)}}
                    />
                )
            }
        </div>
    )
}