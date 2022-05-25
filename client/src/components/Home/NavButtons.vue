<script setup lang="ts">
import useAuthStore from '~/store/useAuth'

const auth = useAuthStore()
const router = useRouter()
const { t } = useI18n()

const showUserMenu = ref(false)
const showNotesMenu = ref(false)
</script>

<template>
  <div class="block">
    <section class="user-menu">
      <header class="user-data" @click="showUserMenu = !showUserMenu">
        <user-profile-picture class="avatar" alt="Avatar" />
        <h3>{{ auth.user.username }}</h3>
      </header>
      <nav v-if="showUserMenu">
        <router-link to="/settings">
          {{ t('index.home.side-buttons.settings') }}
        </router-link>
        <button class="logout" @click="auth.logout().then(() => { $router.go(0) })">
          {{ t('index.home.side-buttons.log-out') }}
        </button>
      </nav>
    </section>
    <div class="display_with_button">
      <button class="standard_button" @click="router.push('/note/create')">
        <div class="i-carbon:add" />{{ t('index.home.side-buttons.add-notes') }}
      </button>
      <a><button class="standard_button">
        <div class="i-carbon:arrow-right" />{{ t('index.home.side-buttons.explore') }}
      </button></a>
      <!-- Not yet!! -->
      <!-- <a><button class="standard_button">
        <div class="i-carbon:user-avatar-filled-alt" /> Subscriptions
      </button></a> -->
      <a><button class="standard_button">
        <div class="i-carbon:folder" />{{ t('index.home.side-buttons.my-notes') }}
      </button></a>
    </div>
  </div>
  <div v-if="showNotesMenu">
    <div class="my_notes_popup">
      <div class="header_for_pop_up_acc">
        All your notes:
        <a class="close" href="#">&times;</a>
      </div>
      <div class="content">
        <ul
          style=" list-style-type: none;
                max-height: 350px;
                overflow-y: auto"
        >
          <!-- {% for note in notes %} -->
          <li style="height: 30px;line-height: 30px;">
            <a href="note.id">note.title</a>
          </li>
          <!-- {% endfor %} -->
        </ul>
      </div>
    </div>
  </div>
</template>
<style scoped lang="scss">
@import "../../assets/scss/standard-button.scss";

.standard_button {
  @include standard-button;
}

.block {
  color: white;
  font-family: 'ClearSans-Regular';
  display: inline-block;
  position: fixed;
  width: 20%;
  right: 15px;
  top: 15px;
}

.user-menu {
  background-color: #465586;
  border-radius: 10px;
  overflow: hidden;
  margin: 25px 0;

  .user-data {
    display: flex;
    align-items: center;
    padding: 10px;
    background-color: #223153;
    transition-duration: 0.2s;

    &:hover {
      background-color: rgba(70, 85, 134, 0.7);
      cursor: pointer;
    }

    h3 {
      font-size: 28px;
      margin-left: 30px;
    }

    img {
      padding: 5px;
      border-radius: 50%;
      width: 100px;
      height: 100px;
      object-fit: cover;
    }
  }

  nav {
    $button-count: 2;
    $button-height: 50px;

    z-index: -1;
    animation-duration: 0.2s;
    animation-name: slidein;

    a,
    button {
      display: block;
      width: 100%;
      text-align: center;
      line-height: $button-height;
      font-family: "ClearSans-Light";
      font-size: 20px;
      transition-duration: 0.3s;
      user-select: none;

      &:hover {
        background-color: #617299;
      }

      &.logout:hover {
        background-color: #fa3b3b;
      }
    }

    @keyframes slidein {
      from {
        height: 0;
      }

      to {
        height: $button-count * $button-height;
      }
    }
  }
}

.display_with_button div {
  color: #F1F7ED;
}

.display_with_button button {
  width: 100%;
}

.b_my_notes:focus {
  background-color: var(--primary-color);
}

.display_with_button {
  display: inline-block;
  width: 100%;
}

.profile_popup {
  margin: 70px auto;
  background: #09132B;
  border-radius: 10px;
  width: 20.2%;
  position: relative;
  top: -3.4%;
  left: 39.69%;
  padding-top: 20px;
  color: white;

  .header_for_pop_up {
    font-family: 'ClearSans-Regular';
    color: white;
    background-color: #09132B;
    text-align: left;
    padding: 10px;
    border-radius: 10px;
    font-size: 20px;
    margin: 0px 6% 0px 4%;
    color: #F1F7ED;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .close {
    position: absolute;
    top: 20px;
    right: 20px;
    transition: all 200ms;
    font-size: 120%;
    font-weight: bold;
    text-decoration: none;
    color: #F1F7ED;
  }

  .close:hover {
    color: #303D67;
  }

  .content {
    text-align: left;
    font-family: 'ClearSans-Regular';
    color: white;
    padding: 0px 3%;
    max-height: 40%;
    overflow: auto;
    margin-left: 4%;
    background-color: #09132B;
    border-radius: 0 0 10px 10px;
  }

  .header_for_pop_up_acc {
    display: flex;
    font-family: 'ClearSans-Regular';
    color: white;
    background-color: #303D67;
    text-align: right;

    padding: 10px;
    border-radius: 10px;
    font-size: 20px;
    margin: 0px 60px 20px 20px;
    color: #F1F7ED;
  }
}

.my_notes_popup {
  margin: 70px auto;
  background: #303D67;
  border-radius: 10px;
  width: 20.5%;
  position: relative;
  top: 29%;
  left: 39.8%;
  padding-top: 20px;

  .header_for_pop_up {
    display: flex;
    font-family: 'Altone-SemiBold';
    color: white;
    background-color: #303D67;
    text-align: left;

    padding: 10px;
    border-radius: 10px;
    font-size: 20px;
    margin: 0px 60px 20px 20px;
    color: #F1F7ED;
  }

  .close {
    position: absolute;
    top: 20px;
    right: 20px;
    transition: all 200ms;
    font-size: 190%;
    font-weight: bold;
    text-decoration: none;
    color: #F1F7ED;
  }

  .close:hover {
    color: #09132B;
  }

  .content {
    text-align: left;
    font-family: 'ClearSans-Regular';
    color: white;
    padding: 0px 3%;
    height: 10%;
    overflow: auto;
    background-color: #303D67;
    border-radius: 0 0 10px 10px;

  }

  .header_for_pop_up_acc {
    display: flex;
    font-family: 'ClearSans-Regular';
    color: white;
    background-color: #303D67;
    text-align: right;

    padding: 10px;
    border-radius: 10px;
    font-size: 20px;
    margin: 0px 60px 20px 20px;
    color: #F1F7ED;
  }
}
</style>
