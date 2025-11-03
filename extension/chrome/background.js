/**
 * DualMind Extension - Background Service Worker
 * Handles extension lifecycle, context menus, and commands
 */

// Extension installation/update handler
chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === 'install') {
    console.log('🎉 DualMind Extension installed!');
    
    // Set default settings
    chrome.storage.sync.set({
      theme: 'dark',
      defaultMode: 'local',
      quickAskEnabled: true
    });
    
    // Open welcome page
    chrome.tabs.create({
      url: chrome.runtime.getURL('welcome.html')
    });
  } else if (details.reason === 'update') {
    console.log('🔄 DualMind Extension updated!');
  }
  
  // Create context menu
  createContextMenus();
});

// Create context menus
function createContextMenus() {
  chrome.contextMenus.removeAll(() => {
    chrome.contextMenus.create({
      id: 'dualmind-ask',
      title: 'Ask DualMind: "%s"',
      contexts: ['selection']
    });
    
    chrome.contextMenus.create({
      id: 'dualmind-explain',
      title: 'Explain this with DualMind',
      contexts: ['selection']
    });
    
    chrome.contextMenus.create({
      id: 'dualmind-summarize',
      title: 'Summarize this page',
      contexts: ['page']
    });
  });
}

// Context menu click handler
chrome.contextMenus.onClicked.addListener((info, tab) => {
  const selectedText = info.selectionText || '';
  
  switch (info.menuItemId) {
    case 'dualmind-ask':
      openDualMindWithQuery(selectedText);
      break;
      
    case 'dualmind-explain':
      openDualMindWithQuery(`Explain: ${selectedText}`);
      break;
      
    case 'dualmind-summarize':
      getPageContent(tab.id).then(content => {
        openDualMindWithQuery(`Summarize this page: ${content.substring(0, 2000)}`);
      });
      break;
  }
});

// Command handler (keyboard shortcuts)
chrome.commands.onCommand.addListener((command) => {
  if (command === 'quick-ask') {
    // Get selected text from active tab
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0]) {
        chrome.tabs.sendMessage(tabs[0].id, { action: 'getSelection' }, (response) => {
          if (response && response.text) {
            openDualMindWithQuery(response.text);
          } else {
            openDualMind();
          }
        });
      }
    });
  }
});

// Open DualMind popup with optional query
function openDualMind() {
  chrome.action.openPopup();
}

function openDualMindWithQuery(query) {
  // Store query in storage for popup to read
  chrome.storage.local.set({ pendingQuery: query }, () => {
    chrome.action.openPopup();
  });
}

// Get page content
async function getPageContent(tabId) {
  try {
    const results = await chrome.scripting.executeScript({
      target: { tabId: tabId },
      function: () => document.body.innerText
    });
    return results[0].result || '';
  } catch (error) {
    console.error('Failed to get page content:', error);
    return '';
  }
}

// Message handler from popup/content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getPageContent') {
    if (sender.tab) {
      getPageContent(sender.tab.id).then(sendResponse);
      return true; // Will respond asynchronously
    }
  }
  
  if (request.action === 'openOptions') {
    chrome.runtime.openOptionsPage();
    sendResponse({ success: true });
  }
  
  if (request.action === 'openPopup') {
    // Open the popup programmatically
    chrome.action.openPopup();
    sendResponse({ success: true });
  }
});

// Keep service worker alive
let keepAliveInterval;

function keepAlive() {
  keepAliveInterval = setInterval(() => {
    chrome.runtime.getPlatformInfo(() => {
      // Just keep the worker alive
    });
  }, 20000); // Every 20 seconds
}

keepAlive();

console.log('🚀 DualMind Background Service Worker ready!');
