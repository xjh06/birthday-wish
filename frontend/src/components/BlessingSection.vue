<script setup lang="ts">
import { onMounted, ref } from "vue";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { BLESSING_LINES } from "../config/site";
import { useBirthdayStore } from "../stores/birthday";

const store = useBirthdayStore();
const root = ref<HTMLElement | null>(null);

onMounted(() => {
  if (!root.value || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  gsap.registerPlugin(ScrollTrigger);

  gsap.fromTo(
    root.value.querySelectorAll(".blessing-line"),
    { opacity: 0.15, y: 20, filter: "blur(10px)" },
    {
      opacity: 1,
      y: 0,
      filter: "blur(0px)",
      duration: 0.9,
      stagger: 0.12,
      ease: "power3.out",
      scrollTrigger: {
        trigger: root.value,
        start: "top 72%",
        end: "bottom 58%",
      },
    },
  );
});
</script>

<template>
  <section ref="root" class="blessing-section section">
    <div class="section-inner blessing-inner">
      <p class="eyebrow">A few words</p>
      <h2>{{ store.info.blessingTitle }}</h2>
      <div class="blessing-lines">
        <p v-for="(line, index) in BLESSING_LINES" :key="index" class="blessing-line">
          {{ line }}
        </p>
      </div>
      <div class="blessing-rule" aria-hidden="true"></div>
    </div>
  </section>
</template>

<style scoped>
.blessing-section {
  padding-top: 80px;
  padding-bottom: 80px;
}

.blessing-inner {
  max-width: 860px;
}

h2 {
  margin: 0 0 46px;
  color: var(--cream);
  font-family: var(--font-display);
  font-size: clamp(34px, 8vw, 66px);
  font-weight: 500;
  line-height: 1.08;
  letter-spacing: 0;
}

.blessing-lines {
  display: grid;
  gap: 20px;
}

.blessing-line {
  margin: 0;
  color: var(--muted);
  font-family: var(--font-display);
  font-size: clamp(20px, 5vw, 34px);
  line-height: 1.5;
  letter-spacing: 0;
}

.blessing-line:nth-child(2) {
  color: var(--gold);
}

.blessing-line:nth-child(4) {
  color: var(--coral);
}

.blessing-rule {
  width: 100%;
  height: 1px;
  margin-top: 62px;
  background: var(--line);
}
</style>
