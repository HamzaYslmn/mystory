import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { applySettingsToDOM, useSettingsStore } from '@/store/settings'
// MARK: - Self-hosted Comic Neue Bold (SIL OFL).
// Open-source Comic Sans alternative; bold (700) is the default weight for the
// 'Playful' font so every device renders identically.
import '@fontsource/comic-neue/700.css'
import '@fontsource/comic-neue/700-italic.css'
import '@/index.css'
import App from '@/App.tsx'

// MARK: - Apply persisted settings to DOM at startup
applySettingsToDOM(useSettingsStore.getState());

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
