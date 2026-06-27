function adicionarCompetencia() {
    const input = document.getElementById('input_nova_comp');
    const nomeComp = input.value.trim();
    const lista = document.getElementById('lista-competencias'); // Busca o contêiner correto
    
    if (nomeComp === "") {
        alert("Digite o nome da competência!");
        return;
    }
    
    // Verificar se já existe na lista atual
    const itens = lista.querySelectorAll('.competencia-item');
    let existe = false;
    
    itens.forEach(item => {
        const label = item.querySelector('label');
        if (label && label.textContent.toLowerCase().trim() === nomeComp.toLowerCase()) {
            existe = true;
            const checkbox = item.querySelector('input[type="checkbox"]');
            if (checkbox) checkbox.checked = true;
        }
    });
    
    if (existe) {
        alert("Esta competência já existe! Foi selecionada automaticamente.");
        input.value = "";
        return;
    }
    
    // Criação dinâmica da nova tag marcada
    const novoId = 'nova_' + Date.now();
    const novoItem = document.createElement('div');
    novoItem.className = 'competencia-item';
 

novoItem.innerHTML = `
    <input type="checkbox" name="competencias_novas_marcadas" value="${nomeComp.replace(/["']/g, '&quot;')}" id="${novoId}" checked>
    <label for="${novoId}">${nomeComp}</label>
`;
    lista.appendChild(novoItem);
    input.value = "";
    input.focus();
}


document.addEventListener('DOMContentLoaded', function() {
    const inputComp = document.getElementById('input_nova_comp');
    if (inputComp) {
        inputComp.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault(); // Evita que o formulário principal seja enviado
                adicionarCompetencia();
            }
        });
    }
});

function formatar(abre, fecha) {
    const textarea = document.getElementById('descricao');
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const texto = textarea.value;
    const textoSelecionado = texto.substring(start, end);
    
    if (textoSelecionado) {
        // Aplica formatação ao texto selecionado
        const novoTexto = texto.substring(0, start) + abre + textoSelecionado + fecha + texto.substring(end);
        textarea.value = novoTexto;
        textarea.focus();
        textarea.setSelectionRange(start + abre.length, end + abre.length);
    } else {
        // Insere marcadores
        const novoTexto = texto.substring(0, start) + abre + fecha + texto.substring(end);
        textarea.value = novoTexto;
        textarea.focus();
        textarea.setSelectionRange(start + abre.length, start + abre.length);
    }
}

function formatarLista(marcador) {
    const textarea = document.getElementById('descricao');
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const texto = textarea.value;
    const linhaAtual = texto.substring(0, start).split('\n').pop();
    const inicioLinha = start - linhaAtual.length;
    
    // Adiciona marcador no início da linha
    const novoTexto = texto.substring(0, inicioLinha) + marcador + linhaAtual + texto.substring(start);
    textarea.value = novoTexto;
    textarea.focus();
    textarea.setSelectionRange(inicioLinha + marcador.length + linhaAtual.length, inicioLinha + marcador.length + linhaAtual.length);
} 