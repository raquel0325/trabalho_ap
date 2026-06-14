
    // Seleciona todos os alertas e remove após 4 segundos
    setTimeout(() => {
        const alertas = document.querySelectorAll('.alerta');
        alertas.forEach(a => a.style.display = 'none');
    }, 4000);



     
        function mudar(tipo) {
           
            if (tipo === 'login') {
                document.getElementById('secaoLogin').classList.remove('hidden');
                document.getElementById('secaoCadastro').classList.add('hidden');
            } else {
                document.getElementById('secaoLogin').classList.add('hidden');
                document.getElementById('secaoCadastro').classList.remove('hidden');
            }
        }


        
        function formCad(idForm) {
           
            document.querySelectorAll('.form-container').forEach(div => {
                div.classList.remove('active');
            });
          
            document.getElementById(idForm).classList.add('active');
        }
    





        function mudar(tipo) {
    const btnLogin = document.querySelector('.btn-main:first-child');
    const btnCadastro = document.querySelector('.btn-main:last-child');
    const secaoLogin = document.getElementById('secaoLogin');
    const secaoCadastro = document.getElementById('secaoCadastro');
    
    if (tipo === 'login') {
        btnLogin.classList.add('ativo');
        btnCadastro.classList.remove('ativo');
        secaoLogin.classList.remove('hidden');
        secaoCadastro.classList.add('hidden');
    } else {
        btnLogin.classList.remove('ativo');
        btnCadastro.classList.add('ativo');
        secaoLogin.classList.add('hidden');
        secaoCadastro.classList.remove('hidden');
    }
}

// Iniciar com o botão Login ativo
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.btn-main:first-child').classList.add('ativo');
});


// Funções de Máscara (Regex)
const mascaras = {
    cpf(value) {
        return value
            .replace(/\D/g, '') // Remove tudo o que não é dígito
            .replace(/(\d{3})(\d)/, '$1.$2') // Adiciona ponto após o terceiro dígito
            .replace(/(\d{3})(\d)/, '$1.$2') // Adiciona ponto após o sexto dígito
            .replace(/(\d{3})(\d{1,2})$/, '$1-$2'); // Adiciona traço antes dos dois últimos dígitos
    },
    cnpj(value) {
        return value
            .replace(/\D/g, '')
            .replace(/^(\d{2})(\d)/, '$1.$2')
            .replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3')
            .replace(/\.(\d{3})(\d)/, '.$1/$2')
            .replace(/(\d{4})(\d)/, '$1-$2');
    },
    telefone(value) {
        return value
            .replace(/\D/g, '')
            .replace(/^(\d{2})(\d)/g, '($1) $2') // Adiciona parênteses no DDD
            .replace(/(\d)(\d{4})$/, '$1-$2'); // Adiciona o traço no número
    }
};

// Mascar form 
document.addEventListener('DOMContentLoaded', () => {
    const inputCpf = document.getElementById('cpf');
    const inputCnpj = document.getElementById('cnpj');
    const telFuncionario = document.getElementById('telFuncionario');
    const telEmpresa = document.getElementById('telEmpresa');

    if (inputCpf) {
        inputCpf.addEventListener('input', (e) => {
            e.target.value = mascaras.cpf(e.target.value);
        });
    }

    if (inputCnpj) {
        inputCnpj.addEventListener('input', (e) => {
            e.target.value = mascaras.cnpj(e.target.value);
        });
    }

    [telFuncionario, telEmpresa].forEach(input => {
        if (input) {
            input.addEventListener('input', (e) => {
                e.target.value = mascaras.telefone(e.target.value);
            });
        }
    });
});