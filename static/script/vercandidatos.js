// vercandidatos.js
function alterarStatus(idCandidatura, novoStatus) {
    if (!confirm(`Tem certeza que deseja ${novoStatus === 'aprovado' ? 'APROVAR' : 'REJEITAR'} este candidato?`)) {
        return;
    }
    
    fetch(`/candidatura/${idCandidatura}/status`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ status: novoStatus })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || 'Erro no servidor');
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert(data.message || 'Status atualizado com sucesso!');
            location.reload();
        } else {
            alert('Erro ao atualizar status: ' + (data.error || 'Erro desconhecido'));
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao atualizar status: ' + error.message);
    });
}