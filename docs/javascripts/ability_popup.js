(function () {
    var popup = null;
    var activeAbbr = null;

    function init() {
        if (document.getElementById('ability-popup')) return;

        popup = document.createElement('div');
        popup.id = 'ability-popup';
        document.body.appendChild(popup);

        document.addEventListener('click', handleClick, true);
    }

    function handleClick(e) {
        var abbr = e.target.closest ? e.target.closest('abbr') :
            (e.target.tagName === 'ABBR' ? e.target : null);

        if (abbr && abbr.title) {
            e.stopPropagation();
            if (abbr === activeAbbr && popup.style.display === 'block') {
                hidePopup();
            } else {
                showPopup(abbr);
            }
        } else if (popup && !popup.contains(e.target)) {
            hidePopup();
        }
    }

    function showPopup(abbr) {
        activeAbbr = abbr;
        var rect = abbr.getBoundingClientRect();
        popup.innerHTML = '<strong>' + abbr.textContent + '</strong><span>' + abbr.title + '</span>';
        popup.style.display = 'block';

        var left = rect.left;
        var top = rect.bottom + 6;
        var maxLeft = window.innerWidth - popup.offsetWidth - 10;

        popup.style.left = Math.max(10, Math.min(left, maxLeft)) + 'px';
        popup.style.top = top + 'px';
    }

    function hidePopup() {
        if (popup) popup.style.display = 'none';
        activeAbbr = null;
    }

    if (typeof document$ !== 'undefined') {
        document$.subscribe(init);
    } else {
        document.addEventListener('DOMContentLoaded', init);
    }
})();
