/**
 * formulario.js
 * Controla a navegação entre as três telas:
 *   Tela 1 → Formulário de Contato
 *   Tela 2 → Revisão dos Dados
 *   Tela 3 → Confirmação de Envio
 */

// ── Referências aos elementos ──────────────────────────────────────────────
const telaFormulario = document.getElementById('tela-formulario');
const telaRevisao    = document.getElementById('tela-revisao');
const telaSucesso    = document.getElementById('tela-sucesso');

const formContato    = document.getElementById('form-contato');
const btnConfirmar   = document.getElementById('btn-confirmar');
const btnVoltarForm  = document.getElementById('btn-voltar-form');
const btnNovoEnvio   = document.getElementById('btn-novo-envio');

const revNome        = document.getElementById('rev-nome');
const revEmail       = document.getElementById('rev-email');
const revMensagem    = document.getElementById('rev-mensagem');

// ── Utilidade: Alternar telas ──────────────────────────────────────────────
/**
 * Exibe apenas a tela passada como argumento e oculta as demais.
 * @param {HTMLElement} telaAtiva - Elemento <main> a ser exibido.
 */
function mostrarTela(telaAtiva) {
    [telaFormulario, telaRevisao, telaSucesso].forEach(tela => {
        tela.classList.add('hidden');
        tela.setAttribute('aria-hidden', 'true');
    });

    telaAtiva.classList.remove('hidden');
    telaAtiva.removeAttribute('aria-hidden');

    // Rola para o topo suavemente ao trocar de tela
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ── TELA 1 → TELA 2: Submissão do formulário ──────────────────────────────
formContato.addEventListener('submit', function (evento) {
    evento.preventDefault(); // Impede o envio tradicional (recarregar página)

    // Validação nativa do HTML5
    if (!formContato.checkValidity()) {
        formContato.reportValidity();
        return;
    }

    // Captura os valores digitados
    const nome     = document.getElementById('nome').value.trim();
    const email    = document.getElementById('email').value.trim();
    const mensagem = document.getElementById('mensagem').value.trim();

    // Preenche a tela de revisão com os dados do usuário
    revNome.textContent     = nome;
    revEmail.textContent    = email;
    revMensagem.textContent = mensagem;

    mostrarTela(telaRevisao);
});

// ── TELA 2 → TELA 3: Confirmação dos dados ────────────────────────────────
btnConfirmar.addEventListener('click', function () {
    // Aqui seria feita a requisição real (fetch/AJAX) para enviar os dados
    // Simulamos o sucesso do envio navegando para a tela de confirmação
    mostrarTela(telaSucesso);
});

// ── TELA 2 → TELA 1: Voltar ao formulário para corrigir ───────────────────
btnVoltarForm.addEventListener('click', function () {
    mostrarTela(telaFormulario);
    // Mantém os dados preenchidos para o usuário apenas corrigir
});

// ── TELA 3 → TELA 1: Novo envio ───────────────────────────────────────────
btnNovoEnvio.addEventListener('click', function () {
    // Limpa todos os campos para um novo preenchimento
    formContato.reset();
    mostrarTela(telaFormulario);
    // Foca no primeiro campo para melhor usabilidade
    document.getElementById('nome').focus();
});
