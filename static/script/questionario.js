function adicionarCompetencia() {
    const input = document.getElementById('input_nova_comp');
    const nomeComp = input.value.trim();

    const lista = document.getElementById('lista-competencias');

    if (nomeComp === "") {
        alert("Digite o nome da competência!");
        return;
    }

    // Verificar se já existe
    const itens = lista.querySelectorAll('.competencia-item');
    let existe = false;

    itens.forEach(item => {
        const label = item.querySelector('label');
        if (label && label.textContent.trim().toLowerCase() === nomeComp.toLowerCase()) {
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

    const novoId = 'nova_' + Date.now();

    const novoItem = document.createElement('div');
    novoItem.className = 'competencia-item';

    // IMPORTANTE: continua como novas_competencias
    novoItem.innerHTML = `
        <input type="checkbox"
               name="novas_competencias"
               value="${nomeComp.replace(/"/g, '&quot;')}"
               id="${novoId}"
               checked>

        <label for="${novoId}">${nomeComp}</label>
    `;

    lista.appendChild(novoItem);

    input.value = "";
    input.focus();
}