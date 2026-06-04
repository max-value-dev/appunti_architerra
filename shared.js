// shared.js — Shared Navigation and Interaction Logic

// Utility to change simulator tabs (used in Chapter 5)
function switchTab(name, btn) {
  document.querySelectorAll('.tabs-panel').forEach(p => p.classList.remove('on'));
  document.querySelectorAll('.tabs-btn').forEach(b => b.classList.remove('on'));
  const panel = document.getElementById('tab-' + name);
  if (panel) panel.classList.add('on');
  if (btn) btn.classList.add('on');
}

// Global script initialized when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  const sections = document.querySelectorAll('.section');
  const navItems = document.querySelectorAll('.nav-item');
  const currentFilename = window.location.pathname.split('/').pop() || 'index.html';

  // Highlight active sidebar item based on scroll position
  function scrollSpy() {
    let currentId = '';
    const scrollPosition = window.scrollY || document.documentElement.scrollTop;

    // Find the section currently in view
    sections.forEach(s => {
      // 120px offset to account for scrolling animations and header padding
      if (scrollPosition >= s.offsetTop - 140) {
        currentId = s.id;
      }
    });

    // If we scrolled past the top of the first section, or are at the top, highlight first section
    if (!currentId && sections.length > 0) {
      currentId = sections[0].id;
    }

    // Toggle 'active' class on sidebar items
    navItems.forEach(n => {
      const href = n.getAttribute('href');
      // Match the href anchor (e.g. "#s1" or "01_fondamenti.html#s1")
      if (href && (href === '#' + currentId || href.endsWith('#' + currentId))) {
        n.classList.add('active');
      } else {
        n.classList.remove('active');
      }
    });
  }

  // Handle local link clicking with smooth scroll
  navItems.forEach(n => {
    n.addEventListener('click', (e) => {
      const href = n.getAttribute('href');
      if (!href) return;

      // Extract file part and hash part
      const parts = href.split('#');
      const targetFile = parts[0] || currentFilename;
      const targetHash = parts[1];

      // If it's a local section on the current page, scroll smoothly
      if (targetFile === currentFilename || currentFilename.endsWith(targetFile) || !targetFile) {
        if (targetHash) {
          const targetEl = document.getElementById(targetHash);
          if (targetEl) {
            e.preventDefault();
            window.scrollTo({
              top: targetEl.offsetTop - 100,
              behavior: 'smooth'
            });
            // Update hash without jumping
            history.pushState(null, null, '#' + targetHash);
            
            // Highlight explicitly
            navItems.forEach(item => item.classList.remove('active'));
            n.classList.add('active');
          }
        }
      }
    });
  });

  // Listen to scroll and trigger scroll spy
  if (sections.length > 0) {
    window.addEventListener('scroll', scrollSpy);
    // Trigger once on load to ensure initial state is correct
    scrollSpy();

    // If page is loaded with a hash anchor, scroll to it smoothly after a tiny delay
    if (window.location.hash) {
      setTimeout(() => {
        const hash = window.location.hash.substring(1);
        const targetEl = document.getElementById(hash);
        if (targetEl) {
          window.scrollTo({
            top: targetEl.offsetTop - 100,
            behavior: 'smooth'
          });
        }
      }, 100);
    }
  }
});
