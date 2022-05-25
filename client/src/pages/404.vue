<template>
  <div class="page_404">
    <div class="content">
      <h1 class="error_heading">
        Error 404
      </h1>
      <p class="text_error">
        text error
      </p>
      <div class="stroke">
        <a class="a_back">Go Back</a>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.page_404 {
  display: flex;
  justify-content: center;

  .text_error {
    text-align: center;
    color: white;
    font-size: 30px;
  }

  .error_heading {
    font-family: 'ClearSans-Bold';
    color: white;
    font-size: 80px;
    width: auto;
    margin: 0%;
    text-align: center;
  }

  .stroke {
    display: flex;
    justify-content: flex-end;

    .a_back {
      color: #9e6dee;
      font-size: 25px;
    }

  }

}
</style>
