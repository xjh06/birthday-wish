<script setup lang="ts">
import { PHOTO_ITEMS } from "../config/site";
</script>

<template>
  <section class="album-section section">
    <div class="section-inner album-header">
      <p class="eyebrow">Our moments</p>
      <h2>时光相册</h2>
      <p class="album-note">横向滑动，翻看那些被保存下来的日子。</p>
    </div>

    <div class="album-scroll">
      <article v-for="(photo, index) in PHOTO_ITEMS" :key="index" class="photo-card glass-card">
        <div class="photo-visual" :class="{ 'has-image': photo.src }">
          <img v-if="photo.src" :src="photo.src" :alt="photo.alt" loading="lazy" />
          <div v-else class="photo-placeholder" :style="{ background: `linear-gradient(145deg, ${photo.gradient[0]}, ${photo.gradient[1]})` }">
            <span>{{ index + 1 }}</span>
          </div>
        </div>
        <div class="photo-meta">
          <time>{{ photo.date }}</time>
          <p>{{ photo.caption }}</p>
        </div>
      </article>
    </div>
  </section>
</template>

<style scoped>
.album-section {
  padding-top: 40px;
  padding-bottom: 80px;
}

.album-header {
  margin-bottom: 28px;
}

h2 {
  margin: 0;
  color: var(--cream);
  font-family: var(--font-display);
  font-size: clamp(34px, 8vw, 66px);
  font-weight: 500;
  line-height: 1.08;
  letter-spacing: 0;
}

.album-note {
  margin: 14px 0 0;
  color: var(--muted);
  font-size: 14px;
}

.album-scroll {
  display: flex;
  gap: 18px;
  width: calc(100vw - 32px);
  margin-left: max(16px, calc((100vw - 1120px) / 2));
  overflow-x: auto;
  overscroll-behavior-x: contain;
  padding: 12px 24px 26px 0;
  scroll-snap-type: x mandatory;
  scrollbar-width: none;
}

.album-scroll::-webkit-scrollbar {
  display: none;
}

.photo-card {
  flex: 0 0 min(82vw, 300px);
  scroll-snap-align: center;
  overflow: hidden;
  border-radius: 8px;
}

.photo-card:nth-child(2) {
  transform: translateY(24px);
}

.photo-card:nth-child(3) {
  transform: translateY(-12px);
}

.photo-visual {
  height: min(58vw, 320px);
  overflow: hidden;
  background: #141b2d;
}

.photo-visual img,
.photo-placeholder {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.photo-placeholder {
  display: grid;
  place-items: center;
  color: rgba(255, 255, 255, 0.7);
  font-family: var(--font-display);
  font-size: 56px;
}

.photo-meta {
  padding: 16px 18px 18px;
}

time {
  color: var(--gold);
  font-size: 11px;
  letter-spacing: 0.14em;
}

p {
  margin: 8px 0 0;
  color: var(--muted);
  font-size: 14px;
}

@media (min-width: 760px) {
  .album-scroll {
    margin-left: max(20px, calc((100vw - 1120px) / 2));
  }

  .photo-card {
    flex-basis: 320px;
  }

  .photo-visual {
    height: 320px;
  }
}
</style>
