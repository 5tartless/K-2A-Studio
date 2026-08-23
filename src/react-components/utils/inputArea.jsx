import react from "react";

export default function InputArea({labelText, inputType='text', placeholderText}) {
    return (
        <div className="input-area">
            <label>{labelText}</label>
            <input type={inputType} placeholder={placeholderText}/>
        </div>
    )
}