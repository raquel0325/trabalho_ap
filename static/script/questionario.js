function adicionarCompetencia() {
    const input = document.getElementById('input_nova_comp');
    const nomeComp = input.value.trim();
    const lista = document.getElementById('lista-competencias');
    
    if (nomeComp === "") {
        alert("Digite o nome da competência!");
        return;
    }
    
    // Verificar se já existe na lista
    const itens = lista.querySelectorAll('.competencia-item');
    let existe = false;
    itens.forEach(item => {
        const label = item.querySelector('label');
        if (label && label.textContent.toLowerCase() === nomeComp.toLowerCase()) {
            existe = true;
            const checkbox = item.querySelector('input[type="checkbox"]');
            if (checkbox) checkbox.checked = true;
        }
    });
    
    if (existe) {
        alert("Esta competência já está na lista! Ela foi selecionada automaticamente.");
        input.value = "";
        return;
    }
    
    // Criar novo item (já marcado)
    const novoId = 'nova_' + Date.now();
    const novoItem = document.createElement('div');
    novoItem.className = 'competencia-item';

    
    novoItem.innerHTML = `
        <input type="checkbox" name="competencias_novas_marcadas" value="${nomeComp.replace(/"/g, '&quot;')}" id="${novoId}" checked>
        <label for="${novoId}"> ${nomeComp}</label>
    `;
    
    lista.appendChild(novoItem);
    input.value = "";
    input.focus();
    
    // Scroll para o novo item
    novoItem.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// Permitir Enter para adicionar competência
document.getElementById('input_nova_comp').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        adicionarCompetencia();
    }
});

// Validar ano
document.querySelector('input[name="ano_conclusao"]').addEventListener('input', function(e) {
    this.value = this.value.replace(/\D/g, '');
    if (this.value.length > 4) {
        this.value = this.value.slice(0, 4);
    }
});