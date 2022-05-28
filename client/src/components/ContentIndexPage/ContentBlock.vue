<script setup lang="ts">
const { t } = useI18n()
</script>

<template>
  <div class="content">
    <div class="material">
      <div class="one_of_the_titles_for_main_page">
        <h1>{{ t("index.title-1") }}</h1>
        <p>
          {{ t("index.text-1") }}
        </p>
      </div>
      <div class="picture">
        <img src="../../assets/img/landing-img-1.webp" alt="image">
      </div>
    </div>
    <div class="material">
      <div class="one_of_the_titles_for_main_page">
        <h1>{{ t("index.title-2") }}</h1>
        <p>
          {{ t("index.text-2") }}
        </p>
      </div>
      <div class="picture">
        <img src="../../assets/img/landing-img-2.webp" alt="image">
      </div>
    </div>
    <div class="material">
      <div class="one_of_the_titles_for_main_page">
        <h1>{{ t("index.title-3") }}</h1>
        <p>{{ t("index.text-3") }}</p>
      </div>
      <div class="picture">
        <img src="../../assets/img/landing-img-3.webp" alt="image">
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.content {
  display: flex;
  flex-direction: column;
  .material {
    display: flex;
    justify-content: space-between;
    background-color: rgba(255, 255, 255, 0.3);
    margin: 6% auto;
    width: 80%;
    border-radius: 20px;
    padding: 3%;
    align-items: center;
  }
}

.one_of_the_titles_for_main_page {
  color: #f1f7ed;
  font-family: "ClearSans-Bold";
  width: 50%;
  margin-right: 10%;
  h1 {
    font-size: 36px;
  }
  p {
    font-size: 22px;
    text-align: justify;
  }
}
.picture {
  width: 90%;
  img {
    object-fit: cover;
  }
}
</style>
