<script setup lang="ts">
// Component logic will go here
</script>

<template>
  <header class="header">
    <div class="container">
      <div class="header__logo">
        <img src="@/assets/images/logo.png" alt="LISSE-SHOP Logo" class="header__logo-image" />
        <span class="header__logo-text">LISSE-SHOP</span>
      </div>
      <nav class="header__nav">
        <a href="/" class="header__nav-link">О НАС</a>
        <a href="/catalog" class="header__nav-link">КАТАЛОГ</a>
        <a href="/cart" class="header__nav-link">КОРЗИНА</a>
        <a href="/orders" class="header__nav-link">МОИ ЗАКАЗЫ</a>
      </nav>
    </div>
  </header>

  <section class="hero">
    <div class="container">
      <div class="hero__content">
        <h1 class="hero__title">LISSE-SHOP</h1>
        <p class="hero__subtitle">
          Забудьте о запутанных проводах и наслаждайтесь кристально чистым звуком наших беспроводных
          наушников — идеальное сочетание стиля, комфорта и инновационных технологий.
        </p>
      </div>
      <img src="@/assets/images/airpods.png" alt="Беспроводные наушники" class="hero__image" />
    </div>
  </section>

  <section class="about">
    <div>
      <h2 class="about__title" id="about">О НАС</h2>
    </div>
    <div class="container">
      <div class="about__content">
        <img src="@/assets/images/about.png" alt="Лиса в наушниках" class="about__image" />
        <div class="about__text">
          «<span class="about__highlight">lisse-shop</span>» — Магазин наушников и техники для
          ценителей качественного звука. Мы открылись в 2023 году и стремимся предложить вам лучший
          выбор продукции и сервиса. Доверьтесь нам в выборе техники и наслаждайтесь качественными
          технологиями вместе lisse-shop!
        </div>
      </div>
    </div>
  </section>

  <footer class="footer">
    <div class="container">
      <p class="footer__copyright">Все права защищены</p>
      <a href="https://t.me/lisse_shop" class="footer__telegram">Наш Telegram</a>
    </div>
  </footer>
</template>

<style scoped>
@import "@/assets/css/styles.css";
</style>
