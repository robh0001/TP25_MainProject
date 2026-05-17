import { onBeforeUnmount, watch } from 'vue'
import { useHoverToRead } from './useHoverToRead'
import { useSpeechSynthesis } from './useSpeechSynthesis'

const READABLE_SELECTOR =
  'p, h1, h2, h3, h4, h5, h6, li, button, a, label, .card, .suggestion-card, [data-hover-read-text]'
const IGNORE_SELECTOR =
  'script, style, svg, path, input, textarea, select, option, [aria-hidden="true"], [data-hover-read-ignore="true"], [data-hover-read-ignore="true"] *'

let listenersAttached = false

export function useHoverSpeechReader() {
  const { isHoverToReadEnabled } = useHoverToRead()
  const { speakText, stopSpeech } = useSpeechSynthesis()

  let lastElement = null

  function getReadableText(element) {
    if (!element) return ''

    const ariaLabel = element.getAttribute('aria-label')
    const text = ariaLabel || element.innerText || element.textContent || ''

    return text.replace(/\s+/g, ' ').trim()
  }

  function isValidReadableTarget(element) {
    if (!element) return false
    if (element.closest(IGNORE_SELECTOR)) return false

    const text = getReadableText(element)

    if (!text || text.length < 2) return false

    if (text.length > 320) return false

    return true
  }

  function handleMouseOver(event) {
    if (!isHoverToReadEnabled.value) return
  
    if (event.target.closest(IGNORE_SELECTOR)) return
  
    const target = event.target.closest(READABLE_SELECTOR)
  
    if (!target || target === lastElement) return
    if (!isValidReadableTarget(target)) return
  
    const text = getReadableText(target)
  
    lastElement = target
    speakText(text)
  }

  function handleMouseOut(event) {
    if (!lastElement) return

    const nextElement = event.relatedTarget

    if (nextElement && lastElement.contains(nextElement)) {
      return
    }

    lastElement = null
  }

  function enableListeners() {
    if (listenersAttached || typeof document === 'undefined') return

    document.addEventListener('mouseover', handleMouseOver)
    document.addEventListener('mouseout', handleMouseOut)

    listenersAttached = true
  }

  function disableListeners() {
    if (typeof document !== 'undefined' && listenersAttached) {
      document.removeEventListener('mouseover', handleMouseOver)
      document.removeEventListener('mouseout', handleMouseOut)
    }

    listenersAttached = false
    lastElement = null
    stopSpeech()
  }

  watch(
    isHoverToReadEnabled,
    (enabled) => {
      if (enabled) {
        enableListeners()
      } else {
        disableListeners()
      }
    },
    { immediate: true }
  )

  onBeforeUnmount(() => {
    disableListeners()
  })
}