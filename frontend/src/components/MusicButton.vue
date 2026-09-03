<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from "vue";
import { useBirthdayStore } from "../stores/birthday";

const store = useBirthdayStore();
const playing = ref(true);

let audioElement: HTMLAudioElement | null = null;
let audioContext: AudioContext | null = null;
let musicMaster: GainNode | null = null;
let musicTimer = 0;
let noteIndex = 0;
let musicStarted = false;

const notes = [
  392.0, 523.25, 659.25, 783.99, 659.25, 587.33,
  523.25, 392.0, 659.25, 783.99, 880.0, 783.99,
  659.25, 587.33, 523.25, 440.0, 523.25, 659.25,
  587.33, 659.25, 523.25,
];

function playGeneratedNote() {
  if (!audioContext || !musicMaster) return;
  const frequency = notes[noteIndex % notes.length];
  noteIndex += 1;
  const now = audioContext.currentTime;
  const oscillator = audioContext.createOscillator();
  const gain = audioContext.createGain();
  oscillator.type = "sine";
  oscillator.frequency.value = frequency;
  gain.gain.setValueAtTime(0.0001, now);
  gain.gain.exponentialRampToValueAtTime(0.12, now + 0.025);
  gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.24);
  oscillator.connect(gain);
  gain.connect(musicMaster);
  oscillator.start(now);
  oscillator.stop(now + 0.28);
}

function startFallbackMusic() {
  const AudioContext = window.AudioContext || window.webkitAudioContext;
  if (!AudioContext) return;
  audioContext = new AudioContext();
  musicMaster = audioContext.createGain();
  musicMaster.gain.value = 0.16;
  musicMaster.connect(audioContext.destination);
  noteIndex = 0;
  playGeneratedNote();
  musicTimer = window.setInterval(playGeneratedNote, 300);
  musicStarted = true;
}

function stopFallbackMusic() {
  if (musicTimer) {
    window.clearInterval(musicTimer);
    musicTimer = 0;
  }
  audioContext?.close().catch(() => {});
  audioContext = null;
  musicMaster = null;
  musicStarted = false;
}

async function startConfiguredMusic() {
  if (!store.info.musicUrl) {
    startFallbackMusic();
    return;
  }

  if (!audioElement) {
    audioElement = new Audio(store.info.musicUrl);
    audioElement.loop = true;
  }

  try {
    await audioElement.play();
    musicStarted = true;
  } catch {
    musicStarted = false;
  }
}

function startMusic() {
  if (!playing.value || musicStarted) return;
  if (store.info.musicUrl) {
    void startConfiguredMusic();
  } else {
    startFallbackMusic();
  }
}

function stopMusic() {
  if (audioElement) {
    audioElement.pause();
    audioElement = null;
  } else {
    stopFallbackMusic();
  }
}

function unlockOnFirstGesture(event: PointerEvent) {
  if ((event.target as HTMLElement).closest(".music-pill")) return;
  if (!playing.value) return;
  audioContext?.resume().catch(() => {});
  startMusic();
}

function playAfterCountdown() {
  if (!playing.value) return;
  audioContext?.resume().catch(() => {});
  startMusic();
}

async function toggle() {
  if (playing.value && !musicStarted) {
    startMusic();
    return;
  }

  playing.value = !playing.value;
  if (playing.value) {
    startMusic();
  } else {
    stopMusic();
  }
}

onMounted(() => {
  window.addEventListener("pointerdown", unlockOnFirstGesture, { once: true });
  window.addEventListener("birthday:loading-done", playAfterCountdown);
});

onBeforeUnmount(() => {
  stopMusic();
  window.removeEventListener("pointerdown", unlockOnFirstGesture);
  window.removeEventListener("birthday:loading-done", playAfterCountdown);
});
</script>

<template>
  <button
    class="music-pill"
    type="button"
    :aria-label="playing ? '暂停音乐' : '播放音乐'"
    @click="toggle"
  >
    <span class="music-face" :class="{ 'is-playing': playing }" aria-hidden="true">
      <span v-if="playing" class="rhythm">
        <span></span><span></span><span></span><span></span>
      </span>
      <svg v-else viewBox="0 0 24 24" fill="currentColor">
        <path d="M8 5v14l11-7z"></path>
      </svg>
    </span>
    <span class="music-label">地球持续旋转中...</span>
  </button>
</template>

<style scoped>
.music-pill {
  position: fixed;
  right: max(20px, env(safe-area-inset-right));
  bottom: max(18px, env(safe-area-inset-bottom));
  z-index: 60;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 7px 16px 7px 7px;
  border-radius: 999px;
  color: var(--ink);
  font-size: 13px;
  letter-spacing: 0.04em;
  background: rgba(10, 18, 38, 0.55);
  border: 1px solid rgba(255, 255, 255, 0.16);
  backdrop-filter: blur(14px);
  transition: transform 0.2s ease, border-color 0.2s ease;
}

.music-pill:hover {
  border-color: rgba(70, 224, 125, 0.6);
}

.music-pill:active {
  transform: scale(0.97);
}

.music-face {
  width: 38px;
  height: 38px;
  flex: none;
  display: grid;
  place-items: center;
  border-radius: 50%;
  color: #06101f;
  background: var(--green);
  box-shadow: 0 6px 18px rgba(70, 224, 125, 0.4);
}

.music-face svg {
  width: 18px;
  height: 18px;
}

.music-label {
  white-space: nowrap;
}

@media (max-width: 560px) {
  .music-pill {
    right: max(14px, env(safe-area-inset-right));
    bottom: max(14px, env(safe-area-inset-bottom));
  }

  .music-label {
    font-size: 12px;
  }
}
</style>
