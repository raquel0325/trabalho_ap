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

function mostrarSecao(secao) {
    const secaoAtiva = document.getElementById(`secao-${secao}`);
    if (secaoAtiva) {
        // Se já estiver aparecendo, esconde. Se estiver escondido, mostra.
        if (secaoAtiva.style.display === 'none' || secaoAtiva.style.display === '') {
            secaoAtiva.style.display = 'block';
            // Rola a tela suavemente até a seção surgir
            secaoAtiva.scrollIntoView({ behavior: 'smooth' });
        } else {
            secaoAtiva.style.display = 'none';
        }
    }
}
function mudarAba(aba) {
    // Esconde todas as abas principais
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Mostra a aba selecionada
    document.getElementById('aba-' + aba).classList.add('active');
    
    // Remove o estado 'active' de todos os botões da sidebar
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Adiciona 'active' ao botão clicado
    if (event && event.currentTarget) {
        event.currentTarget.classList.add('active');
    }

    // --- CORREÇÃO AQUI ---
    // Força o fechamento das subseções do Dashboard ao mudar de aba
    const secaoContratados = document.getElementById('secao-contratados');
    const secaoNotificacoes = document.getElementById('secao-notificacoes');
    
    if (secaoContratados) secaoContratados.style.display = 'none';
    if (secaoNotificacoes) secaoNotificacoes.style.display = 'none';
}