import { reactive, ref } from "vue"

const STORAGE_KEY = "humit-ost-muted"

/**
 * Hum It background audio: plays `public/humit-ost.mp3` when that file exists,
 * otherwise a soft Web Audio drone. Starts after a user tap; gain stays low for mic use.
 */
export function useHumItOst() {
  const muted = ref(false)
  try {
    muted.value = localStorage.getItem(STORAGE_KEY) === "1"
  } catch {
    //
  }

  let mode = "off" // 'file' | 'synth' | 'off'
  let audioEl = null
  let ctx = null
  let masterGain = null
  let filterNode = null
  let synthNodes = []
  let animId = 0

  let reactPitch = 0.5
  let reactVol = 0

  const baseSynthGain = 0.052

  function persistMute() {
    try {
      localStorage.setItem(STORAGE_KEY, muted.value ? "1" : "0")
    } catch {
      //
    }
  }

  function applyMute() {
    const m = muted.value
    if (audioEl) {
      audioEl.volume = m ? 0 : fileVolTarget
    }
    if (masterGain && ctx) {
      const t = ctx.currentTime
      try {
        masterGain.gain.cancelScheduledValues(t)
        masterGain.gain.setTargetAtTime(m ? 0 : baseSynthGain, t, 0.06)
      } catch {
        //
      }
    }
  }

  let fileVolTarget = 0.11

  function stopSynth() {
    if (animId) cancelAnimationFrame(animId)
    animId = 0
    for (const n of synthNodes) {
      try {
        n.stop?.()
        n.disconnect?.()
      } catch {
        //
      }
    }
    synthNodes = []
    try {
      filterNode?.disconnect()
      masterGain?.disconnect()
    } catch {
      //
    }
    filterNode = null
    masterGain = null
    try {
      ctx?.close()
    } catch {
      //
    }
    ctx = null
  }

  function ostSrc() {
    const b = import.meta.env.BASE_URL || "/"
    const base = b.endsWith("/") ? b : `${b}/`
    return `${base}humit-ost.mp3`
  }

  async function tryStartFile() {
    const el = new Audio(ostSrc())
    el.loop = true
    el.preload = "auto"

    await new Promise((resolve, reject) => {
      let settled = false
      const finish = fn => {
        if (settled) return
        settled = true
        window.clearTimeout(tid)
        fn()
      }
      const tid = window.setTimeout(() => finish(() => reject(new Error("ost-timeout"))), 1200)
      el.addEventListener(
        "canplaythrough",
        () => finish(() => resolve()),
        { once: true },
      )
      el.addEventListener(
        "error",
        () => finish(() => reject(new Error("ost-error"))),
        { once: true },
      )
      el.load()
    })

    await el.play()
    mode = "file"
    audioEl = el
    fileVolTarget = 0.11
    audioEl.volume = muted.value ? 0 : fileVolTarget
  }

  async function startSynth() {
    stopSynth()
    mode = "synth"
    ctx = new AudioContext()
    await ctx.resume()

    masterGain = ctx.createGain()
    masterGain.gain.value = muted.value ? 0 : baseSynthGain

    filterNode = ctx.createBiquadFilter()
    filterNode.type = "lowpass"
    filterNode.frequency.value = 380
    filterNode.Q.value = 0.6

    masterGain.connect(filterNode)
    filterNode.connect(ctx.destination)

    const freqs = [146.83, 196, 246.94, 311.13]
    freqs.forEach((f, i) => {
      const osc = ctx.createOscillator()
      osc.type = i % 2 === 0 ? "sine" : "triangle"
      osc.frequency.value = f
      const g = ctx.createGain()
      g.gain.value = 0.065 / (i + 1.15)
      osc.connect(g)
      g.connect(masterGain)
      osc.start()
      synthNodes.push(osc, g)
    })

    let last = performance.now()
    function loop(t) {
      if (mode !== "synth" || !ctx || !filterNode || !masterGain) return
      animId = requestAnimationFrame(loop)
      const dt = Math.min(48, t - last)
      last = t
      const breathe = Math.sin(t / 4200) * 0.015
      const fq = 260 + reactPitch * 420 + reactVol * 180 + Math.sin(t / 8000) * 40
      const gn =
        (muted.value ? 0 : baseSynthGain + reactVol * 0.022 + breathe) *
        (1 + Math.sin(t / 11000) * 0.06)
      try {
        filterNode.frequency.setTargetAtTime(fq, ctx.currentTime, Math.min(0.12, dt / 1000))
        masterGain.gain.setTargetAtTime(Math.min(0.095, gn), ctx.currentTime, Math.min(0.14, dt / 1000))
      } catch {
        //
      }
    }
    animId = requestAnimationFrame(loop)
  }

  /**
   * Call from the game's animation loop - subtly reacts to pitch/volume.
   */
  function tick(pitch01, vol01) {
    reactPitch = pitch01
    reactVol = vol01
    if (mode !== "file" || !audioEl || muted.value) return
    try {
      audioEl.playbackRate = 1 + (pitch01 - 0.5) * 0.035
      fileVolTarget = Math.min(0.16, 0.06 + vol01 * 0.08)
      audioEl.volume = fileVolTarget
    } catch {
      //
    }
  }

  async function start() {
    if (mode !== "off") return
    try {
      await tryStartFile()
    } catch {
      audioEl = null
      await startSynth()
    }
    applyMute()
  }

  function stop() {
    if (audioEl) {
      try {
        audioEl.pause()
        audioEl.removeAttribute("src")
        audioEl.load()
      } catch {
        //
      }
      audioEl = null
    }
    stopSynth()
    mode = "off"
  }

  function toggleMuted() {
    muted.value = !muted.value
    persistMute()
    applyMute()
  }

  function setMuted(m) {
    muted.value = Boolean(m)
    persistMute()
    applyMute()
  }

  return reactive({
    muted,
    start,
    stop,
    tick,
    toggleMuted,
    setMuted,
  })
}
