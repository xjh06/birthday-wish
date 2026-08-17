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

function unlockOnFirstGesture() {
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
    class="icon-button music-button"
    type="button"
    :aria-label="playing ? '暂停音乐' : '播放音乐'"
    @click="toggle"
  >
    <span v-if="!playing" aria-hidden="true">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M9 18V5l12-2v13"></path>
        <circle cx="6" cy="18" r="3"></circle>
        <circle cx="18" cy="16" r="3"></circle>
      </svg>
    </span>
    <span v-else class="rhythm" aria-hidden="true">
      <span></span><span></span><span></span><span></span>
    </span>
  </button>
</template>
