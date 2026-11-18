/**
 * Beacon LMS - Offline Sync Manager
 */
const BeaconSync = (() => {
  let isOnline = navigator.onLine;
  const statusListeners = [];

  function init() {
    updateConnectionStatus();

    window.addEventListener('online', () => {
      console.log('[Beacon Sync] Network detected: Online');
      updateConnectionStatus();
      flushOutbox();
    });

    window.addEventListener('offline', () => {
      console.log('[Beacon Sync] Network lost: Working in Offline Mode');
      updateConnectionStatus();
    });

    // Check periodically by pinging the local hub
    setInterval(checkServerPing, 20000);

    // Initial outbox badge check
    refreshOutboxCount();
  }

  async function checkServerPing() {
    try {
      const res = await fetch('/api/ping', { method: 'GET', cache: 'no-store' });
      if (res.ok) {
        setOnlineState(true);
      } else {
        setOnlineState(false);
      }
    } catch (e) {
      setOnlineState(false);
    }
  }

  function setOnlineState(online) {
    if (isOnline !== online) {
      isOnline = online;
      updateConnectionStatus();
      if (isOnline) {
        flushOutbox();
      }
    }
  }

  function updateConnectionStatus() {
    const statusDot = document.getElementById('sync-status-dot');
    const statusText = document.getElementById('sync-status-text');

    if (statusDot && statusText) {
      if (isOnline) {
        statusDot.className = 'status-dot online';
        statusText.textContent = 'Hub Connected';
      } else {
        statusDot.className = 'status-dot offline';
        statusText.textContent = 'Offline Mode';
      }
    }

    statusListeners.forEach((fn) => fn(isOnline));
  }

  function onStatusChange(callback) {
    statusListeners.push(callback);
  }

  async function refreshOutboxCount() {
    try {
      const items = await BeaconDB.getPendingOutbox();
      const badge = document.getElementById('outbox-count-badge');
      if (badge) {
        badge.textContent = items.length;
        badge.style.display = items.length > 0 ? 'inline-flex' : 'none';
      }
      return items.length;
    } catch (e) {
      return 0;
    }
  }

  async function downloadCurriculumForOffline(onProgress) {
    if (onProgress) onProgress('Fetching curriculum from school server...');
    try {
      const res = await fetch('/api/curriculum');
      if (!res.ok) throw new Error('Failed to reach curriculum server');
      const data = await res.json();

      if (onProgress) onProgress('Caching lessons and questions in offline storage...');
      await BeaconDB.saveCurriculum(data.subjects);

      if (onProgress) onProgress('Done! All subjects downloaded for offline study.');
      return { success: true, count: data.subjects.length };
    } catch (err) {
      console.error('[Beacon Sync] Download curriculum error:', err);
      if (onProgress) onProgress('Error downloading curriculum: ' + err.message);
      return { success: false, error: err.message };
    }
  }

  async function flushOutbox() {
    try {
      const pendingItems = await BeaconDB.getPendingOutbox();
      if (!pendingItems || pendingItems.length === 0) {
        console.log('[Beacon Sync] Outbox is clear, nothing to sync.');
        refreshOutboxCount();
        return { synced: 0 };
      }

      console.log(`[Beacon Sync] Flushing ${pendingItems.length} queued offline items...`);

      const submissions = [];
      const completions = [];
      const itemUuids = [];

      pendingItems.forEach((item) => {
        itemUuids.push(item.uuid);
        if (item.type === 'submission') {
          submissions.push({
            submission_uuid: item.uuid,
            quiz_id: item.data.quiz_id,
            score: item.data.score,
            total_points: item.data.total_points,
            passing_score: item.data.passing_score,
            answers: item.data.answers,
            client_timestamp: item.timestamp
          });
        } else if (item.type === 'completion') {
          completions.push({
            lesson_id: item.data.lesson_id,
            client_timestamp: item.timestamp
          });
        }
      });

      const payload = {
        submissions: submissions,
        completions: completions
      };

      const res = await fetch('/api/sync/push', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        await BeaconDB.clearOutboxItems(itemUuids);
        console.log('[Beacon Sync] Successfully synced outbox items to server!');
        refreshOutboxCount();
        showNotification('Sync Complete', `Synchronized ${itemUuids.length} offline activity records.`);
        return { synced: itemUuids.length };
      } else {
        console.warn('[Beacon Sync] Server returned non-ok during sync:', res.status);
      }
    } catch (e) {
      console.warn('[Beacon Sync] Could not sync outbox right now (still offline):', e.message);
    }
    refreshOutboxCount();
    return { synced: 0 };
  }

  function showNotification(title, message) {
    if (window.showToast) {
      window.showToast(message, 'success');
    }
  }

  return {
    init,
    isOnline: () => isOnline,
    onStatusChange,
    downloadCurriculumForOffline,
    flushOutbox,
    refreshOutboxCount
  };
})();

document.addEventListener('DOMContentLoaded', () => {
  BeaconSync.init();
});
