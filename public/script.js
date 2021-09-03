/*
main functions
@author: DZOJeff
*/
import { validate_input, AJAX, alert_bootstrap, load_site, getFilename } from './function.js';


window.onload = () => {
    const send = document.querySelector('button#send')
    const input = document.querySelector('input#product')
    const form = document.querySelector('form')
    const info = document.querySelector('#info')

    load_site(send, input, info)

    form.addEventListener('submit', async (e) => {
        e.preventDefault()
        info.innerHTML = ''
        send.disabled = true

        let link = input.value
        if(!validate_input(link)){
            info.innerHTML = alert_bootstrap('Digite um link válido!', 'alert dz0-box')
            return
        }

        send.innerHTML = "Aguarde..."
        info.innerHTML = alert_bootstrap(`Extraindo ${link}` ,'alert dz0-box')
        AJAX(`http://musicfinderby2.herokuapp.com/search/${link}`, info, send)
    });
}