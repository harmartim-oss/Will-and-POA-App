import Dexie from 'dexie';

/**
 * Local database for offline storage of document drafts
 * Enables auto-saving and offline-first functionality
 */
export class WillsDatabase extends Dexie {
  constructor() {
    super('OntarioWillsDB');
    
    this.version(1).stores({
      drafts: '++id, type, createdAt, updatedAt, title',
      documents: '++id, draftId, type, createdAt, format',
      settings: 'key, value'
    });
    
    // Type definitions for TypeScript-like autocomplete
    this.drafts = this.table('drafts');
    this.documents = this.table('documents');
    this.settings = this.table('settings');
  }
}

// Create a singleton instance
export const db = new WillsDatabase();

/**
 * Auto-save functionality for document drafts
 */
export const draftService = {
  /**
   * Save or update a draft
   * @param {Object} draft - Draft data
   * @param {string} draft.type - 'will' | 'poa-property' | 'poa-personal'
   * @param {string} draft.title - Draft title
   * @param {Object} draft.data - Draft content
   * @returns {Promise<number>} Draft ID
   */
  async saveDraft(draft) {
    const now = new Date().toISOString();
    
    const draftData = {
      ...draft,
      updatedAt: now,
      createdAt: draft.createdAt || now
    };
    
    if (draft.id) {
      await db.drafts.update(draft.id, draftData);
      return draft.id;
    } else {
      return await db.drafts.add(draftData);
    }
  },
  
  /**
   * Get all drafts
   * @param {string} type - Optional type filter
   * @returns {Promise<Array>} Array of drafts
   */
  async getDrafts(type = null) {
    if (type) {
      return await db.drafts.where('type').equals(type).reverse().sortBy('updatedAt');
    }
    return await db.drafts.orderBy('updatedAt').reverse().toArray();
  },
  
  /**
   * Get a specific draft by ID
   * @param {number} id - Draft ID
   * @returns {Promise<Object>} Draft data
   */
  async getDraft(id) {
    return await db.drafts.get(id);
  },
  
  /**
   * Delete a draft
   * @param {number} id - Draft ID
   * @returns {Promise<void>}
   */
  async deleteDraft(id) {
    // Also delete associated documents
    await db.documents.where('draftId').equals(id).delete();
    await db.drafts.delete(id);
  },
  
  /**
   * Save generated document
   * @param {Object} document - Document data
   * @param {number} document.draftId - Associated draft ID
   * @param {string} document.type - Document type
   * @param {string} document.format - 'pdf' | 'docx'
   * @param {Blob} document.blob - Document blob
   * @returns {Promise<number>} Document ID
   */
  async saveDocument(document) {
    const now = new Date().toISOString();
    
    return await db.documents.add({
      ...document,
      createdAt: now
    });
  },
  
  /**
   * Get documents for a draft
   * @param {number} draftId - Draft ID
   * @returns {Promise<Array>} Array of documents
   */
  async getDocuments(draftId) {
    return await db.documents.where('draftId').equals(draftId).toArray();
  }
};

/**
 * Settings service for user preferences
 */
export const settingsService = {
  /**
   * Get a setting value
   * @param {string} key - Setting key
   * @param {any} defaultValue - Default value if not found
   * @returns {Promise<any>} Setting value
   */
  async get(key, defaultValue = null) {
    const setting = await db.settings.get(key);
    return setting ? setting.value : defaultValue;
  },
  
  /**
   * Set a setting value
   * @param {string} key - Setting key
   * @param {any} value - Setting value
   * @returns {Promise<void>}
   */
  async set(key, value) {
    await db.settings.put({ key, value });
  },
  
  /**
   * Delete a setting
   * @param {string} key - Setting key
   * @returns {Promise<void>}
   */
  async delete(key) {
    await db.settings.delete(key);
  }
};

export default db;
