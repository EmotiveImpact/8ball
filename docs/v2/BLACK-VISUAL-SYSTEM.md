# Black operator visual system

Scope: an implementation of the owner's requested black direction in the existing V0.2 application, not a separate concept render.

Use `#08090b` for the canvas, `#111216` for primary surfaces, `#1b1d22` for raised controls, `#2b2e35` for structural borders, `#f2f3f5` for primary text and `#a9adb7` for secondary text. Primary controls use white with near-black labels. Green, amber and red are reserved for labelled evidence/approval/risk states rather than large decorative surfaces. Conditional plans are neutral, not displayed as successful outcomes.

Maintain the target banner, operational map, Now rail, questions, decisions and route comparison. Distinguish nodes through both labels and styling. Preserve escaped content, keyboard focus, dialog containment, mobile viewport behaviour and a visible workspace lock. The Intelligence page separates ENDSTATE (always available for deterministic work), local Ollama state and optional hosted configuration.

The local visual checks render actual source with the real API/SQLite through the existing explicit ASGI bridge. They do not establish native HTTP, downloads or cross-browser/accessibility acceptance. Current native CI is pending because the code could not be pushed. The full B02-16 accessibility scope remains incomplete.

The relationship explorer extends these tokens with a quiet near-black graph canvas, framed tools and a right-hand evidence inspector. Muted colours distinguish labelled record types; explicit state labels and shapes are always available. It avoids continuous decorative motion, fabricated connection strengths and data-like elements without case backing. See `GRAPH-EXPLORER.md`.
