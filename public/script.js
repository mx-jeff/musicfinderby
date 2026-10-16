/*
main functions
@author: DZOJeff
*/
import { validate_input, AJAX, alert_bootstrap, load_site } from './function.js';
import { BASE_LINK } from "./const.js";


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
            info.innerHTML = alert_bootstrap('Digite um nome de música!', 'alert dz0-box')
            send.disabled = false   // antes ficava travado
            return
        }

        send.innerHTML = "Aguarde..."
        info.innerHTML = alert_bootstrap(`Extraindo ${link}` ,'alert dz0-box')
        AJAX(link, info, send) 
    });
}