<template>
  <nav>
    <div class="logo">
      <img src="../../assets/img/logo.svg">
      <p>DashCode</p>
    </div>
    <div class="buttons">
      <slot />
    </div>
  </nav>
</template>

<style scoped lang="scss">
@import url('../../assets/scss/fonts.scss');

nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #111A2D;

  $nav-padding-y: 6px;
  $nav-height: 80px;
  padding: $nav-padding-y 24px;
  height: $nav-height;

  .logo {
    display: flex;
    justify-content: flex-start;
    align-items: center;

    img {
      aspect-ratio: 1 / 1;
      height: $nav-height - 2 * $nav-padding-y;
    }

    p {
      padding: 0 18px;
      font-family: 'ClearSans-Bold';
      font-size: 40px;
      color: #fff;
    }
  }
}
</style>
