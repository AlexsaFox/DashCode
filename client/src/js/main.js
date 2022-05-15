window.onload = () => {
  const tx = document.querySelectorAll('textarea')
  console.log(tx)
  for (const textarea of tx) {
    console.log(textarea)
    textarea.setAttribute('style', `height:${textarea.scrollHeight}px;overflow-y:hidden;`)
    textarea.addEventListener('input', OnInput, false)
  }
} 

function OnInput() {
  this.style.height = 'auto'
  this.style.height = `${this.scrollHeight}px`
}