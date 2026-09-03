<script setup lang="ts">
function greeting() {
  const hour = new Date().getHours();
  if (hour >= 5 && hour < 11) return "早上好";
  if (hour >= 11 && hour < 13) return "中午好";
  if (hour >= 13 && hour < 18) return "下午好";
  return "晚上好";
}
</script>

<template>
  <header class="top-nav" role="banner">
    <a class="brand" href="#home" aria-label="回到顶部">
      <span class="brand-mark" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="3"></circle>
          <path d="M12 2v3M12 19v3M2 12h3M19 12h3"></path>
        </svg>
      </span>
      <span class="brand-text">ZST&nbsp;DAY</span>
    </a>

    <nav class="nav-pills" aria-label="导航">
      <a href="#home" class="pill">首页</a>
      <a href="#story" class="pill">故事</a>
      <a href="#gift" class="pill">礼物</a>
      <a href="#blessings" class="pill">祝福</a>
    </nav>

    <span class="greeting">{{ greeting() }}</span>
  </header>
</template>

<style scoped>
.top-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 50;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  gap: 16px;
  padding: max(16px, env(safe-area-inset-top)) max(22px, env(safe-area-inset-right)) 16px
    max(22px, env(safe-area-inset-left));
  pointer-events: none;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  pointer-events: auto;
  text-decoration: none;
  color: var(--ink);
}

.brand-mark {
  display: grid;
  place-items: center;
  width: 34px;
  height: 34px;
  border-radius: 9px;
  color: var(--teal);
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.14);
  backdrop-filter: blur(12px);
}

.brand-mark svg {
  width: 18px;
  height: 18px;
}

.brand-text {
  font-family: var(--font-body);
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 0.2em;
}

.nav-pills {
  display: flex;
  gap: 6px;
  padding: 6px;
  border-radius: 999px;
  background: rgba(10, 18, 38, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.14);
  backdrop-filter: blur(14px);
  pointer-events: auto;
}

.pill {
  padding: 8px 18px;
  border-radius: 999px;
  color: var(--muted);
  font-size: 14px;
  letter-spacing: 0.04em;
  text-decoration: none;
  transition: color 0.2s ease, background 0.2s ease;
}

.pill:hover {
  color: var(--ink);
  background: rgba(255, 255, 255, 0.1);
}

.greeting {
  justify-self: end;
  color: var(--ink);
  font-size: 14px;
  letter-spacing: 0.06em;
}

@media (max-width: 720px) {
  .top-nav {
    grid-template-columns: auto 1fr;
  }

  .nav-pills {
    grid-column: 1 / -1;
    justify-self: center;
    order: 3;
    margin-top: 8px;
  }

  .pill {
    padding: 8px 14px;
    font-size: 13px;
  }

  .greeting {
    justify-self: end;
  }
}
</style>
