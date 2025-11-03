/**
 * DualMind Extension - Content Script
 * Runs on all web pages to enable page interaction
 */

// Listen for messages from background script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getSelection') {
    const selectedText = window.getSelection().toString().trim();
    sendResponse({ text: selectedText });
  }
  
  if (request.action === 'getPageText') {
    const pageText = document.body.innerText;
    sendResponse({ text: pageText });
  }
  
  if (request.action === 'highlightText') {
    highlightSelectedText();
  }
  
  return true; // Keep message channel open
});

// Highlight selected text
function highlightSelectedText() {
  const selection = window.getSelection();
  if (selection.rangeCount > 0) {
    const range = selection.getRangeAt(0);
    const span = document.createElement('span');
    span.style.backgroundColor = '#ffeb3b';
    span.style.padding = '2px';
    
    try {
      range.surroundContents(span);
      
      // Remove highlight after 2 seconds
      setTimeout(() => {
        span.outerHTML = span.innerHTML;
      }, 2000);
    } catch (e) {
      // Silently fail if can't wrap selection
      console.debug('Could not highlight selection:', e);
    }
  }
}

// Keyboard shortcut listener
document.addEventListener('keydown', (e) => {
  // Ctrl+Shift+D / Cmd+Shift+D to open DualMind
  if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'D') {
    e.preventDefault();
    chrome.runtime.sendMessage({ action: 'openPopup' });
  }
});

console.log('🔗 DualMind content script loaded');

