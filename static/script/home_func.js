// static/script/home_func.js

// Função para alternar entre seções do menu
function mostrarSecao(secao) {
    // Esconde todas as seções
    const secoes = ['perfil', 'chat', 'pessoas', 'editar', 'freelance'];
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

// Função para ativar o modo de edição do perfil
function ativarEdicao() {
    document.getElementById('view-mode').style.display = 'none';
    document.getElementById('edit-mode').style.display = 'block';
}

// Função para cancelar a edição do perfil
function cancelarEdicao() {
    document.getElementById('view-mode').style.display = 'block';
    document.getElementById('edit-mode').style.display = 'none';
}

// Função para cancelar edição de competências
function cancelarEdicaoCompetencias() {
    location.reload();
}

// Função para deletar candidatura
function deletarCandidatura(idCandidatura) {
    if (confirm('Tem certeza que deseja cancelar esta candidatura?')) {
        fetch(`/cancelar_candidatura/${idCandidatura}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Candidatura cancelada com sucesso!');
                location.reload();
            } else {
                alert('Erro ao cancelar candidatura: ' + data.error);
            }
        })
        .catch(() => {
            alert('Erro ao cancelar candidatura');
        });
    }
}

// Função para adicionar nova competência na lista
function adicionarNovaCompetencia() {
    const input = document.getElementById('input_nova_comp');
    const nomeComp = input.value.trim();
    const lista = document.getElementById('novas-competencias-lista');
    
    if (nomeComp === "") {
        alert("Digite o nome da competência!");
        return;
    }
    
    // Verificar se já existe na lista de novas
    const itens = lista.querySelectorAll('.nova-competencia-tag');
    for (let item of itens) {
        if (item.getAttribute('data-nome') === nomeComp.toLowerCase()) {
            alert("Esta competência já foi adicionada!");
            input.value = "";
            return;
        }
    }
    
    // Verificar se já existe no grid de competências existentes
    const checkboxes = document.querySelectorAll('.competencia-checkbox input');
    for (let cb of checkboxes) {
        const label = cb.parentElement.querySelector('span');
        if (label && label.textContent.toLowerCase() === nomeComp.toLowerCase()) {
            alert("Esta competência já existe na lista! Foi selecionada automaticamente.");
            cb.checked = true;
            input.value = "";
            return;
        }
    }
    
    // Criar tag da nova competência
    const tag = document.createElement('div');
    tag.className = 'nova-competencia-tag';
    tag.setAttribute('data-nome', nomeComp.toLowerCase());
    tag.innerHTML = nomeComp + 
        '<input type="hidden" name="novas_competencias" value="' + nomeComp.replace(/["']/g, '&quot;') + '">' +
        '<button type="button" class="remove-tag" onclick="this.parentElement.remove()">×</button>';
    
    lista.appendChild(tag);
    input.value = "";
    input.focus();
}

// Inicialização quando o DOM carregar
document.addEventListener('DOMContentLoaded', function() {
    // Garante que a seção perfil está visível
    mostrarSecao('perfil');
    
    // Adiciona evento de Enter para o input de nova competência
    const inputNovaComp = document.getElementById('input_nova_comp');
    if (inputNovaComp) {
        inputNovaComp.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                adicionarNovaCompetencia();
            }
        });
    }
    

});
//======================================================================================================================================

// Função para seguir um usuário (usando o novo blueprint)
function seguirUsuario(element) {
    const card = element.closest('.pessoa-card');
    const usuarioId = card.getAttribute('data-usuario-id');
    const nome = card.getAttribute('data-usuario-nome');
    
    fetch(`/seguir_usuario/${usuarioId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(`✅ Você agora está seguindo ${nome}!`);
            // Atualiza o botão para mostrar que está seguindo
            const btn = element;
            btn.innerHTML = '✅ Seguindo';
            btn.classList.remove('btn-seguir');
            btn.classList.add('btn-seguindo');
            btn.setAttribute('onclick', `deixarSeguir(this)`);
        } else {
            alert('❌ Erro ao seguir usuário: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('❌ Erro ao seguir usuário');
    });
}

// Função para deixar de seguir um usuário
function deixarSeguir(element) {
    const card = element.closest('.pessoa-card');
    const usuarioId = card.getAttribute('data-usuario-id');
    const nome = card.getAttribute('data-usuario-nome');
    
    if (!confirm(`Tem certeza que deseja deixar de seguir ${nome}?`)) {
        return;
    }
    
    fetch(`/deixar_seguir/${usuarioId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(`✅ Você deixou de seguir ${nome}!`);
            // Atualiza o botão para voltar ao estado "Seguir"
            const btn = element;
            btn.innerHTML = '➕ Seguir';
            btn.classList.remove('btn-seguindo');
            btn.classList.add('btn-seguir');
            btn.setAttribute('onclick', `seguirUsuario(this)`);
        } else {
            alert('❌ Erro ao deixar de seguir: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('❌ Erro ao deixar de seguir');
    });
}

// Função para recomendar um usuário
function recomendarUsuario(element) {
    const card = element.closest('.pessoa-card');
    const usuarioId = card.getAttribute('data-usuario-id');
    const nome = card.getAttribute('data-usuario-nome');
    
    // Opção 1: Apenas um alerta simples
    alert(`📢 Funcionalidade em desenvolvimento!\n\nVocê pode recomendar ${nome} para vagas.`);
    
    // Opção 2: Abrir um modal (se quiser implementar depois)
    // abrirModalRecomendacao(usuarioId, nome);
}

// Função para carregar o estado inicial dos botões (quem já está seguindo)
function carregarStatusSeguindo() {
    const cards = document.querySelectorAll('.pessoa-card');
    
    cards.forEach(card => {
        const usuarioId = card.getAttribute('data-usuario-id');
        
        fetch(`/verificar_seguindo/${usuarioId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success && data.seguindo) {
                const btn = card.querySelector('.btn-seguir');
                if (btn) {
                    btn.innerHTML = '✅ Seguindo';
                    btn.classList.remove('btn-seguir');
                    btn.classList.add('btn-seguindo');
                    btn.setAttribute('onclick', `deixarSeguir(this)`);
                }
            }
        })
        .catch(error => {
            console.error('Erro ao verificar status:', error);
        });
    });
}

// Inicialização quando o DOM carregar
document.addEventListener('DOMContentLoaded', function() {
    // Garante que a seção perfil está visível
    mostrarSecao('perfil');
    
    // Adiciona evento de Enter para o input de nova competência
    const inputNovaComp = document.getElementById('input_nova_comp');
    if (inputNovaComp) {
        inputNovaComp.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                adicionarNovaCompetencia();
            }
        });
    }
    
    // Carrega o status de seguindo para todos os usuários
    carregarStatusSeguindo();
});