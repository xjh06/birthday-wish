<script setup lang="ts">
import { LETTER_CONTENT } from "../config/site";
</script>

<template>
  <section class="letter-section section">
    <div class="section-inner letter-inner">
      <p class="eyebrow">A letter for you</p>
      <article class="letter-paper">
        <header>
          <p class="letter-greeting">{{ LETTER_CONTENT.greeting }}</p>
        </header>

        <div class="letter-body">
          <p v-for="(paragraph, index) in LETTER_CONTENT.paragraphs" :key="index">
            {{ paragraph }}
          </p>
        </div>

        <footer>
          <p class="letter-closing">{{ LETTER_CONTENT.closing }}</p>
          <p class="letter-signature">{{ LETTER_CONTENT.signature }}</p>
        </footer>
      </article>
    </div>
  </section>
</template>

<style scoped>
.letter-section {
  padding-top: 40px;
  padding-bottom: 96px;
}

.letter-inner {
  max-width: 760px;
}

.eyebrow {
  color: var(--gold);
}

.letter-paper {
  position: relative;
  padding: clamp(34px, 8vw, 68px) clamp(24px, 7vw, 64px);
  border-radius: 4px;
  color: #57433f;
  background-color: #f5ecd8;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.28), rgba(255, 255, 255, 0.28)),
    repeating-linear-gradient(
      to bottom,
      transparent 0,
      transparent 31px,
      rgba(143, 112, 80, 0.13) 31px,
      rgba(143, 112, 80, 0.13) 32px
    );
  border: 1px solid rgba(98, 72, 53, 0.13);
  box-shadow: 0 26px 72px rgba(0, 0, 0, 0.32);
}

.letter-paper::before {
  content: "";
  position: absolute;
  inset: 10px;
  border: 1px solid rgba(120, 87, 63, 0.09);
  border-radius: 2px;
  pointer-events: none;
}

.letter-greeting {
  position: relative;
  margin: 0 0 34px;
  color: #4f342e;
  font-family: var(--font-display);
  font-size: clamp(25px, 6vw, 39px);
  line-height: 1.45;
}

.letter-body {
  position: relative;
  display: grid;
  gap: 18px;
}

.letter-body p {
  margin: 0;
  text-indent: 2em;
  font-family: var(--font-display);
  font-size: clamp(16px, 4vw, 20px);
  line-height: 2.15;
  letter-spacing: 0;
  color: #58453f;
}

.letter-body p:nth-child(6) {
  text-indent: 0;
  color: #9c5a3d;
}

.letter-paper footer {
  position: relative;
  margin-top: 36px;
  display: grid;
  gap: 8px;
  text-align: right;
}

.letter-closing {
  margin: 0;
  white-space: pre-line;
  color: #6a5047;
  font-family: var(--font-display);
  font-size: clamp(16px, 4vw, 19px);
  line-height: 2;
}

.letter-signature {
  margin: 8px 0 0;
  white-space: pre-line;
  color: #a04f3c;
  font-family: var(--font-display);
  font-size: clamp(19px, 5vw, 26px);
  line-height: 1.45;
}

@media (max-width: 640px) {
  .letter-paper {
    padding: 30px 20px 34px;
  }

  .letter-body {
    gap: 14px;
  }
}
</style>
