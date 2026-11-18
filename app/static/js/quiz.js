/**
 * Beacon LMS - Offline Quiz Runner
 */
const BeaconQuiz = (() => {
  let quizData = null;
  let userAnswers = {};

  function init(quizConfig) {
    quizData = quizConfig;
    userAnswers = {};
    renderQuiz();
  }

  function renderQuiz() {
    const container = document.getElementById('quiz-questions-container');
    if (!container || !quizData || !quizData.questions) return;

    let html = '';
    quizData.questions.forEach((q, idx) => {
      html += `
        <div class="card quiz-card mb-4" id="question-card-${q.id}">
          <div class="card-body">
            <div class="d-flex justify-between align-center mb-2">
              <span class="badge badge-primary">Question ${idx + 1} of ${quizData.questions.length}</span>
              <span class="text-muted text-sm">${q.points || 10} Points</span>
            </div>
            <h3 class="question-text mb-3">${escapeHtml(q.question_text)}</h3>
            <div class="options-list">
      `;

      q.options.forEach((opt, optIdx) => {
        const optionId = `q_${q.id}_opt_${optIdx}`;
        html += `
          <label class="option-label" for="${optionId}">
            <input type="radio" id="${optionId}" name="question_${q.id}" value="${optIdx}" onchange="BeaconQuiz.selectAnswer(${q.id}, ${optIdx})">
            <span class="option-custom-radio"></span>
            <span class="option-text">${escapeHtml(opt)}</span>
          </label>
        `;
      });

      html += `
            </div>
            <div class="explanation-box d-none" id="explanation-${q.id}">
              <strong>Explanation:</strong> ${escapeHtml(q.explanation || 'No explanation provided.')}
            </div>
          </div>
        </div>
      `;
    });

    container.innerHTML = html;
  }

  function selectAnswer(questionId, optionIndex) {
    userAnswers[questionId] = optionIndex;
    updateSubmitButton();
  }

  function updateSubmitButton() {
    const btn = document.getElementById('submit-quiz-btn');
    if (!btn || !quizData) return;
    const answeredCount = Object.keys(userAnswers).length;
    btn.disabled = answeredCount === 0;
    btn.textContent = answeredCount === quizData.questions.length ? 'Submit Quiz' : `Submit (${answeredCount}/${quizData.questions.length} Answered)`;
  }

  async function submitQuiz() {
    if (!quizData) return;

    const btn = document.getElementById('submit-quiz-btn');
    if (btn) btn.disabled = true;

    // 1. Calculate Score locally
    let totalPoints = 0;
    let earnedPoints = 0;

    quizData.questions.forEach((q) => {
      totalPoints += (q.points || 10);
      const chosen = userAnswers[q.id];
      const card = document.getElementById(`question-card-${q.id}`);
      const expl = document.getElementById(`explanation-${q.id}`);

      if (expl) expl.classList.remove('d-none');

      if (chosen !== undefined && chosen === q.correct_option_index) {
        earnedPoints += (q.points || 10);
        if (card) card.classList.add('correct-border');
      } else {
        if (card) card.classList.add('incorrect-border');
      }
    });

    const percentage = Math.round((earnedPoints / Math.max(totalPoints, 1)) * 100);
    const passed = percentage >= (quizData.passing_score || 70);

    // 2. Prepare submission record
    const submissionRecord = {
      uuid: 'sub_' + quizData.id + '_' + Date.now(),
      quiz_id: quizData.id,
      score: earnedPoints,
      total_points: totalPoints,
      percentage: percentage,
      passed: passed,
      passing_score: quizData.passing_score || 70,
      answers: userAnswers,
      client_timestamp: new Date().toISOString()
    };

    // 3. Save to local IndexedDB outbox
    await BeaconDB.queueSubmission(submissionRecord);
    BeaconSync.refreshOutboxCount();

    // 4. If online, trigger background flush
    if (navigator.onLine) {
      BeaconSync.flushOutbox();
    }

    // 5. Display Result summary banner
    renderResultBanner(earnedPoints, totalPoints, percentage, passed);

    // Scroll to results
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function renderResultBanner(score, total, percentage, passed) {
    const banner = document.getElementById('quiz-result-banner');
    if (!banner) return;

    banner.classList.remove('d-none');
    banner.className = `result-banner ${passed ? 'banner-success' : 'banner-warning'} mb-4`;

    banner.innerHTML = `
      <div class="result-header">
        <div class="result-icon">${passed ? '🎉' : '📖'}</div>
        <div>
          <h2>${passed ? 'Congratulations! You Passed!' : 'Good Effort! Keep Practicing!'}</h2>
          <p>Score: <strong>${score} / ${total}</strong> (${percentage}%) &bull; Passing required: ${quizData.passing_score}%</p>
          <p class="text-sm text-muted">
            ${navigator.onLine ? '✅ Submission synced with school server.' : '💾 Submission saved securely offline in your device. It will automatically upload when connected to the school hub.'}
          </p>
        </div>
      </div>
      <div class="result-actions mt-3">
        <a href="/student/dashboard" class="btn btn-secondary">Back to Dashboard</a>
        <button onclick="location.reload()" class="btn btn-primary">Retake Quiz</button>
      </div>
    `;

    // Hide submit button container
    const actions = document.getElementById('quiz-action-bar');
    if (actions) actions.style.display = 'none';
  }

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  return {
    init,
    selectAnswer,
    submitQuiz
  };
})();
