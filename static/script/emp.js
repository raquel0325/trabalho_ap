 function mudar(tipo) {
        const secao1 = document.getElementById('secao1');
        const secao2 = document.getElementById('secao2');
        const secao3 = document.getElementById('secao3');
        const secao4 = document.getElementById('secao4');
        
        const botoes = document.querySelectorAll('.btn-main');
        
        // Remove classe 'ativo' de todos os botões
        botoes.forEach(botao => botao.classList.remove('ativo'));
        
        // Esconde todas as seções
        secao1.classList.add('hidden');
        secao2.classList.add('hidden');
        secao3.classList.add('hidden');
        secao4.classList.add('hidden');
        
        // Mostra a seção selecionada e ativa o botão correspondente
        if (tipo === 'home'){
            secao1.classList.remove('hidden');
            botoes[0].classList.add('ativo');
        }
        else if (tipo === 'contratar'){
            secao2.classList.remove('hidden');
            botoes[1].classList.add('ativo');
        }
        else if (tipo === 'contact'){
            secao3.classList.remove('hidden');
            botoes[2].classList.add('ativo');
        }
        else if (tipo === 'about'){
            secao4.classList.remove('hidden');
            botoes[3].classList.add('ativo');
        }
    }

    document.addEventListener('DOMContentLoaded', function() {
        mudar('home');
    });