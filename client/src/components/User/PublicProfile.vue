<script setup lang="ts">
import { getUser } from '~/utils/user'

const { t } = useI18n()

const { username } = defineProps<{ username: string }>()
const emit = defineEmits<{
  (e: 'loadingFailed'): void
}>()

const { user } = await getUser(username)
if (!user)
  emit('loadingFailed')
</script>

<template>
  <section class="user-profile">
    <section class="user-data">
      <UserProfilePicture :filename="user.profilePictureFilename ?? null" />
      <h2>{{ user.username }}</h2>
      <p>{{ t('user-profile.profile-block.amount_of_notes-label', user.notes.length) }}</p>
    </section>

    <section class="user-notes">
      <MiniNote v-for="note in user.notes" :key="note" :note="note" />
    </section>
  </section>
</template>

<style scoped lang="scss">
.user-profile {
  border: 0.1px solid transparent;

  .user-data {
    width: 70%;
    margin-left: 5%;
    margin-top: 70px;
    padding: 50px 0 20px 0;
    border-radius: 10px;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    background-color: #223153;

    img {
      $side: 250px;
      width: $side;
      height: $side;
      margin-bottom: 10px;

      border-radius: 100%;
      object-fit: cover;
      object-position: center;
    }

    h2 {
      font-family: 'ClearSans-Bold';
      font-size: 36px;
    }

    p {
      font-family: 'ClearSans-Regular';
      font-size: 18px;
    }
  }

  .user-notes {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
    width: 70%;
    margin-left: 5%;
    margin-top: 70px;
    user-select: none;
  }
}
</style>
