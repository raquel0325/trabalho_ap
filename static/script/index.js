
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