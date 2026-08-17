<script setup lang="ts">
import { onBeforeUnmount, ref } from "vue";
import CelebrationCanvas from "./CelebrationCanvas.vue";
import { useBirthdayStore } from "../stores/birthday";

const emit = defineEmits<{ blown: [] }>();
const store = useBirthdayStore();
const celebration = ref<InstanceType<typeof CelebrationCanvas> | null>(null);
const blown = ref(false);
const micEnabled = ref(false);
const micDenied = ref(false);
const cardVisible = ref(false);

let micStream: MediaStream | null = null;
let micContext: AudioContext | null = null;
let micAnalyser: AnalyserNode | null = null;
let micFrequency: Uint8Array | null = null;
let micFrameId = 0;
let micReadyAt = 0;
let blowFrames = 0;

function blowOut() {
  if (blown.value) return;
  blown.value = true;
  stopMic();
  celebration.value?.burst();
  window.setTimeout(() => {
    cardVisible.value = true;
    emit("blown");
  }, 550);
}

function handleCakeClick() {
  blowOut();
}

function readBlowStrength() {
  if (!micAnalyser || !micFrequency) return 0;
  micAnalyser.getByteFrequencyData(micFrequency);
  let sum = 0;
  for (let i = 0; i < 18; i += 1) {
    sum += micFrequency[i];
  }
  return sum / 18;
}

function monitorMic() {
  if (!micEnabled.value) return;
  const strength = readBlowStrength();
  if (performance.now() > micReadyAt && strength > 72) {
    blowFrames += 1;
  } else {
    blowFrames = 0;
  }

  if (blowFrames >= 4) {
    blowOut();
    return;
  }

  micFrameId = requestAnimationFrame(monitorMic);
}

function stopMic() {
  micEnabled.value = false;
  micDenied.value = false;
  blowFrames = 0;
  if (micFrameId) {
    cancelAnimationFrame(micFrameId);
    micFrameId = 0;
  }
  micStream?.getTracks().forEach((track) => track.stop());
  micStream = null;
  micContext?.close().catch(() => {});
  micContext = null;
  micAnalyser = null;
  micFrequency = null;
}

async function toggleMic() {
  if (micEnabled.value) {
    stopMic();
    return;
  }

  if (!navigator.mediaDevices?.getUserMedia) {
    micDenied.value = true;
    return;
  }

  try {
    micStream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    micContext = new AudioContext();
    micAnalyser = micContext.createAnalyser();
    micAnalyser.fftSize = 256;
    micAnalyser.smoothingTimeConstant = 0.78;
    micFrequency = new Uint8Array(micAnalyser.frequencyBinCount);
    micContext.createMediaStreamSource(micStream).connect(micAnalyser);
    micEnabled.value = true;
    micReadyAt = performance.now() + 450;
    micFrameId = requestAnimationFrame(monitorMic);
  } catch {
    micDenied.value = true;
  }
}

onBeforeUnmount(() => {
  stopMic();
});
</script>

<template>
  <section class="cake-section section">
    <div class="section-inner cake-inner">
      <p class="eyebrow">Make a wish</p>
      <h2>吹灭蜡烛，收下祝福</h2>
      <p class="cake-hint">点击蜡烛，或开启右上角麦克风后吹气</p>

      <div class="cake-wrap" :class="{ 'is-blown': blown }" @click="handleCakeClick">
        <svg class="cake-svg" viewBox="0 0 340 310" role="img" aria-label="生日蛋糕">
          <defs>
            <linearGradient id="flameGradient" x1="0" y1="1" x2="0" y2="0">
              <stop offset="0" stop-color="#f18378" />
              <stop offset="0.38" stop-color="#f3c86d" />
              <stop offset="1" stop-color="#fff4b4" />
            </linearGradient>
            <linearGradient id="bottomCake" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0" stop-color="#e8a7bd" />
              <stop offset="1" stop-color="#b97395" />
            </linearGradient>
            <linearGradient id="middleCake" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0" stop-color="#f2dba0" />
              <stop offset="1" stop-color="#b89a68" />
            </linearGradient>
            <linearGradient id="topCake" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0" stop-color="#bda9e8" />
              <stop offset="1" stop-color="#745d9e" />
            </linearGradient>
            <filter id="flameGlow" x="-80%" y="-80%" width="260%" height="260%">
              <feGaussianBlur stdDeviation="3.5" result="blur" />
              <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>

          <ellipse cx="170" cy="286" rx="130" ry="16" fill="rgba(0, 0, 0, 0.28)" />
          <path d="M75 206h190v54c0 17-13 28-30 28H105c-17 0-30-11-30-28z" fill="url(#bottomCake)" />
          <path d="M72 203c0 8 44 14 98 14s98-6 98-14-44-13-98-13-98 5-98 13z" fill="#f4cbd8" />
          <path d="M75 209c20-8 59-11 96-11 39 0 78 3 94 11l-2 8c-18-7-53-10-92-10-38 0-73 3-94 10z" fill="rgba(255,255,255,.48)" />

          <path d="M94 158h152v43c0 15-11 25-25 25H119c-14 0-25-10-25-25z" fill="url(#middleCake)" />
          <path d="M90 155c0 7 36 12 80 12s80-5 80-12-36-11-80-11-80 4-80 11z" fill="#f6e6bf" />
          <path d="M94 161c17-6 48-9 76-9 31 0 62 3 75 9l-2 7c-17-6-45-9-73-9-29 0-58 3-75 9z" fill="rgba(255,255,255,.4)" />

          <path d="M114 104h112v39c0 13-10 22-23 22H137c-13 0-23-9-23-22z" fill="url(#topCake)" />
          <path d="M111 101c0 6 27 10 59 10s59-4 59-10-27-9-59-9-59 3-59 9z" fill="#d8cef5" />
          <path d="M114 106c13-5 35-7 56-7 23 0 45 2 56 7l-1 6c-16-5-35-7-55-7-22 0-41 2-55 7z" fill="rgba(255,255,255,.46)" />

          <circle cx="118" cy="236" r="5" fill="#e9c36b" opacity=".9" />
          <circle cx="142" cy="245" r="4" fill="#bda9e8" opacity=".9" />
          <circle cx="196" cy="242" r="5" fill="#e9c36b" opacity=".9" />
          <circle cx="221" cy="232" r="4" fill="#f18378" opacity=".9" />
          <path d="M162 216l7 7 14-15" fill="none" stroke="rgba(255,255,255,.6)" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" />

          <g class="candle" transform="translate(139 55)">
            <rect x="-5" y="0" width="10" height="43" rx="4" fill="#f2cfd8" />
            <rect x="-5" y="0" width="10" height="10" rx="4" fill="#e99fb7" />
            <path d="M0 0v-7" stroke="#d8c4c0" stroke-width="2" stroke-linecap="round" />
            <g class="flame-wrap" transform="translate(0 -12)">
              <path class="flame-shape" d="M0 0C-7-5-11-17-5-27 0-34 7-25 7-15 7-8 4-2 0 0Z" fill="url(#flameGradient)" filter="url(#flameGlow)" />
              <ellipse class="flame-core" cx="0" cy="-15" rx="2.6" ry="5.5" fill="#fff7bd" />
              <path class="smoke" d="M-2 0C-9-11-3-27 2-39c5 12 12 28 3 39Z" fill="#c9bfd1" opacity="0" />
            </g>
          </g>
          <g class="candle" transform="translate(170 44)">
            <rect x="-5" y="0" width="10" height="52" rx="4" fill="#d5c4ef" />
            <rect x="-5" y="0" width="10" height="12" rx="4" fill="#a893d4" />
            <path d="M0 0v-8" stroke="#d8c4c0" stroke-width="2" stroke-linecap="round" />
            <g class="flame-wrap" transform="translate(0 -13)">
              <path class="flame-shape" d="M0 0C-7-5-11-17-5-27 0-34 7-25 7-15 7-8 4-2 0 0Z" fill="url(#flameGradient)" filter="url(#flameGlow)" />
              <ellipse class="flame-core" cx="0" cy="-15" rx="2.6" ry="5.5" fill="#fff7bd" />
              <path class="smoke" d="M-2 0C-9-11-3-27 2-39c5 12 12 28 3 39Z" fill="#c9bfd1" opacity="0" />
            </g>
          </g>
          <g class="candle" transform="translate(201 52)">
            <rect x="-5" y="0" width="10" height="46" rx="4" fill="#f6d9a8" />
            <rect x="-5" y="0" width="10" height="11" rx="4" fill="#d1a965" />
            <path d="M0 0v-8" stroke="#d8c4c0" stroke-width="2" stroke-linecap="round" />
            <g class="flame-wrap" transform="translate(0 -13)">
              <path class="flame-shape" d="M0 0C-7-5-11-17-5-27 0-34 7-25 7-15 7-8 4-2 0 0Z" fill="url(#flameGradient)" filter="url(#flameGlow)" />
              <ellipse class="flame-core" cx="0" cy="-15" rx="2.6" ry="5.5" fill="#fff7bd" />
              <path class="smoke" d="M-2 0C-9-11-3-27 2-39c5 12 12 28 3 39Z" fill="#c9bfd1" opacity="0" />
            </g>
          </g>
        </svg>
      </div>

      <button class="mic-button icon-button" type="button" :class="{ 'is-active': micEnabled, 'is-denied': micDenied }" :aria-label="micEnabled ? '关闭吹气模式' : '开启吹气模式'" @click.stop="toggleMic">
        <svg v-if="!micEnabled" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <rect x="9" y="2" width="6" height="12" rx="3"></rect>
          <path d="M5 10v1a7 7 0 0 0 14 0v-1"></path>
          <path d="M12 18v3"></path>
        </svg>
        <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <rect x="9" y="2" width="6" height="12" rx="3"></rect>
          <path d="M5 10v1a7 7 0 0 0 14 0v-1"></path>
          <path d="M12 18v3"></path>
          <path d="M4 4l16 16"></path>
        </svg>
      </button>

      <Transition name="card-pop">
        <div v-if="cardVisible" class="wish-card glass-card">
          <p class="card-kicker">For You</p>
          <h3>{{ store.info.cardSalutation || store.info.recipientName }}</h3>
          <p class="card-date">{{ store.info.birthdayDate }}</p>
          <p class="card-message">{{ store.info.cardMessage || store.info.blessingText }}</p>
        </div>
      </Transition>
    </div>
  </section>
</template>

<style scoped>
.cake-section {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cake-inner {
  text-align: center;
}

h2 {
  margin: 0;
  color: var(--cream);
  font-family: var(--font-display);
  font-size: clamp(34px, 8vw, 68px);
  font-weight: 500;
  line-height: 1.08;
  letter-spacing: 0;
}

.cake-hint {
  margin: 16px auto 28px;
  max-width: 420px;
  color: var(--muted);
  font-size: 14px;
}

.cake-wrap {
  position: relative;
  width: min(390px, 88vw);
  margin: 0 auto;
  cursor: pointer;
  filter: drop-shadow(0 22px 24px rgba(0, 0, 0, 0.28));
  transition: transform 0.45s ease;
}

.cake-wrap:hover {
  transform: translateY(-4px);
}

.cake-svg {
  display: block;
  width: 100%;
  height: auto;
}

.flame-shape,
.flame-core {
  transform-box: fill-box;
  transform-origin: 50% 100%;
  animation: flame 1.1s ease-in-out infinite;
}

.flame-core {
  animation-duration: 0.82s;
}

.smoke {
  opacity: 0;
}

.is-blown .flame-shape,
.is-blown .flame-core {
  animation: none;
  opacity: 0;
  transform: scale(0.15);
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.is-blown .smoke {
  opacity: 0.62;
  animation: smoke 1.8s ease-out forwards;
}

@keyframes flame {
  0%,
  100% {
    transform: rotate(-2deg) scaleY(0.96) scaleX(1.02);
  }
  25% {
    transform: rotate(3deg) scaleY(1.08) scaleX(0.92);
  }
  55% {
    transform: rotate(-4deg) scaleY(0.92) scaleX(1.08);
  }
  78% {
    transform: rotate(2deg) scaleY(1.05) scaleX(0.96);
  }
}

@keyframes smoke {
  0% {
    opacity: 0;
    transform: translateY(0) scale(0.7);
  }
  35% {
    opacity: 0.65;
  }
  100% {
    opacity: 0;
    transform: translateY(-28px) scale(1.25);
  }
}

.mic-button.is-active {
  color: var(--gold);
  border-color: rgba(233, 195, 107, 0.7);
}

.mic-button.is-denied {
  color: var(--coral);
  border-color: rgba(241, 131, 120, 0.6);
}

.wish-card {
  width: min(360px, calc(100vw - 36px));
  margin: 30px auto 0;
  padding: 30px 28px;
  text-align: center;
  border-radius: 8px;
}

.card-kicker {
  margin: 0 0 12px;
  color: var(--gold);
  font-size: 11px;
  letter-spacing: 0.24em;
  text-transform: uppercase;
}

h3 {
  margin: 0;
  color: var(--cream);
  font-family: var(--font-display);
  font-size: clamp(26px, 7vw, 34px);
  font-weight: 500;
}

.card-date {
  margin: 12px 0 0;
  color: var(--coral);
  letter-spacing: 0.12em;
}

.card-message {
  margin: 20px 0 0;
  color: var(--muted);
  line-height: 1.8;
  font-size: 15px;
}

.card-pop-enter-active,
.card-pop-leave-active {
  transition: opacity 0.55s ease, transform 0.55s ease;
}

.card-pop-enter-from,
.card-pop-leave-to {
  opacity: 0;
  transform: translateY(18px) scale(0.96);
}

@media (prefers-reduced-motion: reduce) {
  .flame-shape,
  .flame-core {
    animation: none;
  }

  .cake-wrap:hover {
    transform: none;
  }
}
</style>
