
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
function mostrarFormFreelance() {
    document.getElementById('form-freelance-container').style.display = 'block';
    // Scroll para o formulário
    document.getElementById('form-freelance-container').scrollIntoView({ behavior: 'smooth' });
}

function fecharFormFreelance() {
    document.getElementById('form-freelance-container').style.display = 'none';
}

function editarFreelance(id) {
    // Redireciona para página de edição
    window.location.href = `/freelancer/editar/${id}`;
}

function excluirFreelance(id) {
    if (confirm('Tem certeza que deseja excluir este freelance?')) {
        fetch(`/freelancer/excluir/${id}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Freelance excluído com sucesso!');
                location.reload();
            } else {
                alert('Erro ao excluir: ' + data.message);
            }
        });
    }
}
// Função para alternar entre seções do menu
function mostrarSecao(secao) {
    // Esconde todas as seções
    const secoes = ['perfil', 'editar', 'freelance', 'contratados'];
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