import { useEffect, useRef } from "react"
import ActionLine from "../../utils/actionLine"
import Splitter from "../../utils/spliter"

export function Chat ({ messages }) {
    const scrollRef = useRef(null)
    useEffect(() => { //fires everytime a new message is thrown
        if (!scrollRef) return

        const scroll = scrollRef.current
        scroll.scrollTop = scroll.scrollHeight        
    }, [messages])

    return (
        <div className="chat-container">
            <div ref={scrollRef} className="chat-scroll">
                {
                    messages.map(
                        (value, index) => <ChatMessage key={index} message={value} mType="right"/>
                    )
                }
            </div>
            <Splitter left={true}/>
        </div>
    )
}

export function ChatMessage ({ message, mType = 'right' }) {
    return (
        <div className={`chat-message chat-message-${mType}`}>{message}</div>
    )
}
