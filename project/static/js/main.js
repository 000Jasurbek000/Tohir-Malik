document.addEventListener('DOMContentLoaded', function () {
    const siteHeader = document.querySelector('.site-header');
    const siteFooter = document.querySelector('.site-footer');
    if (siteHeader) {
        const updateHeaderState = () => {
            siteHeader.classList.toggle('scrolled', window.scrollY > 40);
            if (siteFooter) {
                const headerHeight = siteHeader.getBoundingClientRect().height;
                const footerTop = siteFooter.getBoundingClientRect().top;
                siteHeader.classList.toggle('on-dark', footerTop <= headerHeight);
            }
        };
        updateHeaderState();
        window.addEventListener('scroll', updateHeaderState, { passive: true });
        window.addEventListener('resize', updateHeaderState);
    }

    const revealItems = document.querySelectorAll('.reveal');
    if (revealItems.length) {
        const revealObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                entry.target.classList.add('in-view');
                revealObserver.unobserve(entry.target);
            });
        }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });

        let groupIndex = 0;
        let lastParent = null;
        revealItems.forEach((item) => {
            if (item.parentElement !== lastParent) {
                groupIndex = 0;
                lastParent = item.parentElement;
            }
            item.style.transitionDelay = `${Math.min(groupIndex, 6) * 90}ms`;
            groupIndex += 1;
            revealObserver.observe(item);
        });
    }

    const dictCards = document.querySelectorAll('.dict-card');
    const dictEmptyState = document.querySelector('.dict-empty-state');
    const dictResultsHead = document.querySelector('.dict-results-head');
    const searchInput = document.getElementById('dict-search-input');
    const searchButton = document.getElementById('dict-search-button');
    const alphaButtons = document.querySelectorAll('.alpha-tag');
    let activeLetter = null;

    if (dictCards.length) {
        const applyFilters = () => {
            const query = searchInput ? searchInput.value.trim().toLowerCase() : '';
            let visibleCount = 0;

            dictCards.forEach((card) => {
                const title = (card.querySelector('h2')?.textContent || '').trim();
                const meaning = (card.querySelector('.dict-card-meaning')?.textContent || '').trim();
                const text = `${title} ${meaning}`.toLowerCase();
                const shouldShowBySearch = !query || text.includes(query);
                const firstLetter = title.charAt(0).toUpperCase();
                const isLetterMatch = !activeLetter || firstLetter === activeLetter || (activeLetter === 'O‘' && firstLetter === 'O') || (activeLetter === 'G‘' && firstLetter === 'G') || (activeLetter === 'Sh' && firstLetter === 'S') || (activeLetter === 'Ch' && firstLetter === 'C') || (activeLetter === 'Ng' && firstLetter === 'N');
                const match = shouldShowBySearch && isLetterMatch;
                card.hidden = !match;
                if (match) visibleCount += 1;
            });

            if (dictEmptyState) dictEmptyState.hidden = visibleCount > 0;
            if (dictResultsHead) dictResultsHead.hidden = visibleCount === 0;
        };

        alphaButtons.forEach((btn) => {
            btn.addEventListener('click', () => {
                const letter = btn.dataset.letter;
                const isActive = activeLetter === letter;
                alphaButtons.forEach((b) => b.classList.toggle('active', b === btn && !isActive));
                activeLetter = isActive ? null : letter;
                applyFilters();
            });
        });

        if (searchInput && searchButton) {
            searchButton.addEventListener('click', applyFilters);
            searchInput.addEventListener('input', applyFilters);
            searchInput.addEventListener('keydown', (event) => {
                if (event.key === 'Enter') {
                    applyFilters();
                }
            });
        }
    }

    const menuToggle = document.querySelector('.menu-toggle');
    const mainNav = document.querySelector('.main-nav');

    if (menuToggle && mainNav) {
        menuToggle.addEventListener('click', function () {
            const isOpen = mainNav.classList.toggle('open');
            menuToggle.setAttribute('aria-expanded', String(isOpen));
        });
    }

    const animatedNumbers = document.querySelectorAll('[data-count]');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (!entry.isIntersecting) return;

            const el = entry.target;
            const target = Number(el.dataset.count || 0);
            const duration = 1400;
            const start = performance.now();

            const tick = (now) => {
                const progress = Math.min((now - start) / duration, 1);
                const eased = 1 - Math.pow(1 - progress, 3);
                const value = Math.round(target * eased);
                el.textContent = value.toLocaleString('uz-UZ');

                if (progress < 1) {
                    requestAnimationFrame(tick);
                } else {
                    el.textContent = target.toLocaleString('uz-UZ');
                }
            };

            requestAnimationFrame(tick);
            observer.unobserve(el);
        });
    }, { threshold: 0.4 });

    animatedNumbers.forEach((item) => observer.observe(item));

    const fadeItems = document.querySelectorAll('.feature-card, .stat-box, .article-card, .contact-card, .info-card, .quote-box, .phrase-item');
    fadeItems.forEach((item, index) => {
        item.classList.add('fade-up');
        item.style.animationDelay = `${index * 80}ms`;
    });

    const homeSearchInput = document.getElementById('home-search-input');
    const homeSearchButton = document.getElementById('home-search-button');

    if (homeSearchInput && homeSearchButton) {
        const submitHomeSearch = () => {
            const value = homeSearchInput.value.trim();
            const baseUrl = '/dictionary';
            const params = new URLSearchParams();
            if (value) params.set('q', value);
            window.location.href = params.toString() ? `${baseUrl}?${params.toString()}` : baseUrl;
        };

        homeSearchButton.addEventListener('click', submitHomeSearch);
        homeSearchInput.addEventListener('keydown', function (event) {
            if (event.key === 'Enter') {
                submitHomeSearch();
            }
        });
    }
});
