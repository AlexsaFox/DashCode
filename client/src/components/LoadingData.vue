<script setup lang="ts">
const size = '400px'
const color = '#5B6B98'
const ballColor = 'var(--user-color)'

const innerStyles = computed(() => {
  const sizeNumber = parseInt(size)
  return {
    'transform': `scale(${sizeNumber / 250})`,
    '--bg-color': color,
    '--ball-color': ballColor,
  }
})
const styles = computed(() => {
  return {
    width: size,
    height: size,
  }
})
</script>

<template>
  <section>
    <div :style="styles" class="spinner spinner--ping-pong">
      <div :style="innerStyles" class="spinner-inner">
        <div class="board">
          <div class="left" />
          <div class="right" />
          <div class="ball" />
        </div>
      </div>
    </div>
    <h2>Loading...</h2>
  </section>
</template>

<style scoped lang="scss">
section {
  margin-left: 5%;
  width: 70%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 80vh;

  h2 {
    font-family: "ClearSans-Regular";
    font-size: 36px;
  }
}
.spinner {
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;

  * {
    line-height: 0;
    box-sizing: border-box;
  }
}

.board {
  width: 250px;
  position: relative;
}

.left,
.right {
  height: 50px;
  width: 15px;
  background: var(--bg-color);
  display: inline-block;
  position: absolute;
}

.left {
  left: 0;
  border-radius: 10px;
  animation: ping-pong-position1 3s linear infinite;
}

.right {
  right: 0;
  border-radius: 10px;
  animation: ping-pong-position2 3s linear infinite;
}

.ball {
  width: 15px;
  height: 15px;
  border-radius: 50%;
  background: var(--ball-color);
  position: absolute;
  animation: ping-pong-bounce 3s linear infinite;
}

@keyframes ping-pong-position1 {
  0% {
    top: -60px;
  }

  25% {
    top: 0;
  }

  50% {
    top: 60px;
  }

  75% {
    top: -60px;
  }

  100% {
    top: -60px;
  }
}

@keyframes ping-pong-position2 {
  0% {
    top: 60px;
  }

  25% {
    top: 0;
  }

  50% {
    top: -60px;
  }

  75% {
    top: -60px;
  }

  100% {
    top: 60px;
  }
}

@keyframes ping-pong-bounce {
  0% {
    top: -35px;
    left: 10px;
  }

  25% {
    top: 25px;
    left: 225px;
  }

  50% {
    top: 75px;
    left: 10px;
  }

  75% {
    top: -35px;
    left: 225px;
  }

  100% {
    top: -35px;
    left: 10px;
  }
}
</style>
