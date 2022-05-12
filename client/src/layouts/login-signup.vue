<template>
  <ErrorIndicator />
  <main>
    <div class="landing-form-container">
      <LoginSignupText />
      <RouterView />
    </div>
  </main>
</template>

<style scoped lang="scss">
main {
  min-height: 100vh;
  background-image: url('~/assets/img/background-photo.webp');
  background-attachment: fixed;
  background-size: cover;
}
.landing-form-container {
  height: 100vh;
  max-width: 1200px;
  margin: auto;
  display: flex;
  justify-content: space-around;
  align-items: center;
}
</style>
