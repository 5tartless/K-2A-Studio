import { useRef, useEffect, useState } from "react";
import '../../../style/editor/editor.css'

import ActionLine from "../../utils/actionLine";
import ActionButton from "../../utils/actionButton";
import Chat from "./chat";

import newCodeMirror from "../../utils/codemirror-editor";

function Prompt () {
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
                ref={textAreaRef} onChange={(change) => {
                    setField(change.currentTarget.value)
                }}
            />  
            <div className="prompt-actions">
                <ActionLine/>
                <ActionButton text={'Send'}/>
            </div>
        </div>
    )
}

export default function Editor () {
    const containerRef = useRef(null)
    const spawnedRef = useRef(false)
    const [ code, setCode ] = useState("")
    const [ chatVisible, setChatVisible ] = useState(true)

    useEffect(() => {
        if (!containerRef.current) return
        let codeMirror = newCodeMirror({ 
            parent: containerRef.current,
            onChange: (content) => {
                setCode(content)
            }
        })
        containerRef.current = codeMirror

        return () => {
            codeMirror.destroy()
        }
    }, [])

    useEffect(() => {
        if (!spawnedRef.current) {
            window.electronAPI.onToggleChat(() => {
                setChatVisible(prev => !prev)
            })
            spawnedRef.current = true
        }
    }, [])
    // useEffect(() => {
    //     console.log(code)
    // }, [code])
    
    return (
        <>
            <div className="top-container">

            </div>
            <div className="main-container">
                {
                    chatVisible && <div className="left">
                        <ActionLine title='CHAT'/>
                        <Chat/>
                        <Prompt/>
                    </div>
                }
                <div className="editor">
                    <div ref={containerRef} className="code-mirror"/>
                </div>
                <div className="right">

                </div>
            </div>
        </>
    )
}