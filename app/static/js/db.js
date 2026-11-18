/**
 * Beacon LMS - IndexedDB Manager (Client-Side Storage for Offline Learning)
 */
const BeaconDB = (() => {
  const DB_NAME = 'BeaconOfflineLMS';
  const DB_VERSION = 1;
  let dbPromise = null;

  function openDB() {
    if (dbPromise) return dbPromise;

    dbPromise = new Promise((resolve, reject) => {
      const request = indexedDB.open(DB_NAME, DB_VERSION);

      request.onupgradeneeded = (event) => {
        const db = event.target.result;

        // Store 1: Cached subjects & lessons
        if (!db.objectStoreNames.contains('curriculum')) {
          db.createObjectStore('curriculum', { keyPath: 'id' });
        }

        // Store 2: Offline Outbox (queued quiz submissions and completions)
        if (!db.objectStoreNames.contains('outbox')) {
          const outboxStore = db.createObjectStore('outbox', { keyPath: 'uuid' });
          outboxStore.createIndex('type', 'type', { unique: false });
          outboxStore.createIndex('status', 'status', { unique: false });
        }

        // Store 3: Local settings & cached user profile
        if (!db.objectStoreNames.contains('meta')) {
          db.createObjectStore('meta', { keyPath: 'key' });
        }
      };

      request.onsuccess = (event) => resolve(event.target.result);
      request.onerror = (event) => reject(event.target.error);
    });

    return dbPromise;
  }

  // --- Curriculum Cache Operations ---
  async function saveCurriculum(subjects) {
    const db = await openDB();
    return new Promise((resolve, reject) => {
      const tx = db.transaction('curriculum', 'readwrite');
      const store = tx.objectStore('curriculum');
      store.clear(); // refresh with latest
      subjects.forEach((subj) => store.put(subj));
      tx.oncomplete = () => resolve(true);
      tx.onerror = (e) => reject(e);
    });
  }

  async function getAllSubjects() {
    const db = await openDB();
    return new Promise((resolve, reject) => {
      const tx = db.transaction('curriculum', 'readonly');
      const store = tx.objectStore('curriculum');
      const req = store.getAll();
      req.onsuccess = () => resolve(req.result || []);
      req.onerror = (e) => reject(e);
    });
  }

  async function getLessonById(lessonId) {
    const subjects = await getAllSubjects();
    for (const subj of subjects) {
      if (subj.lessons) {
        const found = subj.lessons.find((l) => l.id === parseInt(lessonId, 10));
        if (found) return { lesson: found, subject: subj };
      }
    }
    return null;
  }

  // --- Outbox Queue Operations ---
  async function queueSubmission(submissionData) {
    const db = await openDB();
    return new Promise((resolve, reject) => {
      const tx = db.transaction('outbox', 'readwrite');
      const store = tx.objectStore('outbox');
      const item = {
        uuid: submissionData.uuid || ('sub_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9)),
        type: 'submission',
        data: submissionData,
        status: 'pending',
        timestamp: new Date().toISOString()
      };
      store.put(item);
      tx.oncomplete = () => resolve(item);
      tx.onerror = (e) => reject(e);
    });
  }

  async function queueLessonCompletion(completionData) {
    const db = await openDB();
    return new Promise((resolve, reject) => {
      const tx = db.transaction('outbox', 'readwrite');
      const store = tx.objectStore('outbox');
      const item = {
        uuid: 'comp_' + completionData.lesson_id + '_' + Date.now(),
        type: 'completion',
        data: completionData,
        status: 'pending',
        timestamp: new Date().toISOString()
      };
      store.put(item);
      tx.oncomplete = () => resolve(item);
      tx.onerror = (e) => reject(e);
    });
  }

  async function getPendingOutbox() {
    const db = await openDB();
    return new Promise((resolve, reject) => {
      const tx = db.transaction('outbox', 'readonly');
      const store = tx.objectStore('outbox');
      const req = store.getAll();
      req.onsuccess = () => resolve(req.result || []);
      req.onerror = (e) => reject(e);
    });
  }

  async function clearOutboxItems(uuids) {
    const db = await openDB();
    return new Promise((resolve, reject) => {
      const tx = db.transaction('outbox', 'readwrite');
      const store = tx.objectStore('outbox');
      uuids.forEach((id) => store.delete(id));
      tx.oncomplete = () => resolve(true);
      tx.onerror = (e) => reject(e);
    });
  }

  return {
    saveCurriculum,
    getAllSubjects,
    getLessonById,
    queueSubmission,
    queueLessonCompletion,
    getPendingOutbox,
    clearOutboxItems
  };
})();
