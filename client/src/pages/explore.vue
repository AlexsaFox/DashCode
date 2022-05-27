<template>
  <div class="block_for_header">
    <p class="header">
      New public notes
    </p>
    <hr class="line_for_header">
  </div>
  <Notes />
  <OneButtonBack />
</template>

<style>
.block_for_header {
  display: inline-block;
  width: 72%;
  margin-top: 70px;
  margin-left: 10%;
}
.block_for_header .header{
    color:white;
    font-size:120%;
    font-family: 'ClearSans-Regular';
}
.block_for_header .line_for_header{
    color: #5B6B98;
    background-color: #5B6B98;
    border-width: 2px;
    border-radius: 5px;
    width: 85%;
    font-size: 4px;
    margin-right: 20%;
    margin-bottom: 2%;
}
</style>

<route lang="yaml">
meta:
  requiresAuth: true
</route>
