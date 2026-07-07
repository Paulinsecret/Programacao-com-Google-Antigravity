/**
 * faq.js — Lógica de interação da página FAQ do SENAI
 *
 * Responsabilidades:
 *  1. Atualizar o ano de copyright dinamicamente no rodapé.
 *  2. Controlar o acordeão de abertura/fechamento das respostas FAQ.
 *  3. Gerenciar o sistema de curtir / descurtir de cada resposta,
 *     com persistência na sessionStorage.
 */

'use strict';

/* ==========================================================================
   1. UTILITÁRIOS — sessionStorage
   ========================================================================== */

function storageKey(faqId) {
  return `senai_faq_vote_${faqId}`;
}

function loadVoteState(faqId) {
  const raw = sessionStorage.getItem(storageKey(faqId));
  if (!raw) return { action: null, likes: 0, dislikes: 0 };
  try {
    return JSON.parse(raw);
  } catch {
    return { action: null, likes: 0, dislikes: 0 };
  }
}

function saveVoteState(faqId, state) {
  sessionStorage.setItem(storageKey(faqId), JSON.stringify(state));
}

/* ==========================================================================
   2. FEEDBACK — renderização e lógica de voto
   ========================================================================== */

/**
 * Atualiza a aparência dos botões de like/dislike de acordo com o estado.
 */
function renderFeedbackButtons(likeBtn, dislikeBtn, state) {
  likeBtn.querySelector('.btn-feedback__count').textContent    = state.likes;
  dislikeBtn.querySelector('.btn-feedback__count').textContent = state.dislikes;

  likeBtn.classList.remove('is-active');
  dislikeBtn.classList.remove('is-active');

  if (state.action === 'like') {
    likeBtn.classList.add('is-active');
    likeBtn.setAttribute('aria-pressed', 'true');
    dislikeBtn.setAttribute('aria-pressed', 'false');
  } else if (state.action === 'dislike') {
    dislikeBtn.classList.add('is-active');
    dislikeBtn.setAttribute('aria-pressed', 'true');
    likeBtn.setAttribute('aria-pressed', 'false');
  } else {
    likeBtn.setAttribute('aria-pressed', 'false');
    dislikeBtn.setAttribute('aria-pressed', 'false');
  }
}

/**
 * Processa um clique em um botão de feedback.
 * Toggle: clicar no mesmo botão desfaz o voto.
 */
function handleVote(faqId, action, likeBtn, dislikeBtn) {
  const state    = loadVoteState(faqId);
  const previous = state.action;

  // Desfaz voto anterior
  if (previous === 'like')    state.likes    = Math.max(0, state.likes - 1);
  if (previous === 'dislike') state.dislikes = Math.max(0, state.dislikes - 1);

  if (previous === action) {
    // Toggle off: remove o voto
    state.action = null;
  } else {
    // Novo voto
    state.action = action;
    if (action === 'like')    state.likes    += 1;
    if (action === 'dislike') state.dislikes += 1;
  }

  saveVoteState(faqId, state);
  renderFeedbackButtons(likeBtn, dislikeBtn, state);
  triggerPopAnimation(action === 'like' ? likeBtn : dislikeBtn);
}

/** Dispara animação "pop" em um botão. */
function triggerPopAnimation(btn) {
  btn.classList.remove('pop');
  void btn.offsetWidth; // forçar reflow
  btn.classList.add('pop');
  btn.addEventListener('animationend', () => btn.classList.remove('pop'), { once: true });
}

/* ==========================================================================
   3. ACORDEÃO — abertura e fechamento das respostas
   ========================================================================== */

/**
 * Alterna o estado aberto/fechado de um card FAQ.
 *
 * @param {HTMLElement} card     - O elemento <article class="faq-card">
 * @param {HTMLButtonElement} toggleBtn - O botão de toggle do card
 */
function toggleCard(card, toggleBtn) {
  const isOpen = card.classList.contains('is-open');

  if (isOpen) {
    // Fechar
    card.classList.remove('is-open');
    toggleBtn.setAttribute('aria-expanded', 'false');
  } else {
    // Abrir
    card.classList.add('is-open');
    toggleBtn.setAttribute('aria-expanded', 'true');
  }
}

/**
 * Inicializa os botões de toggle de todos os cards FAQ.
 * Os botões de feedback ficam dentro do corpo recolhível e
 * não propagam o clique para o toggle.
 */
function initAccordion() {
  const toggleButtons = document.querySelectorAll('.faq-card__toggle');

  toggleButtons.forEach((toggleBtn) => {
    const card = toggleBtn.closest('.faq-card');
    if (!card) return;

    toggleBtn.addEventListener('click', () => {
      toggleCard(card, toggleBtn);
    });
  });
}

/* ==========================================================================
   4. INICIALIZAÇÃO DOS BOTÕES DE FEEDBACK
   ========================================================================== */

function initFeedbackButtons() {
  const likeButtons = document.querySelectorAll('.btn-feedback--like');

  likeButtons.forEach((likeBtn) => {
    const faqId      = likeBtn.dataset.faq;
    const feedback   = likeBtn.closest('.faq-card__feedback');
    const dislikeBtn = feedback ? feedback.querySelector('.btn-feedback--dislike') : null;

    if (!dislikeBtn || !faqId) return;

    // Restaura estado salvo da sessão
    const savedState = loadVoteState(faqId);
    renderFeedbackButtons(likeBtn, dislikeBtn, savedState);

    // Listeners — stopPropagation garante que o clique não chegue ao toggle
    likeBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      handleVote(faqId, 'like', likeBtn, dislikeBtn);
    });

    dislikeBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      handleVote(faqId, 'dislike', likeBtn, dislikeBtn);
    });
  });
}

/* ==========================================================================
   5. FOOTER — ano dinâmico
   ========================================================================== */

function initFooterYear() {
  const yearEl = document.getElementById('footer-year');
  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }
}

/* --------------------------------------------------------------------------
   Ponto de entrada: aguarda o DOM estar pronto.
   -------------------------------------------------------------------------- */
document.addEventListener('DOMContentLoaded', () => {
  initFooterYear();
  initAccordion();
  initFeedbackButtons();
});
