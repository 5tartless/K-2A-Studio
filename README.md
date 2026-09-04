# K2A-Studio Electron

_Made with **electron, react + vite**._
This is an **EXPERIMENT** entirely developed by `5tartless`.

>_**Note:** If it overcomes in someway or results promising to everyone then pyqt5 will get replaced._

The main idea is to convert **K2A-Studio** into an **Electron App** that links with _Python for AI communication_.

Allowing us to **improve communication between your code and our service**; making the app feel modern and more polished visually.

---

## Current progress

* Current objective: `Catch up` _**`to the main branch.`**_

### Project Editor Part 2 `v0.03.2`

* Added chat features:
  * The user can now send messages
  * Chat auto scrolls down when new message is sent.
  * No Assistant feature for now.

* Changed how code mirror was implemented.
  * Improved code in general.
  * Removed support for javascript (Bug)

* Added tabs:
  * For now there are pre-fabricated tabs just for testing.
  * Each tab contains code information separately.
  * Added new history for tabs.
    * When closing your current tab it relocates you to the latest one open.

---

### Project Editor Part 1 `v0.03.1`

* Added Code Mirror instead of Monaco Editor
**( May change )**
  * Only supports **javascript sintax**
* Added Chat for Ollama Qwen 3:4b
**( Useless for now )**
  * Chat can be expanded sideways.
  * Chat can be toggled with Ctrl+Alt+C, or with the app menu.
