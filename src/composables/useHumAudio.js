import { computed, ref, shallowRef } from "vue"

/** Autocorrelation pitch estimate (child-ish hum range ~100-700 Hz typical). */
function estimatePitchHz(floatBuf, sampleRate) {
  const SIZE = floatBuf.length
  let rms = 0
  for (let i = 0; i < SIZE; i++) rms += floatBuf[i] * floatBuf[i]
  rms = Math.sqrt(rms / SIZE)
  if (rms < 0.012) return -1

  const thres = 0.2
  let r1 = 0
  for (let i = 0; i < SIZE / 2; i++) {
    if (Math.abs(floatBuf[i]) < thres) {
      r1 = i
      break
    }
  }
  let r2 = SIZE - 1
  for (let i = 1; i < SIZE / 2; i++) {
    if (Math.abs(floatBuf[SIZE - i]) < thres) {
      r2 = SIZE - i
      break
    }
  }

  const trimmed = floatBuf.slice(r1, r2)
  const n = trimmed.length
  if (n < 256) return -1

  const c = new Float32Array(n)
  for (let i = 0; i < n; i++) {
    let s = 0
    for (let j = 0; j < n - i; j++) s += trimmed[j] * trimmed[j + i]
    c[i] = s
  }

  let d = 0
  while (d + 2 < c.length && c[d] > c[d + 1]) d++

  let max = -1
  let maxPos = -1
  for (let i = d; i < n; i++) {
    if (c[i] > max) {
      max = c[i]
      maxPos = i
    }
  }

  const T0 = maxPos
  if (T0 <= 0) return -1
  const f = sampleRate / T0
  if (f < 90 || f > 1400) return -1
  return f
}

function clamp01(v) {
  return Math.min(1, Math.max(0, v))
}

/**
 * Microphone -> pitch / volume / simple hum classification for Hum It! web prototype.
 */
export function useHumAudio() {
  const supported = ref(
    typeof navigator !== "undefined" && Boolean(navigator.mediaDevices?.getUserMedia),
  )
  const status = ref("idle") // idle | requesting | live | error
  const errorMessage = ref("")

  const pitchHz = ref(0)
  const volume = ref(0)
  const pitchNorm = ref(0.5)
  const humStable = ref(true)
  const continuousHumMs = ref(0)

  /** Demo overrides when mic unavailable - pitch 0-1, vol 0-1 */
  const demoPitch = ref(0.45)
  const demoVolume = ref(0)

  let audioCtx = null
  let analyser = null
  let stream = null
  let rafId = 0
  const timeBuf = shallowRef(new Float32Array(2048))

  let smoothPitch = 220
  let smoothVol = 0
  let baselinePitch = 260
  let pitchVarianceAcc = 0
  let varianceN = 0
  let humMs = 0
  let silentMs = 0
  let lastTs = 0

  const isLive = computed(() => status.value === "live")

  function resetDynamics() {
    smoothPitch = 220
    smoothVol = 0
    baselinePitch = 260
    pitchVarianceAcc = 0
    varianceN = 0
    humMs = 0
    silentMs = 0
    lastTs = 0
  }

  function tick(ts) {
    if (status.value !== "live" || !analyser || !audioCtx) return

    const dt = lastTs ? Math.min(64, ts - lastTs) : 16
    lastTs = ts

    analyser.getFloatTimeDomainData(timeBuf.value)

    let rms = 0
    for (let i = 0; i < timeBuf.value.length; i++) rms += timeBuf.value[i] * timeBuf.value[i]
    rms = Math.sqrt(rms / timeBuf.value.length)

    const f = estimatePitchHz(timeBuf.value, audioCtx.sampleRate)
    const vRaw = Math.min(1, rms * 4.2)

    const alpha = 0.22
    smoothVol = smoothVol * (1 - alpha) + vRaw * alpha

    if (f > 0) {
      smoothPitch = smoothPitch * (1 - alpha) + f * alpha
      baselinePitch = baselinePitch * 0.998 + smoothPitch * 0.002
      const dev = Math.abs(smoothPitch - baselinePitch)
      pitchVarianceAcc += dev
      varianceN += 1
    }

    const humming = smoothVol > 0.035
    if (humming) {
      humMs += dt
      silentMs = 0
      continuousHumMs.value = humMs
    } else {
      silentMs += dt
      humMs = 0
      continuousHumMs.value = 0
    }

    const varAvg = varianceN > 8 ? pitchVarianceAcc / varianceN : 0
    humStable.value = varAvg < 18

    pitchHz.value = f > 0 ? Math.round(smoothPitch) : 0
    volume.value = smoothVol

    const normFromFreq = clamp01((smoothPitch - 140) / (620 - 140))
    pitchNorm.value = normFromFreq

    rafId = requestAnimationFrame(tick)
  }

  async function start() {
    errorMessage.value = ""
    if (!supported.value) {
      status.value = "error"
      errorMessage.value = "Microphone not supported in this browser."
      return
    }
    resetDynamics()
    status.value = "requesting"
    try {
      stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        },
      })
      audioCtx = new AudioContext()
      const src = audioCtx.createMediaStreamSource(stream)
      analyser = audioCtx.createAnalyser()
      analyser.fftSize = 2048
      src.connect(analyser)
      status.value = "live"
      lastTs = 0
      rafId = requestAnimationFrame(tick)
    } catch (e) {
      status.value = "error"
      errorMessage.value =
        e?.name === "NotAllowedError"
          ? "Microphone permission denied. Use demo sliders below or enable the mic in browser settings."
          : "Could not open microphone."
    }
  }

  function stop() {
    if (rafId) cancelAnimationFrame(rafId)
    rafId = 0
    if (stream) {
      stream.getTracks().forEach(t => t.stop())
      stream = null
    }
    if (audioCtx) {
      audioCtx.close().catch(() => {})
      audioCtx = null
    }
    analyser = null
    status.value = "idle"
    pitchHz.value = 0
    volume.value = 0
    pitchNorm.value = 0.5
    continuousHumMs.value = 0
  }

  /** Effective pitch norm - mic live uses detection; else demo slider */
  function effectivePitchNorm() {
    return status.value === "live" ? pitchNorm.value : clamp01(demoPitch.value)
  }

  /** Effective volume */
  function effectiveVolume() {
    return status.value === "live" ? volume.value : clamp01(demoVolume.value)
  }

  return {
    supported,
    status,
    errorMessage,
    isLive,
    pitchHz,
    volume,
    pitchNorm,
    humStable,
    continuousHumMs,
    demoPitch,
    demoVolume,
    start,
    stop,
    effectivePitchNorm,
    effectiveVolume,
  }
}
