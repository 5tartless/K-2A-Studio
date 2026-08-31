import react from "react"
import ActionLine from "../../utils/actionLine"
import Splitter from "../../utils/spliter"

export default function Chat() {
    return (
        <div className="chat-container">
            <div className="chat-scroll">
                <ChatMessage message={
                    'what? wosa this works so good that i think its just better than k2a-python'
                } mType="right"/>
                <ChatMessage message={
                    'what? wosa this works so good that i think its just better than k2a-python'
                } mType="left"/>
            </div>
            <Splitter/>
        </div>
    )
}

export function ChatMessage ({message, mType = 'right'}) {
    return (
        <div className={`chat-message chat-message-${mType}`}>{message}</div>
    )
}