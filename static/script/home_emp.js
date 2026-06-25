function mostrarSecao(secao) {
    // Esconde todas as seções
    const secoes = [ 'contratados'];
    secoes.forEach(sec => {
        const elemento = document.getElementById(`secao-${sec}`);
        if (elemento) elemento.style.display = 'none';
    });
    
    // Mostra a seção selecionada
    const secaoAtiva = document.getElementById(`secao-${secao}`);
    if (secaoAtiva) secaoAtiva.style.display = 'block';


    // Remove active de todos os itens do menu
    const menuItems = document.querySelectorAll('.menu-item');
    menuItems.forEach(item => {
        item.classList.remove('active');
    });
    
    // Adiciona active ao item clicado
    menuItems.forEach(item => {
        const texto = item.textContent.toLowerCase();
        if (texto.includes(secao.toLowerCase())) {
            item.classList.add('active');
        }
    });
}
function confirmarExcluirPerfil() {

    const msg1 =
        "⚠️ ATENÇÃO!\n\n" +
        "Você está prestes a excluir PERMANENTEMENTE seu perfil e todos os dados associados.\n\n" +
        "Essa ação não poderá ser desfeita.\n\n" +
        "Deseja continuar?";

    if (!confirm(msg1)) {
        return;
    }

    if (!confirm("Última confirmação. Excluir perfil permanentemente?")) {
        return;
    }

    const form = document.createElement('form');

    form.method = 'POST';

    form.action = '/excluir_perfil';

    document.body.appendChild(form);

    form.submit();
}
function mudarAba(aba) {
    // Esconde todas as abas
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Mostra a aba selecionada
    document.getElementById('aba-' + aba).classList.add('active');
    
    // Remove active de todos os botões
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Adiciona active ao botão clicado
    event.currentTarget.classList.add('active');
}

function ativarEdicaoEmpresa() {
    document.getElementById('view-mode-empresa').style.display = 'none';
    document.getElementById('edit-mode-empresa').style.display = 'block';
}

function cancelarEdicaoEmpresa() {
    document.getElementById('view-mode-empresa').style.display = 'block';
    document.getElementById('edit-mode-empresa').style.display = 'none';
}