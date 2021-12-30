/**
 * 
 * @returns log of start
 */
export async function load_site(send, input, info){
    send.disabled = true
    input.disabled = true
    info.innerHTML = alert_bootstrap('Iniciando site...', 'alert dz0-box')

    console.log('Carregando...')
    const resp = await fetch('http://musicfinderby2.herokuapp.com')
    if (resp.status == 500) return
    if (resp.status == 200){
        info.innerHTML = alert_bootstrap('Bem vindo! Digite uma música', 'alert btn-success dz0-f700')
        send.disabled = false
        input.disabled = false
    }
}

/**
 * 
 * @param {input to validate} input 
 * @returns boolean
 */
export function validate_input(input){
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

export function getFilename(response){
    if (response.headers.get('Content-Disposition') == null) return 'file'
    return response.headers.get('Content-Disposition').split('filename=')[1];
}

/**
 * send alert based on text and params
 * @param {string} text 
 * @param {string} tag 
 * @returns html element alert
 */
export function alert_bootstrap(text, tag){
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
export async function AJAX(music, info, send){
    
    try {
        const resp = await fetch(music)
    
        if (resp.status == 500) throw "Erro de servidor!"
        const filename = getFilename(resp)
        info.innerHTML = alert_bootstrap('Baixando arquivo...', 'alert dz0-box')
        
        const blob = await resp.blob()

        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        // the filename you want
        console.log(filename.replace('./','').replace(/"/g,''))
        if (filename == "file") {
            info.innerHTML = alert_bootstrap(err, 'alert btn-danger dz0-f700')
            return
        }
        a.download = filename.replace('./','').replace(/"/g,'')
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        
        // UX
        info.innerHTML = alert_bootstrap('<strong>Successo!</strong> Arquivo baixado.', 'alert btn-success dz0-f700')
        send.disabled = false
        send.innerHTML = "Extrair"
    }
    catch(err) {
        send.disabled = false
        send.innerHTML = "Extrair"
        info.innerHTML = alert_bootstrap(err, 'alert btn-danger dz0-f700')
    }
}
