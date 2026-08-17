<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from "vue";

const canvas = ref<HTMLCanvasElement | null>(null);
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

let context: CanvasRenderingContext2D | null = null;
let width = 0;
let height = 0;
let rafId = 0;
let particles: any[] = [];

const colors = ["#f18378", "#e9c36b", "#f3a0b8", "#bda9e8", "#7fd3c7", "#fff4d7"];

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
}

function addConfetti(x: number, y: number, count = 90) {
  for (let i = 0; i < count; i += 1) {
    const angle = Math.random() * Math.PI * 2;
    const speed = 5 + Math.random() * 8;
    particles.push({
      type: "confetti",
      x,
      y,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed - 3,
      width: 5 + Math.random() * 7,
      height: 11 + Math.random() * 9,
      rotation: Math.random() * Math.PI,
      spin: (Math.random() - 0.5) * 0.3,
      color: colors[Math.floor(Math.random() * colors.length)],
      gravity: 0.17,
      drag: 0.985,
      life: 1,
      decay: 0.008 + Math.random() * 0.008,
    });
  }
}

function addFirework(x: number, y: number) {
  const count = 56;
  for (let i = 0; i < count; i += 1) {
    const angle = (Math.PI * 2 * i) / count + (Math.random() - 0.5) * 0.12;
    const speed = 3.4 + Math.random() * 4.8;
    particles.push({
      type: "spark",
      x,
      y,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed,
      size: 1.4 + Math.random() * 2.3,
      color: colors[Math.floor(Math.random() * colors.length)],
      gravity: 0.05,
      drag: 0.975,
      life: 1,
      decay: 0.011 + Math.random() * 0.009,
    });
  }
}

function render() {
  if (!context) return;
  context.clearRect(0, 0, width, height);
  particles = particles.filter((particle) => particle.life > 0);

  for (const particle of particles) {
    particle.vx *= particle.drag;
    particle.vy = particle.vy * particle.drag + particle.gravity;
    particle.x += particle.vx;
    particle.y += particle.vy;
    particle.life -= particle.decay;

    context.save();
    context.globalAlpha = Math.max(particle.life, 0);
    context.fillStyle = particle.color;

    if (particle.type === "confetti") {
      particle.rotation += particle.spin;
      context.translate(particle.x, particle.y);
      context.rotate(particle.rotation);
      context.fillRect(-particle.width / 2, -particle.height / 2, particle.width, particle.height);
    } else {
      context.beginPath();
      context.arc(particle.x, particle.y, particle.size * Math.max(particle.life, 0.2), 0, Math.PI * 2);
      context.fill();
      context.globalAlpha *= 0.25;
      context.beginPath();
      context.arc(particle.x, particle.y, particle.size * 2.3 * Math.max(particle.life, 0.12), 0, Math.PI * 2);
      context.fill();
    }

    context.restore();
  }

  if (particles.length > 0) {
    rafId = requestAnimationFrame(render);
  }
}

function burst() {
  const x = width * (0.28 + Math.random() * 0.44);
  const y = height * (0.28 + Math.random() * 0.2);
  addConfetti(x, y);
  addFirework(x, y);
  if (reduceMotion) {
    render();
    cancelAnimationFrame(rafId);
  } else if (!rafId) {
    rafId = requestAnimationFrame(render);
  }
}

defineExpose({ burst });

onMounted(() => {
  const target = canvas.value;
  if (!target) return;
  context = target.getContext("2d");
  resize();
  window.addEventListener("resize", resize);
});

onBeforeUnmount(() => {
  cancelAnimationFrame(rafId);
  window.removeEventListener("resize", resize);
});
</script>

<template>
  <canvas ref="canvas" class="celebration-canvas" aria-hidden="true"></canvas>
</template>

<style scoped>
.celebration-canvas {
  position: fixed;
  inset: 0;
  z-index: 30;
  pointer-events: none;
}
</style>
