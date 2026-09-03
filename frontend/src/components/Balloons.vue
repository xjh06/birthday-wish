<script setup lang="ts">
const balloons = [
  { left: "8%", color: "#6fd0c9", delay: "0s", duration: "11s", drift: "24px" },
  { left: "20%", color: "#f6b4c4", delay: "-3s", duration: "13s", drift: "-18px" },
  { left: "33%", color: "#8f7bd8", delay: "-7s", duration: "12s", drift: "30px" },
  { left: "48%", color: "#f0a188", delay: "-2s", duration: "14s", drift: "-28px" },
  { left: "62%", color: "#b9c8ff", delay: "-8s", duration: "11.5s", drift: "20px" },
  { left: "76%", color: "#6fd0c9", delay: "-4s", duration: "13.5s", drift: "-20px" },
  { left: "88%", color: "#8f7bd8", delay: "-6s", duration: "12.5s", drift: "26px" },
];
</script>

<template>
  <div class="balloon-layer" aria-hidden="true">
    <span
      v-for="(balloon, index) in balloons"
      :key="index"
      class="balloon"
      :style="{
        left: balloon.left,
        '--balloon-color': balloon.color,
        '--balloon-delay': balloon.delay,
        '--balloon-duration': balloon.duration,
        '--balloon-drift': balloon.drift,
      }"
    ></span>
  </div>
</template>

<style scoped>
.balloon-layer {
  position: fixed;
  inset: 0;
  z-index: -1;
  pointer-events: none;
  overflow: hidden;
}

.balloon {
  position: absolute;
  bottom: -16vh;
  width: 32px;
  height: 42px;
  animation: balloon-rise var(--balloon-duration) linear infinite;
  animation-delay: var(--balloon-delay);
  opacity: 0.72;
  filter: saturate(0.8) drop-shadow(0 10px 16px rgba(0, 0, 0, 0.22));
}

.balloon::before {
  content: "";
  position: absolute;
  inset: 0 0 10px;
  border-radius: 50% 50% 48% 52%;
  background: var(--balloon-color);
  background-image: radial-gradient(circle at 34% 24%, rgba(255, 255, 255, 0.42), transparent 27%);
  box-shadow: inset -7px -8px 16px rgba(0, 0, 0, 0.12);
}

.balloon::after {
  content: "";
  position: absolute;
  left: 15px;
  bottom: 0;
  width: 2px;
  height: 10px;
  background: rgba(255, 255, 255, 0.55);
  transform: rotate(8deg);
}

@keyframes balloon-rise {
  0% {
    transform: translate3d(0, 0, 0) rotate(-3deg);
  }
  50% {
    transform: translate3d(var(--balloon-drift), -62vh, 0) rotate(5deg);
  }
  100% {
    transform: translate3d(calc(var(--balloon-drift) * -0.4), -134vh, 0) rotate(-5deg);
  }
}

@media (prefers-reduced-motion: reduce) {
  .balloon {
    animation: none;
    opacity: 0.38;
  }
}
</style>
