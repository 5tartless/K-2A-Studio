import { useRef, useEffect, useState } from "react";
import '../../../style/editor/editor.css'

import ActionLine from "../../utils/actionLine";
import ActionButton from "../../utils/actionButton";
import { Chat, ChatMessage } from "./chat";
import { TabBar, Tab } from "./tabBar";

import newCodeMirror from "../../utils/code-editor";

function Prompt ({ onSend }) {
    const [ field, setField ] = useState("")
    const textAreaRef = useRef(null)

    useEffect(() => {
        const textArea = textAreaRef.current
        const textAreaStyle = window.getComputedStyle(textArea)
        const maxHeight = parseInt(textAreaStyle.maxHeight, 10) 
        
        
        if (textArea.scrollHeight >= maxHeight) {
            textArea.style.height = maxHeight
            textArea.classList.add('input-max')

        } else {
            textArea.classList.remove('input-max')
            if (textArea.scrollHeight === textArea.clientHeight) {
                textArea.style.height = "0px"
                textArea.style.height = `${textArea.scrollHeight}px`
            
            } else {
                textArea.style.height = `${textArea.scrollHeight}px`
            }
        }

    }, [field])

    return (
        <div className="prompt-container">
            <textarea
                className="prompt-input" rows='1' placeholder="Enter a message..."
                ref={textAreaRef} onChange={change => {
                    setField(change.currentTarget.value)
                }}
                onKeyDown={(event => {
                    if (event.key === 'Enter') {
                        if (event.shiftKey) { 
                            return                                  //add new line
                        } else {
                            event.preventDefault()                  //prevent new line
                            if (field.trim().length > 0) {
                                onSend(field)                       //send if text
                                event.currentTarget.value = ''      //reset value
                                setField(event.currentTarget.value) //ensure react notices
                            } 
                        }
                    }
                })}
            />  
            <div className="prompt-actions">
                <ActionButton text={'Send'} onClick={() => {
                    if (field.trim().length > 0 ) onSend(field)
                }}/>
            </div>
        </div>
    )
}

export default function Editor () {
    const spawnedRef = useRef(false)
    const [ tabs, setTabs ] = useState([
        {id: 1, title: "app.py",  code: ''},
        {id: 2, title: "main.js", code: ''},
        {id: 3, title: "app.py",  code: ''},
        {id: 4, title: "main.js", code: ''},
        {id: 5, title: "app.py",  code: ''},
        {id: 6, title: "main.js", code: ''}
    ])
    const [ selectedTab, setSelectedTab ] = useState(-1)
    const selectedTabRef = useRef(-1)

    const [ containerRef, editorViewRef ] = newCodeMirror({
        initialDoc: '',
        onChange: state => {
            if (selectedTabRef.current === -1) return
            
            setTabs(prev => {
                const newVal = prev.map(value => {
                    if (selectedTabRef.current === value.id)
                        return {...value, code: state.doc.toString()}
                    return value
                })
                return newVal
            })
        }
    })

    useEffect(() => { //ensure there is only 1 editor view
        return () => {
            if (editorViewRef.current) {
                editorViewRef.current.destroy()
            }
        }
    }, [])
    
    const [ chatVisible, setChatVisible ] = useState(false)
    const [ messages, setMessages ] = useState([])
    useEffect(() => {
        if (!spawnedRef.current) {
            window.electronAPI.onToggleChat(() => {
                setChatVisible(prev => !prev)
            })
            spawnedRef.current = true
        }
    }, [])
    const chatOnSend = userPrompt => {
        setMessages(prev => [
            ...prev,
            userPrompt
        ])
    }

    
    useEffect(() => {
        if (selectedTab === -1) {
            containerRef.current.classList.add('hidden')
        }
        else {
            const tabInfo = tabs.filter(value => {
                return selectedTab === value.id
            })[0]
            const view = editorViewRef.current
            view.dispatch({
                changes: {
                    from: 0, to: view.state.doc.length,
                    insert: tabInfo.code
                }
            })
            containerRef.current.classList.remove('hidden')
        }
        selectedTabRef.current = selectedTab
    }, [selectedTab])

    useEffect(() => {
        console.log(tabs)
    }, [tabs])

    return (
        <>
            <div className="main-container">
                {
                    chatVisible && <div className="left">
                        <ActionLine title='CHAT'/>
                        <Chat messages={messages}/>
                        <Prompt onSend={chatOnSend}/>
                    </div>
                }
                <div className="center">
                    <TabBar 
                        tabs={tabs}
                        onTabClose={tabs => setTabs(tabs)}
                        selectedTab={selectedTab}
                        onTabSelect={id => setSelectedTab(id)}
                    />
                    <div className="editor">
                        <div ref={containerRef} className="code-mirror"/>
                    </div>
                </div>
                <div className="right">

                </div>
            </div>
        </>
    )
}