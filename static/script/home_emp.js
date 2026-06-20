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