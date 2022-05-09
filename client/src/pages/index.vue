<template>
  <div>
    <Header>
      <HeaderButton href="login">
        Log In
      </HeaderButton>
      <HeaderButton href="signup" fg="#111a2d" bg="#9e6dee">
        Sign up
      </HeaderButton>
    </Header>
  </div>
  <ContentBlock />
</template>

<route lang="yaml">
meta:
  layout: landing
</route>
