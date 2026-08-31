import { useEffect, useState, useRef } from "react"

export default function Splitter ({ left = true }) {
    const [ isDragging, setIsDragging ] = useState(false)
    const splitterRef = useRef(null)

    useEffect(() => {
        const handleMouseMove = (e) => {
            if (!isDragging) return
            const splitter = splitterRef.current

            const parent = splitter.parentElement.parentElement
            const rect = parent.getBoundingClientRect()

            const newWidth = left
                ? e.clientX - rect.left
                : rect.right - e.clientX
            parent.style.width = `${newWidth}px`
        }
        const handleMouseUp = () => setIsDragging(false)

        document.addEventListener("mousemove", handleMouseMove)
        document.addEventListener("mouseup", handleMouseUp)

        return () => {
            document.removeEventListener("mousemove", handleMouseMove)
            document.removeEventListener("mouseup", handleMouseUp)
        }

    }, [isDragging])

    const splitter = <div 
        className="splitter"
        ref={splitterRef}
        onMouseDown={
            () => setIsDragging(true)
        }
    ></div>

    return splitter
}