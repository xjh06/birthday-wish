<script setup lang="ts">
import { computed, ref } from "vue";
import { useBirthdayStore } from "../stores/birthday";

const store = useBirthdayStore();
const senderName = ref("");
const relationship = ref("");
const content = ref("");
const submitted = ref(false);
const errorText = ref("");

const isValid = computed(() => {
  return senderName.value.trim().length >= 2 && content.value.trim().length >= 2;
});

async function submit() {
  if (!isValid.value || store.submitting) return;
  errorText.value = "";

  const ok = await store.submitMessage({
    senderName: senderName.value.trim(),
    relationship: relationship.value.trim() || "朋友",
    content: content.value.trim(),
  });

  if (ok) {
    submitted.value = true;
    content.value = "";
    window.setTimeout(() => {
      submitted.value = false;
    }, 2400);
  } else {
    errorText.value = "留言没有送达，请稍后再试。";
  }
}

function like(message: any) {
  store.toggleLike(message);
}
</script>

<template>
  <section id="blessings" class="message-section section">
    <div class="section-inner message-inner">
      <p class="eyebrow">Leave a note</p>
      <h2>朋友留言墙</h2>

      <div class="message-layout">
        <form class="message-form glass-card" @submit.prevent="submit">
          <label>
            <span>你的名字</span>
            <input v-model="senderName" type="text" maxlength="30" placeholder="例如：阿哲" required />
          </label>
          <label>
            <span>你们的关系</span>
            <input v-model="relationship" type="text" maxlength="30" placeholder="例如：多年好友" />
          </label>
          <label>
            <span>祝福内容</span>
            <textarea v-model="content" maxlength="500" rows="4" placeholder="写一句想对寿星说的话" required></textarea>
          </label>
          <div class="form-actions">
            <span v-if="submitted" class="success-text">祝福已经送到</span>
            <span v-else-if="errorText" class="error-text">{{ errorText }}</span>
            <span v-else></span>
            <button type="submit" :disabled="!isValid || store.submitting">
              {{ store.submitting ? "发送中" : "送出祝福" }}
            </button>
          </div>
        </form>

        <div class="message-list">
          <article v-for="message in store.messages" :key="message.id" class="message-card glass-card">
            <div class="message-head">
              <div>
                <strong>{{ message.senderName }}</strong>
                <span>{{ message.relationship }}</span>
              </div>
              <time>{{ new Date(message.createdAt).toLocaleDateString("zh-CN") }}</time>
            </div>
            <p>{{ message.content }}</p>
            <button class="like-button" type="button" @click="like(message)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 0 0-7.8 7.8l1.1 1.1L12 21l7.8-7.5 1.1-1.1a5.5 5.5 0 0 0-.1-7.8Z"></path>
              </svg>
              {{ message.likeCount }}
            </button>
          </article>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.message-section {
  padding-top: 60px;
  padding-bottom: 100px;
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

.message-layout {
  display: grid;
  grid-template-columns: minmax(280px, 0.8fr) 1.2fr;
  gap: 22px;
  margin-top: 36px;
  align-items: start;
}

.message-form {
  display: grid;
  gap: 18px;
  padding: 22px;
  border-radius: 8px;
  position: sticky;
  top: 20px;
}

label {
  display: grid;
  gap: 8px;
}

label span {
  color: var(--muted);
  font-size: 12px;
  letter-spacing: 0.06em;
}

input,
textarea {
  width: 100%;
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 12px 13px;
  color: var(--cream);
  background: rgba(255, 255, 255, 0.06);
  outline: 0;
  resize: vertical;
}

input:focus,
textarea:focus {
  border-color: rgba(233, 195, 107, 0.72);
}

.form-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.success-text {
  color: var(--teal);
  font-size: 12px;
}

.error-text {
  color: var(--coral);
  font-size: 12px;
}

.form-actions button {
  min-height: 40px;
  padding: 0 17px;
  border-radius: 6px;
  color: #140d12;
  background: var(--gold);
  font-weight: 600;
}

.form-actions button:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.message-list {
  display: grid;
  gap: 14px;
}

.message-card {
  padding: 18px;
  border-radius: 8px;
}

.message-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.message-head strong {
  display: block;
  color: var(--cream);
  font-size: 15px;
}

.message-head span {
  display: block;
  margin-top: 3px;
  color: var(--gold);
  font-size: 12px;
}

time {
  color: var(--muted);
  font-size: 11px;
  white-space: nowrap;
}

.message-card p {
  margin: 16px 0;
  color: rgba(255, 248, 238, 0.78);
  line-height: 1.75;
  font-size: 14px;
}

.like-button {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 10px;
  border-radius: 6px;
  color: var(--coral);
  background: rgba(241, 131, 120, 0.12);
  font-size: 12px;
}

.like-button svg {
  width: 15px;
  height: 15px;
}

@media (max-width: 820px) {
  .message-layout {
    grid-template-columns: 1fr;
  }

  .message-form {
    position: static;
  }
}
</style>
