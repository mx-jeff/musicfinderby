async function getMusic(music) {
    const data = []

    await fetch(`http://127.0.0.1:5000/s/${music}`)
        .then(response => data.push(response))
        .catch(erro => data.push(erro))
    
    return data
}

export default getMusic