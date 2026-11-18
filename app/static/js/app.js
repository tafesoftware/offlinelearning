/**
 * Beacon LMS - Core Application UI & PWA Bootstrap
 */

// 1. Register Service Worker
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker
      .register('/static/sw.js')
      .then((registration) => {
        console.log('[Beacon LMS] Service Worker registered with scope:', registration.scope);
      })
      .catch((error) => {
        console.warn('[Beacon LMS] Service Worker registration failed:', error);
      });
  });
}

// 2. PWA Install Prompt Banner
let deferredInstallPrompt = null;
window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredInstallPrompt = e;
  const installBanner = document.getElementById('pwa-install-banner');
  if (installBanner) {
    installBanner.classList.remove('d-none');
  }
});

function triggerPWAInstall() {
  if (deferredInstallPrompt) {
    deferredInstallPrompt.prompt();
    deferredInstallPrompt.userChoice.then((choiceResult) => {
      if (choiceResult.outcome === 'accepted') {
        console.log('[Beacon LMS] User accepted PWA installation');
      }
      deferredInstallPrompt = null;
      const installBanner = document.getElementById('pwa-install-banner');
      if (installBanner) installBanner.classList.add('d-none');
    });
  }
}

// 3. Toast Notifications
window.showToast = function (message, type = 'info') {
  let toastContainer = document.getElementById('toast-container');
  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.id = 'toast-container';
    toastContainer.className = 'toast-container';
    document.body.appendChild(toastContainer);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type} animate-slide-in`;
  toast.innerHTML = `
    <span>${message}</span>
    <button onclick="this.parentElement.remove()" class="toast-close">&times;</button>
  `;

  toastContainer.appendChild(toast);
  setTimeout(() => {
    toast.classList.add('fade-out');
    setTimeout(() => toast.remove(), 300);
  }, 4000);
};

// 4. Mark Lesson Complete Handler (Offline & Online capable)
async function markLessonComplete(lessonId) {
  const btn = document.getElementById('complete-lesson-btn');
  if (btn) btn.disabled = true;

  try {
    if (navigator.onLine) {
      const res = await fetch('/api/lesson/complete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ lesson_id: lessonId })
      });
      if (res.ok) {
        showToast('Lesson marked as completed!', 'success');
        updateCompletionButtonUI();
        return;
      }
    }

    // If offline or network request failed, queue in IndexedDB
    await BeaconDB.queueLessonCompletion({ lesson_id: lessonId });
    BeaconSync.refreshOutboxCount();
    showToast('Saved offline! Will sync when connected to school hub.', 'info');
    updateCompletionButtonUI();
  } catch (e) {
    console.error('Error marking lesson complete:', e);
    showToast('Could not save completion: ' + e.message, 'danger');
    if (btn) btn.disabled = false;
  }
}

function updateCompletionButtonUI() {
  const btn = document.getElementById('complete-lesson-btn');
  if (btn) {
    btn.className = 'btn btn-success';
    btn.innerHTML = '✓ Lesson Completed';
    btn.disabled = true;
  }
}
