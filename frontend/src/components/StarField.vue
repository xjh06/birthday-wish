<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from "vue";

const canvas = ref<HTMLCanvasElement | null>(null);
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

let context: CanvasRenderingContext2D | null = null;
let width = 0;
let height = 0;
let rafId = 0;
let pointerX = 0;
let pointerY = 0;

type Star = {
  x: number;
  y: number;
  radius: number;
  baseAlpha: number;
  speed: number;
  phase: number;
  layer: number;
};

let stars: Star[] = [];

function resize() {
  if (!canvas.value || !context) return;
  const ratio = Math.min(window.devicePixelRatio || 1, 2);
  width = window.innerWidth;
  height = window.innerHeight;
  canvas.value.width = width * ratio;
  canvas.value.height = height * ratio;
  canvas.value.style.width = `${width}px`;
  canvas.value.style.height = `${height}px`;
  context.setTransform(ratio, 0, 0, ratio, 0, 0);
  createStars();
}

function createStars() {
  const count = Math.min(120, Math.max(42, Math.floor((width * height) / 13000)));
  stars = Array.from({ length: count }, () => ({
    x: Math.random() * width,
    y: Math.random() * height,
    radius: Math.random() * 1.2 + 0.3,
    baseAlpha: Math.random() * 0.55 + 0.18,
    speed: Math.random() * 0.012 + 0.003,
    phase: Math.random() * Math.PI * 2,
    layer: Math.random() > 0.7 ? 0.22 : 0.08,
  }));
}

function draw(time: number) {
  if (!context) return;
  context.clearRect(0, 0, width, height);
  const offsetX = (pointerX - width / 2) * 0.018;
  const offsetY = (pointerY - height / 2) * 0.018;

  for (const star of stars) {
    const twinkle = Math.sin(time * star.speed + star.phase) * 0.28 + 0.72;
    const alpha = star.baseAlpha * twinkle;
    const x = star.x + offsetX * star.layer;
    const y = star.y + offsetY * star.layer;

    context.beginPath();
    context.arc(x, y, star.radius, 0, Math.PI * 2);
    context.fillStyle = `rgba(255, 248, 230, ${alpha})`;
    context.fill();
  }

  rafId = requestAnimationFrame(draw);
}

function handlePointer(event: PointerEvent) {
  pointerX = event.clientX;
  pointerY = event.clientY;
}

onMounted(() => {
  const target = canvas.value;
  if (!target) return;
  context = target.getContext("2d");
  resize();
  window.addEventListener("resize", resize);
  window.addEventListener("pointermove", handlePointer, { passive: true });
  if (reduceMotion) {
    draw(1);
    cancelAnimationFrame(rafId);
  } else {
    rafId = requestAnimationFrame(draw);
  }
});

onBeforeUnmount(() => {
  cancelAnimationFrame(rafId);
  window.removeEventListener("resize", resize);
  window.removeEventListener("pointermove", handlePointer);
});
</script>

<template>
  <canvas ref="canvas" class="starfield" aria-hidden="true"></canvas>
</template>

<style scoped>
.starfield {
  position: fixed;
  inset: 0;
  z-index: -1;
  width: 100%;
  height: 100%;
  pointer-events: none;
}
</style>
