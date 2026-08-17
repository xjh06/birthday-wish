<script setup lang="ts">
import { useBirthdayStore } from "../stores/birthday";

const store = useBirthdayStore();

function replay() {
  window.location.reload();
}
</script>

<template>
  <section class="finale-section section">
    <div class="section-inner finale-inner">
      <p class="eyebrow">Happy birthday</p>
      <h2>{{ store.info.heroTitle }}</h2>
      <p class="finale-message">{{ store.info.blessingText }}</p>
      <button class="replay-button" type="button" @click="replay">再看一次</button>
    </div>
  </section>
</template>

<style scoped>
.finale-section {
  min-height: 100vh;
  min-height: 100dvh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.finale-inner {
  text-align: center;
}

h2 {
  margin: 0;
  color: var(--cream);
  font-family: var(--font-display);
  font-size: clamp(46px, 11vw, 96px);
  font-weight: 500;
  line-height: 1.02;
  letter-spacing: 0;
}

.finale-message {
  max-width: 560px;
  margin: 24px auto 30px;
  color: var(--muted);
  line-height: 1.8;
}

.replay-button {
  min-height: 46px;
  padding: 0 20px;
  border-radius: 6px;
  color: #140d12;
  background: var(--gold);
  font-weight: 600;
}
</style>
