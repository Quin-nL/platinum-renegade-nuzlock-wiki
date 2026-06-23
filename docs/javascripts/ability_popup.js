document$.subscribe(function () {
    var popup = document.getElementById('ability-popup');
    if (!popup) {
        popup = document.createElement('div');
        popup.id = 'ability-popup';
        document.body.appendChild(popup);
    }

    function showPopup(abbr) {
        var rect = abbr.getBoundingClientRect();
        popup.innerHTML = '<strong>' + abbr.textContent + '</strong><span>' + abbr.title + '</span>';
        popup.style.display = 'block';

        var left = rect.left + window.scrollX;
        var top = rect.bottom + window.scrollY + 6;

        // Keep within viewport horizontally
        var maxLeft = window.innerWidth - popup.offsetWidth - 10;
        popup.style.left = Math.max(10, Math.min(left, maxLeft)) + 'px';
        popup.style.top = top + 'px';
    }

    document.addEventListener('click', function (e) {
        var abbr = e.target.closest('abbr');
        if (abbr && abbr.title) {
            e.stopPropagation();
            if (popup.style.display === 'block' && popup.dataset.for === abbr.textContent) {
                popup.style.display = 'none';
                popup.dataset.for = '';
            } else {
                popup.dataset.for = abbr.textContent;
                showPopup(abbr);
            }
        } else {
            popup.style.display = 'none';
            popup.dataset.for = '';
        }
    });
});
