/*
main functions
@author: DZOJeff
*/


function validate_input(input){
    if(input == '') {
        return false
    }
    
    // if(input.split('/')[0] != "https:") {
    //     return false;
    // }
    
    return true
}


/**
 * extract download name from headers
 * @param {string} res 
 * @returns filename of file
 */

function getFilename(response){
    if (response.headers.get('Content-Disposition') == null) return 'file'
    return response.headers.get('Content-Disposition').split('filename=')[1];
}

/**
 * send alert based on text and params
 * @param {string} text 
 * @param {string} tag 
 * @returns html element alert
 */
function alert_bootstrap(text, tag){
    return `
        <div class='${tag} text-center'>
            ${text}
        </div>
    `
}

/**
 * Call AJAX API scrapper and return file 
 * @param {string} url 
 * @param {string} info 
 * @param {string} send 
 */
function AJAX(url, info, send){
    fetch(url)
    .then(resp => {
        if (resp.status == 500) throw "Erro de servidor!"

        const filename = getFilename(resp)
        resp.blob().then(blob => {
            info.innerHTML = alert_bootstrap('<strong>Successo!</strong> Baixando arquivo', 'alert alert-success')
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            // the filename you want
            a.download = filename
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            
            // UX
            info.innerHTML = alert_bootstrap('<strong>Successo!</strong> Arquivo baixado.', 'alert alert-success')
            send.innerHTML = "Extrair"
        })
    })
    .catch((err) => {
        info.innerHTML = alert_bootstrap(err, 'alert alert-danger')
    });
}


window.onload = () => {
    const send = document.querySelector('button#send')
    const input = document.querySelector('input#product')
    const form = document.querySelector('form')
    const info = document.querySelector('#info')

    form.addEventListener('submit', async (e) => {
        e.preventDefault()
        info.innerHTML = ''

        let link = input.value
        if(!validate_input(link)){
            info.innerHTML = alert_bootstrap('Digite um link válido!', 'alert alert-danger')
            return
        }

        send.innerHTML = "Aguarde..."
        info.innerHTML = alert_bootstrap(`Extraindo ${link}` ,'alert alert-info')
        AJAX(`http://musicfinderby2.herokuapp.com/search/${link}`, info, send)
    });
}