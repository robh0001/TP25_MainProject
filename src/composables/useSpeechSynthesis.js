import { computed, onMounted, ref } from 'vue'

const isSupported = ref(false)
const isSpeaking = ref(false)
const isPaused = ref(false)
const voices = ref([])
const selectedVoiceURI = ref('')
const selectedLanguage = ref('en-AU')
const errorMessage = ref('')

function getSpeechSynthesis() {
  if (typeof window === 'undefined') return null
  return window.speechSynthesis || null
}

function loadVoices() {
  const speechSynthesis = getSpeechSynthesis()

  if (!speechSynthesis) {
    isSupported.value = false
    return
  }

  const availableVoices = speechSynthesis.getVoices()

  voices.value = availableVoices

  if (!selectedVoiceURI.value && availableVoices.length > 0) {
    const preferredVoice =
      availableVoices.find((voice) => voice.lang === selectedLanguage.value) ||
      availableVoices.find((voice) => voice.lang.startsWith('en')) ||
      availableVoices[0]

    if (preferredVoice) {
      selectedVoiceURI.value = preferredVoice.voiceURI
      selectedLanguage.value = preferredVoice.lang
    }
  }
}

export function useSpeechSynthesis() {
  const selectedVoice = computed(() => {
    return voices.value.find((voice) => voice.voiceURI === selectedVoiceURI.value) || null
  })

  const languageVoices = computed(() => {
    return voices.value.filter((voice) => voice.lang.startsWith(selectedLanguage.value.split('-')[0]))
  })

  function initialiseSpeech() {
    const speechSynthesis = getSpeechSynthesis()

    if (!speechSynthesis || typeof SpeechSynthesisUtterance === 'undefined') {
      isSupported.value = false
      errorMessage.value = 'Speech is not supported in this browser.'
      return
    }

    isSupported.value = true
    errorMessage.value = ''

    loadVoices()

    speechSynthesis.onvoiceschanged = () => {
      loadVoices()
    }
  }

  function speakText(text, options = {}) {
    const speechSynthesis = getSpeechSynthesis()
  
    if (!speechSynthesis || typeof SpeechSynthesisUtterance === 'undefined') {
      isSupported.value = false
      errorMessage.value = 'Speech is not supported in this browser.'
      return
    }
  
    const cleanText = String(text || '').replace(/\s+/g, ' ').trim()
  
    if (!cleanText) {
      errorMessage.value = 'No text available to read.'
      return
    }
  
    speechSynthesis.cancel()
  
    const utterance = new SpeechSynthesisUtterance(cleanText)
  
    utterance.lang = options.lang || selectedLanguage.value || 'en-AU'
    utterance.rate = options.rate || 0.95
    utterance.pitch = options.pitch || 1
    utterance.volume = options.volume || 1
  
    if (selectedVoice.value) {
      utterance.voice = selectedVoice.value
      utterance.lang = selectedVoice.value.lang
    }
  
    utterance.onstart = () => {
      isSpeaking.value = true
      isPaused.value = false
      errorMessage.value = ''
    }
  
    utterance.onend = () => {
      isSpeaking.value = false
      isPaused.value = false
    }
  
    utterance.onerror = (event) => {
      isSpeaking.value = false
      isPaused.value = false
  
      if (event.error !== 'interrupted' && event.error !== 'canceled') {
        errorMessage.value = `Speech error: ${event.error}`
      }
    }
  
    speechSynthesis.speak(utterance)
  }

  function stopSpeech() {
    const speechSynthesis = getSpeechSynthesis()

    if (!speechSynthesis) return

    speechSynthesis.cancel()
    isSpeaking.value = false
    isPaused.value = false
  }

  function pauseSpeech() {
    const speechSynthesis = getSpeechSynthesis()

    if (!speechSynthesis || !speechSynthesis.speaking) return

    speechSynthesis.pause()
    isPaused.value = true
  }

  function resumeSpeech() {
    const speechSynthesis = getSpeechSynthesis()

    if (!speechSynthesis || !speechSynthesis.paused) return

    speechSynthesis.resume()
    isPaused.value = false
  }

  function updateSelectedVoice(voiceURI) {
    selectedVoiceURI.value = voiceURI

    const voice = voices.value.find((item) => item.voiceURI === voiceURI)

    if (voice) {
      selectedLanguage.value = voice.lang
    }
  }

  function updateSelectedLanguage(language) {
    selectedLanguage.value = language

    const matchingVoice =
      voices.value.find((voice) => voice.lang === language) ||
      voices.value.find((voice) => voice.lang.startsWith(language.split('-')[0]))

    if (matchingVoice) {
      selectedVoiceURI.value = matchingVoice.voiceURI
    }
  }

  onMounted(() => {
    initialiseSpeech()
  })

  return {
    isSupported,
    isSpeaking,
    isPaused,
    voices,
    selectedVoiceURI,
    selectedLanguage,
    selectedVoice,
    languageVoices,
    errorMessage,
    initialiseSpeech,
    speakText,
    stopSpeech,
    pauseSpeech,
    resumeSpeech,
    updateSelectedVoice,
    updateSelectedLanguage,
  }
}