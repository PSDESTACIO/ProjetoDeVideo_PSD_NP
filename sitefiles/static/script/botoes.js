//Utilizado para mostrar o painel de editar video
function MostrarPainelEditar(filename) {
    document.getElementById('edit-buttons-' + filename).style.display = 'none';
    document.getElementById('edit-form-' + filename).style.display = 'block';
}

//Utilizado para esconder o painel de editar video
function EsconderPainelEditar(filename) {
    document.getElementById('edit-form-' + filename).style.display = 'none';
    document.getElementById('edit-buttons-' + filename).style.display = 'block';
}

//Utilizado para confirmar ou não a exclusão do vídeo
function ConfirmarExclusao() {
    return confirm("Tem certeza de que deseja excluir o vídeo?");
}

//Utilizado para confirmar ou não a exclusão do vídeo
function ConfirmarEdicao() {
    return confirm("Tem certeza de que deseja modificar o vídeo?");
}