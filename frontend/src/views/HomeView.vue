<script setup lang="ts">
import { onMounted, ref } from "vue";
import LoadingOverlay from "../components/LoadingOverlay.vue";
import TopNav from "../components/TopNav.vue";
import StarField from "../components/StarField.vue";
import Balloons from "../components/Balloons.vue";
import MusicButton from "../components/MusicButton.vue";
import HeroSection from "../components/HeroSection.vue";
import CakeSection from "../components/CakeSection.vue";
import BlessingSection from "../components/BlessingSection.vue";
import MessageWall from "../components/MessageWall.vue";
import LetterSection from "../components/LetterSection.vue";
import FinaleSection from "../components/FinaleSection.vue";
import { useBirthdayStore } from "../stores/birthday";

const store = useBirthdayStore();
const ready = ref(false);

function finishLoading() {
  ready.value = true;
  window.dispatchEvent(new Event("birthday:loading-done"));
}

onMounted(() => {
  store.initialize();
});
</script>

<template>
  <div class="site-shell">
    <StarField />
    <Balloons />
    <MusicButton />
    <TopNav />
    <LoadingOverlay @done="finishLoading" />

    <template v-if="ready">
      <HeroSection />
      <CakeSection />
      <BlessingSection />
      <MessageWall />
      <LetterSection />
      <FinaleSection />
    </template>
  </div>
</template>
