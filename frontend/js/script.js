import api from './api.js'

const musica = document.querySelector('#musica')
const search = document.querySelector('#search')
const status = document.querySelector('footer')

search.addEventListener('submit', e => {
    e.preventDefault()
    status.textContent = 'Aguarde...'
    api(musica.value)
})