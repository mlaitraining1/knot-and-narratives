/* ==========================================================================
   THE KNOT & NARRATIVES — site.js
   Vanilla JS, no dependencies. Progressive enhancement throughout.
   ========================================================================== */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------- Hero background slideshow (images + one video slide) ---------------- */
  document.querySelectorAll('[data-hero-slideshow]').forEach(function (wrap) {
    var slides = wrap.querySelectorAll('.hero-slide');
    if (slides.length < 2 || reduceMotion) return;
    var current = 0;
    var fallbackTimer;

    function activate(i) {
      var prev = slides[current];
      if (prev.tagName === 'VIDEO') { prev.pause(); }
      prev.classList.remove('is-active');
      current = i;
      slides[current].classList.add('is-active');
      schedule();
    }

    function goNext() { activate((current + 1) % slides.length); }

    function schedule() {
      clearTimeout(fallbackTimer);
      var el = slides[current];
      if (el.tagName === 'VIDEO') {
        el.currentTime = 0;
        var p = el.play();
        if (p && p.catch) { p.catch(function () { /* autoplay blocked — fallback timer still advances */ }); }
        el.addEventListener('ended', goNext, { once: true });
        // Safety net in case 'ended' never fires (autoplay blocked, load error, etc.)
        fallbackTimer = setTimeout(goNext, 9000);
      } else {
        fallbackTimer = setTimeout(goNext, 5500);
      }
    }

    schedule();
  });

  /* ---------------- Header scroll state ---------------- */
  var header = document.querySelector('.site-header');
  function onScroll() {
    if (!header) return;
    if (window.scrollY > 40) header.classList.add('is-scrolled');
    else header.classList.remove('is-scrolled');
  }
  document.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------------- Mobile nav ---------------- */
  var navToggle = document.querySelector('.nav-toggle');
  var mobileNav = document.querySelector('.mobile-nav');
  if (navToggle && mobileNav) {
    navToggle.addEventListener('click', function () {
      var isOpen = mobileNav.classList.toggle('is-open');
      document.body.classList.toggle('nav-open', isOpen);
      navToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
    mobileNav.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        mobileNav.classList.remove('is-open');
        document.body.classList.remove('nav-open');
      });
    });
  }

  /* ---------------- Scroll reveal ---------------- */
  var revealEls = document.querySelectorAll('.reveal, .stagger');
  if ('IntersectionObserver' in window && !reduceMotion) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -60px 0px' });
    revealEls.forEach(function (el) { io.observe(el); });

    var threadEls = document.querySelectorAll('.thread-path');
    var threadIo = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-drawn');
          threadIo.unobserve(entry.target);
        }
      });
    }, { threshold: 0.3 });
    threadEls.forEach(function (el) { threadIo.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('is-visible'); });
    document.querySelectorAll('.thread-path').forEach(function (el) { el.classList.add('is-drawn'); });
  }

  /* ---------------- Testimonial slider ---------------- */
  document.querySelectorAll('[data-testimonial-slider]').forEach(function (slider) {
    var slides = slider.querySelectorAll('.testimonial-slide');
    var dotsWrap = slider.querySelector('.testimonial-dots');
    var current = 0, timer;
    if (!slides.length) return;
    if (dotsWrap) {
      slides.forEach(function (_, i) {
        var b = document.createElement('button');
        b.setAttribute('aria-label', 'Show testimonial ' + (i + 1));
        if (i === 0) b.classList.add('is-active');
        b.addEventListener('click', function () { go(i); resetTimer(); });
        dotsWrap.appendChild(b);
      });
    }
    function go(i) {
      slides[current].classList.remove('is-active');
      dotsWrap && dotsWrap.children[current] && dotsWrap.children[current].classList.remove('is-active');
      current = (i + slides.length) % slides.length;
      slides[current].classList.add('is-active');
      dotsWrap && dotsWrap.children[current] && dotsWrap.children[current].classList.add('is-active');
    }
    function resetTimer() {
      clearInterval(timer);
      if (!reduceMotion) timer = setInterval(function () { go(current + 1); }, 6000);
    }
    resetTimer();
  });

  /* ---------------- FAQ accordion ---------------- */
  document.querySelectorAll('.faq-item').forEach(function (item) {
    var q = item.querySelector('.faq-q');
    var a = item.querySelector('.faq-a');
    if (!q || !a) return;
    q.addEventListener('click', function () {
      var isOpen = item.classList.contains('is-open');
      item.parentElement.querySelectorAll('.faq-item').forEach(function (other) {
        other.classList.remove('is-open');
        other.querySelector('.faq-a').style.maxHeight = null;
        other.querySelector('.faq-q').setAttribute('aria-expanded', 'false');
      });
      if (!isOpen) {
        item.classList.add('is-open');
        a.style.maxHeight = a.scrollHeight + 'px';
        q.setAttribute('aria-expanded', 'true');
      }
    });
  });

  /* ---------------- Portfolio filter ---------------- */
  var filterBar = document.querySelector('.filter-bar');
  if (filterBar) {
    var items = document.querySelectorAll('.masonry-item');
    filterBar.addEventListener('click', function (e) {
      var btn = e.target.closest('.filter-btn');
      if (!btn) return;
      filterBar.querySelectorAll('.filter-btn').forEach(function (b) { b.classList.remove('is-active'); });
      btn.classList.add('is-active');
      var filter = btn.dataset.filter;
      items.forEach(function (item) {
        var show = filter === 'all' || item.dataset.category === filter;
        item.hidden = !show;
      });
    });
  }

  /* ---------------- Lightbox ---------------- */
  var lightbox = document.querySelector('.lightbox');
  if (lightbox) {
    var lbImg = lightbox.querySelector('img');
    var lbCaption = lightbox.querySelector('.lightbox-caption');
    var galleryItems = Array.prototype.slice.call(document.querySelectorAll('[data-lightbox-src]'));
    var lbIndex = 0;

    function openLightbox(i) {
      lbIndex = i;
      var el = galleryItems[lbIndex];
      lbImg.src = el.dataset.lightboxSrc;
      lbImg.alt = el.dataset.lightboxAlt || '';
      if (lbCaption) lbCaption.textContent = el.dataset.lightboxCaption || '';
      lightbox.classList.add('is-open');
      document.body.classList.add('nav-open');
    }
    function closeLightbox() {
      lightbox.classList.remove('is-open');
      document.body.classList.remove('nav-open');
    }
    galleryItems.forEach(function (el, i) {
      el.addEventListener('click', function () { openLightbox(i); });
    });
    var closeBtn = lightbox.querySelector('.lightbox-close');
    var prevBtn = lightbox.querySelector('.lightbox-prev');
    var nextBtn = lightbox.querySelector('.lightbox-next');
    closeBtn && closeBtn.addEventListener('click', closeLightbox);
    lightbox.addEventListener('click', function (e) { if (e.target === lightbox) closeLightbox(); });
    prevBtn && prevBtn.addEventListener('click', function () { openLightbox((lbIndex - 1 + galleryItems.length) % galleryItems.length); });
    nextBtn && nextBtn.addEventListener('click', function () { openLightbox((lbIndex + 1) % galleryItems.length); });
    document.addEventListener('keydown', function (e) {
      if (!lightbox.classList.contains('is-open')) return;
      if (e.key === 'Escape') closeLightbox();
      if (e.key === 'ArrowRight') nextBtn && nextBtn.click();
      if (e.key === 'ArrowLeft') prevBtn && prevBtn.click();
    });
  }

  /* ---------------- Contact form (client-side validation + demo submit) ---------------- */
  var contactForm = document.querySelector('#contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var status = contactForm.querySelector('.form-status');
      var required = contactForm.querySelectorAll('[required]');
      var valid = true;
      required.forEach(function (field) {
        if (!field.value.trim()) valid = false;
      });
      if (!valid) {
        if (status) { status.textContent = 'Please fill in all required fields.'; status.style.color = '#B23A2E'; }
        return;
      }
      var btn = contactForm.querySelector('button[type="submit"]');
      var originalText = btn ? btn.textContent : '';
      if (btn) { btn.textContent = 'Sending…'; btn.disabled = true; }
      // NOTE: Replace this timeout with a real submission call — e.g. to
      // Formspree, Getform, a serverless function on Vercel, or your CRM.
      setTimeout(function () {
        if (status) { status.textContent = "Thank you — your inquiry has been received. We'll reply within 24 hours."; status.style.color = '#3B6B4E'; }
        contactForm.reset();
        if (btn) { btn.textContent = originalText; btn.disabled = false; }
      }, 900);
    });
  }

  /* ---------------- Client gallery demo login ---------------- */
  var galleryForm = document.querySelector('#gallery-login-form');
  if (galleryForm) {
    galleryForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var locked = document.querySelector('.gallery-locked-grid');
      var status = galleryForm.querySelector('.form-status');
      var code = galleryForm.querySelector('#gallery-code');
      if (code && code.value.trim().toUpperCase() === 'DEMO2026') {
        if (locked) {
          locked.querySelector('.masonry').style.filter = 'none';
          locked.querySelector('.masonry').style.pointerEvents = 'auto';
          locked.querySelector('.overlay-cta').style.display = 'none';
        }
        if (status) { status.textContent = ''; }
      } else if (status) {
        status.textContent = 'Try demo code DEMO2026 to preview this gallery.';
        status.style.color = '#B23A2E';
      }
    });
  }

  /* ---------------- Current year in footer ---------------- */
  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

})();
