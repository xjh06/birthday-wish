<script setup lang="ts">
import { onMounted, ref } from "vue";
import gsap from "gsap";
import { useBirthdayStore } from "../stores/birthday";

const store = useBirthdayStore();
const root = ref<HTMLElement | null>(null);

onMounted(() => {
  if (!root.value) return;
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduceMotion) return;

  gsap.fromTo(
    root.value.querySelectorAll("[data-hero-reveal]"),
    { y: 32, opacity: 0, filter: "blur(12px)" },
    { y: 0, opacity: 1, filter: "blur(0px)", duration: 1.2, stagger: 0.12, ease: "power3.out" },
  );
});
</script>

<template>
  <section ref="root" class="hero-section section">
    <div class="hero-copy section-inner">
      <p class="eyebrow" data-hero-reveal>Happy Birthday</p>
      <h1 data-hero-reveal>{{ store.info.heroTitle }}</h1>
      <p class="hero-date" data-hero-reveal>{{ store.info.birthdayDate }}</p>
      <div class="hero-subline" data-hero-reveal>
        <span></span>
        <p>把这一天的光，都留给你。</p>
        <span></span>
      </div>
    </div>
    <div class="scroll-cue" aria-hidden="true">
      <span></span>
    </div>
  </section>
</template>

<style scoped>
.hero-section {
  min-height: 100vh;
  min-height: 100dvh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding-top: 88px;
}

.hero-copy {
  text-align: center;
}

.eyebrow {
  color: var(--gold);
}

h1 {
  margin: 0;
  color: var(--cream);
  font-family: var(--font-display);
  font-size: clamp(46px, 12vw, 116px);
  font-weight: 500;
  line-height: 0.98;
  letter-spacing: 0;
  text-shadow: 0 18px 70px rgba(233, 195, 107, 0.15);
}

.hero-date {
  margin: 22px 0 0;
  color: var(--coral);
  font-size: clamp(17px, 4vw, 24px);
  letter-spacing: 0.08em;
}

.hero-subline {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 14px;
  margin-top: 28px;
  color: var(--muted);
}

.hero-subline p {
  margin: 0;
  font-size: 14px;
  letter-spacing: 0.08em;
}

.hero-subline span {
  width: 36px;
  height: 1px;
  background: var(--line);
}

.scroll-cue {
  position: absolute;
  left: 50%;
  bottom: 26px;
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
  background: var(--gold);
  transform: translateX(-50%);
  animation: cue 1.6s ease-in-out infinite;
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

@media (max-width: 640px) {
  .hero-section {
    padding-top: 72px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .scroll-cue span {
    animation: none;
  }
}
</style>
