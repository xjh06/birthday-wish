<script setup lang="ts">
import { onBeforeUnmount, onMounted } from "vue";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Lenis from "lenis";

gsap.registerPlugin(ScrollTrigger);

let lenis: Lenis | null = null;
let rafId = 0;
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
const allowSmoothScroll = window.matchMedia("(pointer: fine)").matches && !reduceMotion.matches;

function updateScrollProxy() {
  if (!allowSmoothScroll) return;
  lenis = new Lenis({
    duration: 1.05,
    easing: (value) => 1 - Math.pow(1 - value, 4),
    smoothWheel: true,
    syncTouch: false,
  });

  lenis.on("scroll", ScrollTrigger.update);

  const tick = (time: number) => {
    lenis?.raf(time);
    rafId = requestAnimationFrame(tick);
  };
  rafId = requestAnimationFrame(tick);
}

onMounted(() => {
  updateScrollProxy();
});

onBeforeUnmount(() => {
  cancelAnimationFrame(rafId);
  lenis?.destroy();
});
</script>

<template>
  <RouterView />
</template>
