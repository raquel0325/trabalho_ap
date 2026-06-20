
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
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Status atualizado com sucesso!');
            location.reload();
        } else {
            alert('Erro ao atualizar status: ' + data.error);
        }
    })
    .catch(error => {
        alert('Erro ao atualizar status');
    });
}
