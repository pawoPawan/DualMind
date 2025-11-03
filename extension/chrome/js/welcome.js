/**
 * DualMind Extension - Welcome Page Script
 * Handles first-time user onboarding
 */

document.addEventListener('DOMContentLoaded', () => {
  const getStartedBtn = document.getElementById('get-started-btn');
  
  if (getStartedBtn) {
    getStartedBtn.addEventListener('click', () => {
      // Send a message to the background script to open the extension
      chrome.runtime.sendMessage({ action: 'openPopup' }, () => {
        // Close this welcome tab
        window.close();
      });
    });
  }
});

