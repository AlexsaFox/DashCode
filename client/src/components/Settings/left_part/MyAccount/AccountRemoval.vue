<template>
  <div class="base_settings">
    <div class="account_removal">
      <h3>ACCOUNT REMOVAL</h3>
      <span>Disabling your account means you can recover it at any time after
        this action.</span>
      <div class="stroke">
        <button class="disable_account">
          Disable Account
        </button>
        <button class="delete_account">
          Delete Account
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.base_settings {
  .password h2 {
    font-family: "ClearSans-Bold";
    font-size: 20px;
    text-align: left;
  }
  .account_removal {
    h3 {
      font-family: "ClearSans-Medium";
      color: rgba(255, 255, 255, 0.6);
      font-weight: 100;
    }
    span {
      font-family: "ClearSans-Regular";
      color: rgba(255, 255, 255, 0.6);
      font-weight: 100;
      font-size: 20px;
    }
    .disable_account {
      border: 3px solid #fa3b3b;
      border-radius: 5px;
      background-color: #fa3b3b;
      color: white;
      padding: 1% 2%;
      font-family: "ClearSans-Regular";
      font-size: 20px;
      font-weight: 200;
    }
    .delete_account {
      border: 3px solid #fa3b3b;
      border-radius: 5px;
      background-color: #223153;
      color: #fa3b3b;
      padding: 1% 2%;
      font-family: "ClearSans-Regular";
      font-size: 20px;
      font-weight: 200;
      margin: 2%;
    }

  }
}
</style>
