async function carregarPergunta() {
    const response = await fetch('/api/proxima_pergunta');
    const data = await response.json();

    if (data.finalizado) {
        exibirFimDeJogo(data.pontos);
        return;
    }

    document.getElementById('pergunta').innerText = data.pergunta;
    document.getElementById('categoria').innerText = `Categoria: ${data.cat}`;
    document.getElementById('progresso').innerText = `Pergunta ${data.index} de ${data.total}`;

    const containerOpcoes = document.getElementById('opcoes');
    containerOpcoes.innerHTML = '';

    data.opcoes.forEach(opcao => {
        const btn = document.createElement('button');
        btn.innerText = opcao;
        btn.onclick = () => enviarResposta(opcao);
        containerOpcoes.appendChild(btn);
    });
}

async function enviarResposta(escolha) {
    const response = await fetch('/api/verificar_resposta', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ resposta: escolha })
    });

    const result = await response.json();

    document.getElementById('placar').innerText = `Pontos: ${result.pontos_atuais}`;

    setTimeout(carregarPergunta, 500);
}

function exibirFimDeJogo(total) {
    document.getElementById('quiz-box').innerHTML = `
        <h1>FIM DE JOGO!</h1>
        <p>Você marcou ${total} pontos.</p>
        <button onclick="location.reload()">JOGAR NOVAMENTE</button>
    `;
}

window.onload = carregarPergunta;