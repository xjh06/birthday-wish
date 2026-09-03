<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from "vue";
import gsap from "gsap";
import { useBirthdayStore } from "../stores/birthday";

const store = useBirthdayStore();
const root = ref<HTMLElement | null>(null);
let cleanupParallax: (() => void) | null = null;

const name = computed(() => store.info.recipientName);
const slogan = "今天，宇宙把所有温柔的光，都照向同一个名字。";

const sparkles = [
  { left: "10%", top: "20%", size: 7, delay: "0s" },
  { left: "24%", top: "38%", size: 5, delay: "1.2s" },
  { left: "40%", top: "16%", size: 6, delay: "0.6s" },
  { left: "56%", top: "30%", size: 5, delay: "1.8s" },
  { left: "68%", top: "12%", size: 7, delay: "0.3s" },
  { left: "80%", top: "26%", size: 5, delay: "1.4s" },
  { left: "90%", top: "18%", size: 6, delay: "0.9s" },
  { left: "32%", top: "56%", size: 5, delay: "2.1s" },
];

const bubbles = [
  { left: "8%", size: 14, delay: "0s", dur: "9s", drift: "30px" },
  { left: "18%", size: 10, delay: "1.3s", dur: "11s", drift: "-22px" },
  { left: "27%", size: 18, delay: "2.2s", dur: "10s", drift: "18px" },
  { left: "38%", size: 12, delay: "0.7s", dur: "12s", drift: "-26px" },
  { left: "49%", size: 16, delay: "1.6s", dur: "9.5s", drift: "24px" },
  { left: "60%", size: 11, delay: "2.6s", dur: "11.5s", drift: "-18px" },
  { left: "71%", size: 17, delay: "0.4s", dur: "10.5s", drift: "30px" },
  { left: "83%", size: 12, delay: "1.9s", dur: "12s", drift: "-24px" },
  { left: "93%", size: 15, delay: "2.9s", dur: "9s", drift: "20px" },
];

function scrollToStory() {
  document.querySelector("#story")?.scrollIntoView({ behavior: "smooth" });
}

function setupParallax() {
  if (!root.value) return;
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduceMotion || window.matchMedia("(pointer: coarse)").matches) return;

  const planet = root.value.querySelector(".planet");
  const astronaut = root.value.querySelector(".astronaut");
  const coral = root.value.querySelector(".coral-field");
  const copy = root.value.querySelector(".hero-copy");
  const assets = [planet, astronaut, coral, copy];

  const handleMove = (event: PointerEvent) => {
    const cx = event.clientX / window.innerWidth - 0.5;
    const cy = event.clientY / window.innerHeight - 0.5;
    if (planet) gsap.to(planet, { x: cx * -46, y: cy * -32, duration: 1.1, ease: "power2.out" });
    if (astronaut) gsap.to(astronaut, { x: cx * 30, y: cy * 22, duration: 1.1, ease: "power2.out" });
    if (coral) gsap.to(coral, { x: cx * -20, duration: 1.1, ease: "power2.out" });
    if (copy) gsap.to(copy, { x: cx * 16, y: cy * 12, duration: 1.1, ease: "power2.out" });
  };

  window.addEventListener("pointermove", handleMove, { passive: true });
  cleanupParallax = () => {
    window.removeEventListener("pointermove", handleMove);
    assets.forEach((el) => el && gsap.killTweensOf(el));
  };
}

onMounted(() => {
  if (!root.value) return;
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (!reduceMotion) {
    gsap.fromTo(
      root.value.querySelectorAll("[data-hero-reveal]"),
      { y: 34, opacity: 0, filter: "blur(12px)" },
      { y: 0, opacity: 1, filter: "blur(0px)", duration: 1.15, stagger: 0.11, ease: "power3.out" },
    );

    gsap.fromTo(
      root.value.querySelectorAll("[data-planet]"),
      { scale: 0.9, opacity: 0 },
      { scale: 1, opacity: 1, duration: 1.6, ease: "power2.out" },
    );

    gsap.fromTo(
      root.value.querySelectorAll(".astronaut-inner"),
      { y: 40, opacity: 0 },
      { y: 0, opacity: 1, duration: 1.1, delay: 0.55, ease: "power2.out" },
    );
  }

  setupParallax();
});

onBeforeUnmount(() => {
  cleanupParallax?.();
});
</script>

<template>
  <section ref="root" id="home" class="hero">
    <div class="planet" data-planet aria-hidden="true"></div>

    <div class="fx-sparkles" aria-hidden="true">
      <span
        v-for="(s, i) in sparkles"
        :key="i"
        class="sparkle-g"
        :style="{ left: s.left, top: s.top, '--s': s.size + 'px', '--d': s.delay }"
      ></span>
    </div>

    <div class="shooting-star" aria-hidden="true"></div>

    <div class="fx-bubbles" aria-hidden="true">
      <span
        v-for="(b, i) in bubbles"
        :key="i"
        class="bubble"
        :style="{
          left: b.left,
          width: b.size + 'px',
          height: b.size + 'px',
          '--bd': b.delay,
          '--bt': b.dur,
          '--bdrift': b.drift,
        }"
      ></span>
    </div>

    <div class="coral-field" aria-hidden="true">
      <div class="coral-inner">
        <svg viewBox="0 0 1440 400" preserveAspectRatio="none" class="coral-svg">
          <defs>
            <radialGradient id="cg-pink" cx="50%" cy="40%" r="70%">
              <stop offset="0%" stop-color="#f6b4c4" />
              <stop offset="100%" stop-color="#c06a86" />
            </radialGradient>
            <radialGradient id="cg-purple" cx="50%" cy="40%" r="70%">
              <stop offset="0%" stop-color="#9b86e0" />
              <stop offset="100%" stop-color="#5a4486" />
            </radialGradient>
            <radialGradient id="cg-teal" cx="50%" cy="40%" r="70%">
              <stop offset="0%" stop-color="#79d6ca" />
              <stop offset="100%" stop-color="#2f7c74" />
            </radialGradient>
            <radialGradient id="cg-coral" cx="50%" cy="40%" r="70%">
              <stop offset="0%" stop-color="#f0a188" />
              <stop offset="100%" stop-color="#c06a5a" />
            </radialGradient>
          </defs>

          <ellipse cx="120" cy="430" rx="320" ry="150" fill="#3b2e55" />
          <ellipse cx="520" cy="450" rx="360" ry="150" fill="#2c3f5e" />
          <ellipse cx="980" cy="445" rx="380" ry="155" fill="#3a2c50" />
          <ellipse cx="1420" cy="435" rx="320" ry="150" fill="#2a3a57" />

          <ellipse cx="220" cy="400" rx="150" ry="90" fill="url(#cg-pink)" />
          <ellipse cx="470" cy="415" rx="120" ry="86" fill="url(#cg-coral)" />
          <ellipse cx="700" cy="412" rx="150" ry="92" fill="url(#cg-teal)" />
          <ellipse cx="980" cy="418" rx="150" ry="96" fill="url(#cg-purple)" />
          <ellipse cx="1240" cy="410" rx="140" ry="88" fill="url(#cg-pink)" />
          <ellipse cx="1430" cy="415" rx="120" ry="90" fill="url(#cg-coral)" />

          <g stroke-linecap="round" fill="none">
            <path d="M180 400 C170 340 150 320 130 300 M180 400 C185 330 205 310 220 292 M180 400 C180 335 180 300 178 270" stroke="#e07f96" stroke-width="14" />
            <path d="M690 400 C680 340 660 322 645 302 M690 400 C695 334 715 316 728 300 M690 400 C690 340 692 306 690 278" stroke="#67beb4" stroke-width="14" />
            <path d="M1240 400 C1230 340 1212 322 1196 302 M1240 400 C1246 336 1266 318 1278 302 M1240 400 C1240 340 1242 306 1240 280" stroke="#a98fd8" stroke-width="14" />
          </g>

          <g fill="#dbe9ff">
            <circle cx="360" cy="300" r="5" />
            <circle cx="600" cy="290" r="4" />
            <circle cx="860" cy="300" r="5" />
            <circle cx="1100" cy="285" r="4" />
            <circle cx="1330" cy="300" r="5" />
          </g>
        </svg>
      </div>
    </div>

    <div class="astronaut" aria-hidden="true">
      <div class="astronaut-inner">
        <svg viewBox="0 0 260 340" class="astronaut-svg">
          <defs>
            <linearGradient id="helm" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stop-color="#ffffff" />
              <stop offset="100%" stop-color="#cfd4dd" />
            </linearGradient>
            <linearGradient id="visor" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stop-color="#f7e2c4" />
              <stop offset="100%" stop-color="#efc79a" />
            </linearGradient>
            <linearGradient id="suit" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#f4eee3" />
              <stop offset="100%" stop-color="#dcd2c2" />
            </linearGradient>
          </defs>

          <rect x="70" y="150" width="120" height="110" rx="22" fill="#cabfa9" opacity="0.85" />

          <line x1="196" y1="60" x2="222" y2="42" stroke="#b9ad99" stroke-width="4" stroke-linecap="round" />
          <circle cx="224" cy="40" r="6" fill="#f6b4c4" />

          <path d="M84 150 Q62 240 130 258 Q198 240 176 150 Z" fill="url(#suit)" />
          <rect x="100" y="172" width="60" height="40" rx="9" fill="#e3d6c2" stroke="#c2b399" />
          <circle cx="116" cy="190" r="4.5" fill="#e0a2b2" />
          <circle cx="130" cy="190" r="4.5" fill="#6fd0c9" />
          <circle cx="144" cy="190" r="4.5" fill="#8f7bd8" />

          <path d="M84 158 Q50 200 56 232 Q60 244 74 244 Q88 244 90 230 Q92 200 100 168 Z" fill="url(#suit)" />
          <path d="M176 158 Q210 200 204 232 Q200 244 186 244 Q172 244 170 230 Q168 200 160 168 Z" fill="url(#suit)" />
          <circle cx="64" cy="244" r="15" fill="#e3d6c2" />
          <circle cx="196" cy="244" r="15" fill="#e3d6c2" />

          <path d="M104 252 Q96 300 100 316 Q104 326 116 326 Q128 326 130 314 Q132 296 130 254 Z" fill="url(#suit)" />
          <path d="M130 254 Q128 296 130 314 Q132 326 144 326 Q156 326 160 316 Q164 300 156 252 Z" fill="url(#suit)" />
          <ellipse cx="118" cy="328" rx="20" ry="11" fill="#c2b399" />
          <ellipse cx="150" cy="328" rx="20" ry="11" fill="#c2b399" />

          <circle cx="130" cy="92" r="62" fill="url(#helm)" />
          <circle cx="130" cy="92" r="50" fill="url(#visor)" />
          <path d="M96 62 Q130 42 168 66" fill="none" stroke="rgba(255,255,255,0.6)" stroke-width="5" stroke-linecap="round" />

          <g class="astronaut-eyes">
            <ellipse cx="112" cy="90" rx="7" ry="9" fill="#3a2a1e" />
            <ellipse cx="150" cy="90" rx="7" ry="9" fill="#3a2a1e" />
            <ellipse cx="114" cy="84" rx="2.4" ry="2.6" fill="#fff" />
            <ellipse cx="152" cy="84" rx="2.4" ry="2.6" fill="#fff" />
          </g>
          <ellipse cx="131" cy="102" rx="5" ry="4" fill="#d7a178" />
          <path d="M125 112 Q131 118 137 112" fill="none" stroke="#6b4a34" stroke-width="3" stroke-linecap="round" />
          <circle cx="106" cy="106" r="6" fill="#f2b3c2" opacity="0.65" />
          <circle cx="156" cy="106" r="6" fill="#f2b3c2" opacity="0.65" />

          <ellipse cx="130" cy="150" rx="58" ry="12" fill="#bdb29c" />
        </svg>
      </div>
    </div>

    <div class="hero-copy">
      <p class="hero-kicker" data-hero-reveal>B U B B L E &nbsp; W O R L D</p>
      <h1 class="hero-en" data-hero-reveal>HAPPY BIRTHDAY</h1>

      <div class="hero-name-row" data-hero-reveal>
        <h2 class="hero-name">{{ name }}</h2>
        <div class="make-a-wish">
          <button class="wish-play" type="button" aria-label="开启生日祝福" @click="scrollToStory">
            <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M8 5v14l11-7z"></path>
            </svg>
          </button>
          <span class="wish-text">make a wish</span>
        </div>
      </div>

      <div class="hero-left" data-hero-reveal>
        <p class="hero-slogan">{{ slogan }}</p>
        <a class="hero-cta" href="#story">
          <span class="cta-dot" aria-hidden="true"></span>
          开启生日祝福
        </a>
      </div>
    </div>

    <div class="age-badge" aria-hidden="true">
      <span>18</span>
    </div>

    <div class="scroll-cue" aria-hidden="true">
      <span></span>
    </div>
  </section>
</template>

<style scoped>
.hero {
  position: relative;
  min-height: 100vh;
  min-height: 100dvh;
  display: flex;
  align-items: center;
  padding: max(88px, env(safe-area-inset-top)) max(28px, env(safe-area-inset-right)) 84px
    max(34px, env(safe-area-inset-left));
  overflow: hidden;
}

/* --- 行星 --- */
.planet {
  position: absolute;
  top: -6%;
  right: -9%;
  width: min(46vw, 560px);
  aspect-ratio: 1;
  border-radius: 50%;
  background:
    radial-gradient(circle at 30% 28%, rgba(255, 238, 244, 0.95), rgba(230, 150, 162, 0.56) 42%, rgba(184, 118, 136, 0.4) 64%, rgba(120, 72, 96, 0.62) 100%),
    #a97184;
  box-shadow:
    0 0 90px rgba(216, 118, 132, 0.42),
    inset -34px -46px 90px rgba(56, 18, 42, 0.6),
    inset 12px 14px 40px rgba(255, 255, 255, 0.28);
  overflow: hidden;
}

.planet::before {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: repeating-linear-gradient(
    174deg,
    rgba(255, 255, 255, 0.1) 0 9px,
    rgba(120, 56, 82, 0.14) 9px 26px,
    rgba(255, 255, 255, 0.04) 26px 42px
  );
  mix-blend-mode: overlay;
  animation: spin 70s linear infinite;
}

.planet::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: radial-gradient(circle at 28% 26%, transparent 42%, rgba(28, 8, 26, 0.55) 88%);
  animation: breathe 7s ease-in-out infinite;
}

/* --- 闪烁星光 --- */
.fx-sparkles {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
}

.sparkle-g {
  position: absolute;
  width: var(--s, 6px);
  height: var(--s, 6px);
  border-radius: 50%;
  background: #fff;
  box-shadow: 0 0 12px 2px rgba(255, 255, 255, 0.7);
  animation: twinkle 3.4s ease-in-out infinite;
  animation-delay: var(--d, 0s);
}

/* --- 流星 --- */
.shooting-star {
  position: absolute;
  top: 14%;
  right: 18%;
  z-index: 1;
  width: 120px;
  height: 2px;
  border-radius: 999px;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0), rgba(255, 255, 255, 0.9));
  transform: rotate(-35deg);
  animation: shoot 8s ease-in infinite;
  opacity: 0;
}

/* --- 上升气泡 --- */
.fx-bubbles {
  position: absolute;
  inset: 0;
  z-index: 2;
  pointer-events: none;
}

.bubble {
  position: absolute;
  bottom: -10%;
  border-radius: 50%;
  background: radial-gradient(circle at 32% 28%, rgba(255, 255, 255, 0.7), rgba(255, 255, 255, 0.06) 70%);
  border: 1px solid rgba(255, 255, 255, 0.28);
  box-shadow: inset -3px -4px 8px rgba(255, 255, 255, 0.18);
  animation: bubble-rise var(--bt, 10s) linear infinite;
  animation-delay: var(--bd, 0s);
}

/* --- 珊瑚海床 --- */
.coral-field {
  position: absolute;
  left: 0;
  right: 0;
  bottom: -2px;
  z-index: 2;
  height: min(48vh, 430px);
  pointer-events: none;
}

.coral-inner {
  width: 100%;
  height: 100%;
  transform-origin: 50% 100%;
  animation: sway 9s ease-in-out infinite;
}

.coral-svg {
  width: 100%;
  height: 100%;
  display: block;
}

/* --- 宇航员 --- */
.astronaut {
  position: absolute;
  left: 50%;
  bottom: 6%;
  z-index: 3;
  width: min(30vw, 250px);
  transform: translateX(-50%);
  filter: drop-shadow(0 26px 30px rgba(6, 12, 26, 0.5));
}

.astronaut-inner {
  animation: bob 5s ease-in-out infinite;
}

.astronaut-svg {
  width: 100%;
  height: auto;
  display: block;
}

.astronaut-eyes {
  transform-box: fill-box;
  transform-origin: center;
  animation: blink 6.5s infinite;
}

/* --- 文案 --- */
.hero-copy {
  position: relative;
  z-index: 4;
  max-width: 900px;
  margin-left: clamp(0px, 4vw, 70px);
}

.hero-kicker {
  margin: 0 0 14px;
  color: var(--teal);
  font-size: 12px;
  letter-spacing: 0.42em;
}

.hero-en {
  margin: 0;
  font-family: var(--font-display);
  font-size: clamp(44px, 11vw, 130px);
  line-height: 0.92;
  letter-spacing: 0.015em;
  color: #fff;
  text-shadow: 0 10px 60px rgba(90, 160, 255, 0.22);
}

.hero-name-row {
  display: flex;
  align-items: baseline;
  gap: clamp(12px, 2vw, 22px);
  margin-top: clamp(8px, 1.5vw, 14px);
  flex-wrap: wrap;
}

.hero-name {
  margin: 0;
  font-family: var(--font-body);
  font-size: clamp(30px, 6.5vw, 80px);
  font-weight: 900;
  line-height: 1;
  letter-spacing: 0.04em;
  color: #fff;
}

.make-a-wish {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  transform: translateY(-4px);
}

.wish-play {
  width: 44px;
  height: 44px;
  flex: none;
  display: grid;
  place-items: center;
  border-radius: 50%;
  color: #06101f;
  background: var(--green);
  box-shadow: 0 8px 22px rgba(70, 224, 125, 0.4);
  transition: transform 0.2s ease;
  animation: pulse 2.4s ease-in-out infinite;
}

.wish-play:hover {
  transform: scale(1.06);
}

.wish-play svg {
  width: 22px;
  height: 22px;
  transform: translateX(1px);
}

.wish-text {
  font-family: var(--font-script);
  font-size: clamp(28px, 5vw, 54px);
  line-height: 1;
  font-weight: 600;
  color: var(--green);
  transform: rotate(-4deg);
  animation: wish-wobble 3.4s ease-in-out infinite;
}

.hero-left {
  margin-top: clamp(26px, 4vh, 44px);
  max-width: 340px;
}

.hero-slogan {
  margin: 0 0 20px;
  color: var(--muted);
  font-size: clamp(14px, 2vw, 16px);
  line-height: 1.8;
}

.hero-cta {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 12px 22px;
  border-radius: 999px;
  color: var(--ink);
  font-size: 15px;
  letter-spacing: 0.06em;
  text-decoration: none;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.24);
  backdrop-filter: blur(12px);
  transition: background 0.2s ease, border-color 0.2s ease, transform 0.2s ease;
}

.hero-cta:hover {
  background: rgba(255, 255, 255, 0.12);
  border-color: rgba(255, 255, 255, 0.42);
  transform: translateY(-1px);
}

.cta-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--teal);
  box-shadow: 0 0 0 4px rgba(111, 208, 201, 0.2);
  animation: pulse 2.4s ease-in-out infinite;
}

/* --- 18 徽标 --- */
.age-badge {
  position: absolute;
  right: max(22px, env(safe-area-inset-right));
  top: 46%;
  z-index: 5;
  display: grid;
  place-items: center;
  width: 34px;
  height: 120px;
  border-radius: 999px;
  color: var(--ink);
  font-family: var(--font-display);
  font-size: 20px;
  background: rgba(10, 18, 38, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.16);
  backdrop-filter: blur(12px);
}

.age-badge span {
  writing-mode: vertical-rl;
  letter-spacing: 0.1em;
}

/* --- 滚动提示 --- */
.scroll-cue {
  position: absolute;
  left: 50%;
  bottom: 18px;
  z-index: 5;
  width: 24px;
  height: 40px;
  border: 1px solid rgba(255, 255, 255, 0.24);
  border-radius: 999px;
  transform: translateX(-50%);
}

.scroll-cue span {
  position: absolute;
  left: 50%;
  top: 8px;
  width: 3px;
  height: 8px;
  border-radius: 999px;
  background: var(--teal);
  transform: translateX(-50%);
  animation: cue 1.6s ease-in-out infinite;
}

/* --- 动画 --- */
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@keyframes breathe {
  0%,
  100% {
    opacity: 0.9;
  }
  50% {
    opacity: 0.65;
  }
}

@keyframes twinkle {
  0%,
  100% {
    opacity: 0.2;
    transform: scale(0.7);
  }
  50% {
    opacity: 0.95;
    transform: scale(1.2);
  }
}

@keyframes shoot {
  0% {
    transform: translate(0, 0) rotate(-35deg);
    opacity: 0;
  }
  3% {
    opacity: 0;
  }
  6% {
    opacity: 1;
  }
  14% {
    transform: translate(-360px, 240px) rotate(-35deg);
    opacity: 0;
  }
  100% {
    opacity: 0;
    transform: translate(-360px, 240px) rotate(-35deg);
  }
}

@keyframes bubble-rise {
  0% {
    transform: translate(0, 0) scale(1);
    opacity: 0;
  }
  12% {
    opacity: 0.75;
  }
  100% {
    transform: translate(var(--bdrift, 20px), -52vh) scale(1.25);
    opacity: 0;
  }
}

@keyframes sway {
  0%,
  100% {
    transform: rotate(-1.1deg);
  }
  50% {
    transform: rotate(1.1deg);
  }
}

@keyframes bob {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-13px);
  }
}

@keyframes blink {
  0%,
  90%,
  100% {
    transform: scaleY(1);
  }
  94% {
    transform: scaleY(0.08);
  }
  97% {
    transform: scaleY(1);
  }
}

@keyframes pulse {
  0%,
  100% {
    box-shadow: 0 0 0 0 rgba(70, 224, 125, 0.5);
  }
  50% {
    box-shadow: 0 0 0 12px rgba(70, 224, 125, 0);
  }
}

@keyframes wish-wobble {
  0%,
  100% {
    transform: rotate(-4deg) translateY(0);
  }
  50% {
    transform: rotate(-2deg) translateY(-3px);
  }
}

@keyframes cue {
  0%,
  100% {
    transform: translate(-50%, 0);
    opacity: 0.7;
  }
  50% {
    transform: translate(-50%, 12px);
    opacity: 0.2;
  }
}

/* --- 响应式 --- */
@media (max-width: 860px) {
  .planet {
    width: min(64vw, 380px);
    top: -4%;
    right: -16%;
    opacity: 0.9;
  }

  .astronaut {
    width: min(48vw, 220px);
    bottom: 4%;
    opacity: 0.96;
  }

  .hero-copy {
    margin-left: 0;
  }

  .wish-play {
    width: 38px;
    height: 38px;
  }

  .age-badge {
    top: auto;
    bottom: 120px;
    right: max(14px, env(safe-area-inset-right));
  }
}

@media (max-width: 560px) {
  .hero {
    padding-top: 132px;
    padding-bottom: 120px;
  }

  .coral-field {
    height: 40vh;
  }

  .astronaut {
    bottom: 2%;
  }

  .hero-name-row {
    align-items: center;
  }
}

@media (prefers-reduced-motion: reduce) {
  .planet::before,
  .planet::after,
  .sparkle-g,
  .shooting-star,
  .bubble,
  .coral-inner,
  .astronaut-inner,
  .astronaut-eyes,
  .wish-play,
  .wish-text,
  .cta-dot,
  .scroll-cue span {
    animation: none;
  }
}
</style>
