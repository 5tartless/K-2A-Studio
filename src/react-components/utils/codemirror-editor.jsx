import react from "react";
import { EditorState, StateEffect } from "@codemirror/state";
//languages
import { javascript } from "@codemirror/lang-javascript";


//anything else
import { 
    EditorView, keymap, lineNumbers,
    highlightSpecialChars, drawSelection, highlightActiveLine,
    dropCursor, rectangularSelection, crosshairCursor,
    highlightActiveLineGutter
} from "@codemirror/view";
import { 
    defaultKeymap, history, historyKeymap,
    indentWithTab

} from "@codemirror/commands";
import { 
    defaultHighlightStyle, syntaxHighlighting, indentOnInput,
    bracketMatching, foldGutter, foldKeymap 
} from "@codemirror/language";
import {
    searchKeymap, highlightSelectionMatches
} from "@codemirror/search"
import { 
    autocompletion, completionKeymap, closeBrackets, closeBracketsKeymap
} from "@codemirror/autocomplete";
import { lintKeymap } from "@codemirror/lint";

export default function newCodeMirror ({ parent, onChange }) {
    const startState = EditorState.create({
        doc: "",
        extensions: [
            //live save
            EditorView.updateListener.of((update) => {
                if (update.docChanged) {
                    onChange(update.state.doc.toString())
                }
            }),
            //language toggle
            javascript(),

            lineNumbers(),
            foldGutter(),
            highlightSpecialChars(),
            history(),
            drawSelection(),
            dropCursor(), 
            indentOnInput(), 
            syntaxHighlighting(defaultHighlightStyle),
            bracketMatching(), 
            closeBrackets(), 
            autocompletion(),
            rectangularSelection(),
            // crosshairCursor(),
            highlightActiveLine(),
            highlightActiveLineGutter(),
            highlightSelectionMatches(),
            keymap.of([
                defaultKeymap, 
                historyKeymap,
                closeBracketsKeymap,
                searchKeymap,
                foldKeymap,
                completionKeymap,
                lintKeymap,
                indentWithTab
            ])
        ]
    })

    let view = new EditorView({
        state: startState,
        parent,
    })
    return view
}