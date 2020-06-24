async function getMusic(music) {
    await fetch(`http://127.0.0.1:5000/s/${music}`)
        .then(response => console.log(response))
        .catch(erro => musics.push(erro))
}

export default getMusic