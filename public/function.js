import { BASE_LINK } from "./const.js";


/**
 * 
 * @returns log of start
 */
export async function load_site(send, input, info){
    send.disabled = true
    input.disabled = true
    info.innerHTML = alert_bootstrap('Iniciando site...', 'alert dz0-box')

    console.log('Carregando...')
    const resp = await fetch(`${BASE_LINK}/api`)
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
    const cd = response.headers.get('Content-Disposition')
    if (!cd) return 'file'

    // versão codificada (UTF-8), tem prioridade
    const encoded = cd.match(/filename\*\s*=\s*UTF-8''([^;]+)/i)
    if (encoded) {
        try { return decodeURIComponent(encoded[1]) } catch (e) {}
    }

    // versão simples
    const plain = cd.match(/filename\s*=\s*"?([^";]+)"?/i)
    return plain ? plain[1] : 'file'
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

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

/**
 * Call AJAX API scrapper and return file 
 * @param {string} url 
 * @param {string} info 
 * @param {string} send 
 */
export async function AJAX(music, info, send) {
    try {
        const s = await fetch(`${BASE_LINK}/search/${encodeURIComponent(music)}`)
        if (!s.ok) throw "Erro ao buscar a música!"
        const { url } = await s.json()

        info.innerHTML = alert_bootstrap('Baixando e convertendo...', 'alert dz0-box')
        const d = await fetch(`${BASE_LINK}/download/?url=${encodeURIComponent(url)}`)
        if (!d.ok) throw "Erro ao iniciar o download!"

        let resp
        while (true) {
            resp = await fetch(`${BASE_LINK}/music`)
            if (resp.status !== 202) break
            await sleep(2000)
        }
        if (!resp.ok) throw "Música não disponível!"

        const filename = getFilename(resp).replace(/"/g, '')
        const blob = await resp.blob()
        const objUrl = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.style.display = 'none'
        a.href = objUrl
        a.download = filename
        document.body.appendChild(a)
        a.click()
        a.remove()
        window.URL.revokeObjectURL(objUrl)

        info.innerHTML = alert_bootstrap('<strong>Successo!</strong> Arquivo baixado.', 'alert btn-success dz0-f700')
    } catch (err) {
        info.innerHTML = alert_bootstrap(err, 'alert btn-danger dz0-f700')
    } finally {
        send.disabled = false
        send.innerHTML = "Extrair"
    }
}
