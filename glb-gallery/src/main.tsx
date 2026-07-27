import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { Gallery } from './Gallery'
import './styles.css'

const rootElement = document.getElementById('root')

if (!rootElement) {
  throw new Error('Root element was not found.')
}

createRoot(rootElement).render(
  <StrictMode>
    <Gallery />
  </StrictMode>,
)
