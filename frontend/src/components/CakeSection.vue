<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from "vue";
import CelebrationCanvas from "./CelebrationCanvas.vue";
import { useBirthdayStore } from "../stores/birthday";

const emit = defineEmits<{ blown: [] }>();
const store = useBirthdayStore();
const celebration = ref<InstanceType<typeof CelebrationCanvas> | null>(null);
const blown = ref(false);
const micEnabled = ref(false);
const micDenied = ref(false);
const cardVisible = ref(false);

const sparks = [
  { x: "12%", y: "14%", c: "#ffd66b", sz: 7, d: "0s" },
  { x: "24%", y: "8%", c: "#7fd3c7", sz: 6, d: "1.2s" },
  { x: "36%", y: "20%", c: "#8f7bd8", sz: 8, d: "0.6s" },
  { x: "50%", y: "5%", c: "#ff9fc4", sz: 6, d: "1.8s" },
  { x: "64%", y: "16%", c: "#6fd0c9", sz: 7, d: "0.3s" },
  { x: "77%", y: "10%", c: "#ffd66b", sz: 6, d: "1.4s" },
  { x: "88%", y: "22%", c: "#8f7bd8", sz: 8, d: "0.9s" },
  { x: "18%", y: "34%", c: "#ff9fc4", sz: 5, d: "2.1s" },
  { x: "92%", y: "40%", c: "#7fd3c7", sz: 6, d: "0.5s" },
  { x: "8%", y: "50%", c: "#ffd66b", sz: 6, d: "1.6s" },
];

let micStream: MediaStream | null = null;
let micContext: AudioContext | null = null;
let micAnalyser: AnalyserNode | null = null;
let micFrequency: Uint8Array | null = null;
let micFrameId = 0;
let micReadyAt = 0;
let blowFrames = 0;

function burstFireworks() {
  celebration.value?.burst();
}

function blowOut() {
  if (blown.value) return;
  blown.value = true;
  stopMic();
  burstFireworks();
  burstFireworks();
  window.setTimeout(() => {
    cardVisible.value = true;
    emit("blown");
  }, 550);
}

function handleCakeClick() {
  blowOut();
}

function startAmbient() {
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduceMotion) return;
  burstFireworks();
  window.setTimeout(burstFireworks, 900);
  window.setTimeout(burstFireworks, 1900);
  window.setTimeout(burstFireworks, 3000);
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

onMounted(() => {
  window.setTimeout(startAmbient, 900);
});

onBeforeUnmount(() => {
  stopMic();
});
</script>

<template>
  <section id="gift" class="cake-section section">
    <CelebrationCanvas ref="celebration" />
    <div class="section-inner cake-inner">
      <p class="eyebrow">Make a wish</p>
      <h2>许下一个生日愿望</h2>
      <p class="cake-hint">点击蛋糕，或开启右上角麦克风，吹亮整个宇宙</p>

      <div class="cake-scene">
        <div class="cake" :class="{ 'is-blown': blown }" @click="handleCakeClick">
          <div class="cake-halo" aria-hidden="true"></div>

          <span
            v-for="(s, i) in sparks"
            :key="i"
            class="spark"
            :style="{
              left: s.x,
              top: s.y,
              width: s.sz + 'px',
              height: s.sz + 'px',
              '--c': s.c,
              '--d': s.d,
            }"
            aria-hidden="true"
          ></span>

          <div class="cake-base" aria-hidden="true"></div>

          <div class="cake-body" aria-hidden="true">
            <div class="starfield"></div>
            <div class="sheen"></div>
          </div>

          <div class="cake-top" aria-hidden="true">
            <div class="froth"></div>
          </div>

          <div class="ring ring-over" aria-hidden="true"></div>
          <div class="ring ring-main" aria-hidden="true"></div>
          <div class="ring ring-under" aria-hidden="true"></div>

          <div class="candle" aria-hidden="true">
            <div class="flame-glow"></div>
            <div class="flame"></div>
            <div class="smoke"></div>
          </div>
        </div>
        <p class="hb-text">Happy birthday</p>
      </div>

      <button
        class="mic-button icon-button"
        type="button"
        :class="{ 'is-active': micEnabled, 'is-denied': micDenied }"
        :aria-label="micEnabled ? '关闭吹气模式' : '开启吹气模式'"
        @click.stop="toggleMic"
      >
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
@property --ang {
  syntax: "<angle>";
  inherits: false;
  initial-value: 0deg;
}

.cake-section {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding-top: 80px;
  padding-bottom: 40px;
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
  margin: 16px auto 30px;
  max-width: 420px;
  color: var(--muted);
  font-size: 14px;
}

/* 场景 */
.cake-scene {
  position: relative;
  width: min(440px, 94vw);
  margin: 0 auto;
  perspective: 1100px;
}

.cake {
  position: relative;
  height: 350px;
  cursor: pointer;
  animation: cake-sway 9s ease-in-out infinite;
}

/* 光晕 */
.cake-halo {
  position: absolute;
  left: 50%;
  top: 46%;
  width: 82%;
  aspect-ratio: 1;
  transform: translate(-50%, -50%);
  border-radius: 50%;
  background: radial-gradient(circle, rgba(120, 150, 255, 0.35), rgba(180, 120, 240, 0.2) 42%, transparent 68%);
  filter: blur(28px);
  animation: halo-pulse 6s ease-in-out infinite;
  pointer-events: none;
}

/* 底部幻彩底座 */
.cake-base {
  position: absolute;
  left: 50%;
  bottom: 16px;
  width: 340px;
  height: 80px;
  transform: translateX(-50%);
  border-radius: 50%;
  background: linear-gradient(180deg, rgba(190, 205, 255, 0.34), rgba(120, 150, 255, 0.08) 55%, rgba(255, 255, 255, 0.05));
  filter: blur(1px);
  box-shadow: 0 30px 46px rgba(0, 0, 0, 0.5);
}

/* 蛋糕主体（星系表面） */
.cake-body {
  position: absolute;
  left: 50%;
  top: 96px;
  width: 252px;
  height: 178px;
  transform: translateX(-50%);
  border-radius: 18px 18px 26px 26px;
  background: linear-gradient(175deg, #2b3c7c 0%, #1c2b60 34%, #101a44 62%, #0a1234 100%);
  overflow: hidden;
  box-shadow:
    inset -24px -32px 64px rgba(0, 0, 0, 0.5),
    inset 8px 10px 24px rgba(120, 140, 255, 0.18),
    0 28px 56px rgba(0, 0, 0, 0.45);
}

.starfield {
  position: absolute;
  inset: 0;
  background-image:
    radial-gradient(1.6px 1.6px at 30% 30%, rgba(255, 255, 255, 0.9), transparent 60%),
    radial-gradient(1.5px 1.5px at 70% 60%, rgba(255, 214, 120, 0.95), transparent 60%),
    radial-gradient(1.7px 1.7px at 50% 82%, rgba(127, 211, 199, 0.95), transparent 60%),
    radial-gradient(2.2px 2.2px at 20% 72%, rgba(143, 123, 216, 0.95), transparent 60%),
    radial-gradient(1.5px 1.5px at 86% 40%, rgba(246, 180, 196, 0.95), transparent 60%);
  background-size: 120px 120px;
  animation: star-scroll 16s linear infinite;
}

.sheen {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    100deg,
    transparent 18%,
    rgba(255, 182, 220, 0.28) 34%,
    rgba(143, 235, 255, 0.34) 48%,
    rgba(255, 226, 150, 0.28) 62%,
    transparent 78%
  );
  mix-blend-mode: screen;
  background-size: 260% 100%;
  animation: sheen 7s linear infinite;
}

/* 顶盖 */
.cake-top {
  position: absolute;
  left: 50%;
  top: 92px;
  width: 252px;
  height: 72px;
  transform: translateX(-50%);
  border-radius: 50%;
  background: linear-gradient(160deg, #37477f, #1e2c62 55%, #14204c);
  box-shadow:
    inset 0 -14px 26px rgba(0, 0, 0, 0.5),
    0 6px 18px rgba(0, 0, 0, 0.4);
}

.froth {
  position: absolute;
  left: 50%;
  bottom: 2px;
  width: 96%;
  height: 26px;
  transform: translateX(-50%);
  border-radius: 50%;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.75), rgba(190, 205, 255, 0.18));
  filter: blur(2px);
}

/* 幻彩光环 */
.ring {
  position: absolute;
  left: 50%;
  top: 46%;
  transform: translate(-50%, -50%);
  border-radius: 50%;
  pointer-events: none;
  -webkit-mask: radial-gradient(farthest-side, transparent calc(100% - 3px), #000 calc(100% - 2px));
  mask: radial-gradient(farthest-side, transparent calc(100% - 3px), #000 calc(100% - 2px));
  background: conic-gradient(
    from var(--ang),
    rgba(246, 180, 196, 0.95),
    rgba(143, 123, 216, 0.95),
    rgba(127, 211, 199, 0.95),
    rgba(255, 214, 120, 0.95),
    rgba(246, 180, 196, 0.95)
  );
  animation: ring-spin 6s linear infinite;
}

.ring-over {
  width: 316px;
  height: 92px;
  top: 34%;
  animation-duration: 5s;
  animation-delay: -1.5s;
  opacity: 0.9;
}

.ring-main {
  width: 388px;
  height: 112px;
  top: 45%;
  animation-duration: 6.5s;
}

.ring-under {
  width: 356px;
  height: 104px;
  top: 60%;
  animation-duration: 7.5s;
  animation-delay: -3s;
  opacity: 0.85;
}

/* 蜡烛与火苗 */
.candle {
  position: absolute;
  left: 50%;
  top: 60px;
  transform: translateX(-50%);
  width: 12px;
  height: 70px;
  border-radius: 6px;
  background: linear-gradient(180deg, #f6d9e0, #e39bb4 55%, #d884a4);
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.35);
}

.candle::before {
  content: "";
  position: absolute;
  left: 50%;
  top: -6px;
  width: 2px;
  height: 8px;
  background: #6b4a55;
  transform: translateX(-50%);
}

.flame-glow {
  position: absolute;
  left: 50%;
  top: -46px;
  width: 130px;
  height: 130px;
  transform: translate(-50%, -50%);
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 200, 120, 0.55), rgba(255, 160, 90, 0.2) 45%, transparent 70%);
  filter: blur(10px);
  animation: halo-pulse 2.6s ease-in-out infinite;
  pointer-events: none;
}

.flame {
  position: absolute;
  left: 50%;
  top: -30px;
  transform: translateX(-50%);
  width: 18px;
  height: 30px;
  transform-origin: 50% 100%;
  background: radial-gradient(
    circle at 50% 80%,
    #fff7bd 0%,
    #ffd35c 32%,
    #ff9f45 58%,
    rgba(255, 120, 60, 0.6) 76%,
    transparent 100%
  );
  border-radius: 50% 50% 46% 54% / 62% 62% 42% 42%;
  filter: drop-shadow(0 0 12px rgba(255, 180, 80, 0.9)) blur(0.4px);
  animation: flame 1.1s ease-in-out infinite;
}

.smoke {
  position: absolute;
  left: 50%;
  top: -30px;
  transform: translateX(-50%);
  width: 10px;
  height: 22px;
  background: radial-gradient(ellipse at 50% 100%, rgba(200, 205, 225, 0.7), transparent 70%);
  opacity: 0;
  border-radius: 50%;
}

.is-blown .flame {
  animation: none;
  opacity: 0;
  transform: translateX(-50%) scale(0.2);
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.is-blown .flame-glow {
  animation: none;
  opacity: 0;
  transition: opacity 0.4s ease;
}

.is-blown .smoke {
  opacity: 0.7;
  animation: smoke 1.8s ease-out forwards;
}

.is-blown .cake-halo {
  animation: none;
}

/* 飘浮的幻彩光点 */
.spark {
  position: absolute;
  border-radius: 50%;
  background: var(--c);
  box-shadow: 0 0 10px var(--c);
  opacity: 0.9;
  animation: float-spark 6s ease-in-out infinite;
  animation-delay: var(--d, 0s);
  pointer-events: none;
}

.hb-text {
  margin: 32px auto 0;
  font-family: var(--font-script);
  font-size: clamp(24px, 4.4vw, 34px);
  font-weight: 600;
  color: rgba(255, 255, 255, 0.88);
  text-align: center;
  transform: rotate(-3deg);
}

.mic-button.is-active {
  color: var(--gold);
  border-color: rgba(185, 200, 255, 0.7);
}

.mic-button.is-denied {
  color: var(--coral);
  border-color: rgba(242, 160, 176, 0.6);
}

.wish-card {
  width: min(360px, calc(100vw - 36px));
  margin: 34px auto 0;
  padding: 30px 28px;
  text-align: center;
  border-radius: 12px;
}

.card-kicker {
  margin: 0 0 12px;
  color: var(--teal);
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

/* 动画 */
@keyframes cake-sway {
  0%,
  100% {
    transform: rotate(-1.2deg);
  }
  50% {
    transform: rotate(1.2deg);
  }
}

@keyframes halo-pulse {
  0%,
  100% {
    opacity: 0.85;
    transform: translate(-50%, -50%) scale(1);
  }
  50% {
    opacity: 0.55;
    transform: translate(-50%, -50%) scale(1.08);
  }
}

@keyframes star-scroll {
  to {
    background-position: -240px 0;
  }
}

@keyframes sheen {
  to {
    background-position: -260% 0;
  }
}

@keyframes ring-spin {
  to {
    --ang: 360deg;
  }
}

@keyframes flame {
  0%,
  100% {
    transform: translateX(-50%) rotate(-2deg) scaleY(0.96) scaleX(1.02);
  }
  25% {
    transform: translateX(-50%) rotate(3deg) scaleY(1.08) scaleX(0.92);
  }
  55% {
    transform: translateX(-50%) rotate(-4deg) scaleY(0.92) scaleX(1.08);
  }
  78% {
    transform: translateX(-50%) rotate(2deg) scaleY(1.05) scaleX(0.96);
  }
}

@keyframes smoke {
  0% {
    opacity: 0;
    transform: translate(-50%, 0) scale(0.7);
  }
  35% {
    opacity: 0.65;
  }
  100% {
    opacity: 0;
    transform: translate(-50%, -32px) scale(1.3);
  }
}

@keyframes float-spark {
  0%,
  100% {
    transform: translateY(0) scale(1);
  }
  50% {
    transform: translateY(-14px) scale(1.18);
  }
}

/* 响应式 */
@media (max-width: 720px) {
  .cake-scene {
    transform: scale(0.84);
  }
}

@media (max-width: 520px) {
  .cake-scene {
    transform: scale(0.68);
    width: min(380px, 96vw);
  }
}

@media (prefers-reduced-motion: reduce) {
  .cake,
  .cake-halo,
  .starfield,
  .sheen,
  .ring,
  .flame,
  .flame-glow,
  .spark {
    animation: none;
  }
}
</style>
