<template>
  <ErrorIndicator />
  <main>
    <RouterView />
  </main>
</template>

<style lang="scss">
main {
  min-height: 100vh;
  background-image: url('~/assets/img/background-photo.webp');
  background-attachment: fixed;
  background-size: cover;
}
</style>
