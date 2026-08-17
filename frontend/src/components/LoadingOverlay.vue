<script setup lang="ts">
import { onMounted, ref } from "vue";

const emit = defineEmits<{ done: [] }>();
const countdown = ref(3);
const visible = ref(true);

onMounted(() => {
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const duration = reduceMotion ? 1100 : 2300;
  const steps = reduceMotion ? [3, 0] : [3, 2, 1];
  let index = 0;

  const interval = window.setInterval(() => {
    index += 1;
    countdown.value = steps[Math.min(index, steps.length - 1)];
    if (index >= steps.length - 1) {
      window.clearInterval(interval);
    }
  }, 700);

  window.setTimeout(() => {
    visible.value = false;
    emit("done");
  }, duration);
});
</script>

<template>
  <Transition name="loader">
    <div v-if="visible" class="loading-overlay">
      <div class="orbit" aria-hidden="true">
        <span></span>
        <span></span>
        <span></span>
      </div>
      <div class="countdown">{{ countdown }}</div>
      <p>准备生日惊喜</p>
    </div>
  </Transition>
</template>

<style scoped>
.loading-overlay {
  position: fixed;
  inset: 0;
  z-index: 100;
  display: grid;
  place-content: center;
  justify-items: center;
  gap: 14px;
  color: var(--cream);
  background: #080d1b;
}

.orbit {
  position: relative;
  width: 100px;
  height: 100px;
  animation: spin 2.8s linear infinite;
}

.orbit span {
  position: absolute;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--gold);
  box-shadow: 0 0 18px rgba(233, 195, 107, 0.8);
}

.orbit span:nth-child(1) {
  top: 0;
  left: 44px;
}

.orbit span:nth-child(2) {
  right: 6px;
  bottom: 24px;
  background: var(--coral);
  box-shadow: 0 0 18px rgba(241, 131, 120, 0.8);
}

.orbit span:nth-child(3) {
  bottom: 8px;
  left: 18px;
  background: var(--purple);
  box-shadow: 0 0 18px rgba(189, 169, 232, 0.8);
}

.countdown {
  font-family: var(--font-display);
  font-size: 72px;
  line-height: 1;
  color: var(--gold);
}

p {
  margin: 0;
  color: var(--muted);
  letter-spacing: 0.16em;
  font-size: 13px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loader-leave-active {
  transition: opacity 0.6s ease, transform 0.6s ease;
}

.loader-leave-to {
  opacity: 0;
  transform: scale(1.04);
}

@media (prefers-reduced-motion: reduce) {
  .orbit {
    animation: none;
  }
}
</style>
