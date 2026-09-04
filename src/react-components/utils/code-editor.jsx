import { useState, useEffect, useRef } from 'react'

import { EditorState } from '@codemirror/state'
import { EditorView, highlightActiveLine, highlightActiveLineGutter, keymap, lineNumbers } from '@codemirror/view'
import { defaultKeymap, historyKeymap, history } from '@codemirror/commands'
import { bracketMatching, defaultHighlightStyle, indentOnInput } from '@codemirror/language'
import { javascript } from '@codemirror/lang-javascript'

export default function newCodeMirror ({ initialDoc, onChange}) {
    const containerRef = useRef(null)
    const editorViewRef = useRef(null)

    useEffect(() => {
        if (!containerRef.current) return
        const startState = EditorState.create({
            doc: initialDoc,
            extensions: [
                EditorView.lineWrapping,
                EditorView.updateListener.of(update => {
                    if (update.changes) {
                        onChange && onChange(update.state)
                    }
                }),
                keymap.of([...defaultKeymap, historyKeymap]),
                lineNumbers(),
                highlightActiveLineGutter(),
                history(),
                indentOnInput(),
                bracketMatching(),
                highlightActiveLine(),
                javascript()
            ]
        })

        const view = new EditorView({
            state: startState,
            parent: containerRef.current
        })
        editorViewRef.current = view
    }, [containerRef])

    return [containerRef, editorViewRef]
}
