document$.subscribe(function () {
    const STAT_MAX = 255;
    const BST_MAX = 780;
    const STAT_COLS = ['HP', 'Atk', 'Def', 'SAtk', 'SDef', 'Spd'];

    function findNextTable(heading) {
        var el = heading.nextElementSibling;
        while (el && el.tagName !== 'H1' && el.tagName !== 'H2') {
            if (el.tagName === 'TABLE') return el;
            var inner = el.querySelector('table');
            if (inner) return inner;
            el = el.nextElementSibling;
        }
        return null;
    }

    // Hide "Version" column from small info tables (Type, Ability, Base Stats)
    document.querySelectorAll('table').forEach(function (table) {
        var headers = table.querySelectorAll('thead th');
        if (!headers.length || headers[0].textContent.trim() !== 'Version') return;
        if (headers.length > 9) return;
        headers[0].style.display = 'none';
        table.querySelectorAll('tbody td:first-child').forEach(function (td) {
            td.style.display = 'none';
        });
    });

    // Add stat bars to Base Stats tables
    document.querySelectorAll('h2').forEach(function (h2) {
        if (!h2.textContent.includes('Base Stats')) return;

        var table = findNextTable(h2);
        if (!table) return;

        var headers = Array.from(table.querySelectorAll('thead th')).map(function (th) {
            return th.textContent.trim();
        });

        table.querySelectorAll('tbody tr').forEach(function (row) {
            var cells = row.querySelectorAll('td');
            headers.forEach(function (header, i) {
                if (!cells[i]) return;
                var isStat = STAT_COLS.includes(header);
                var isBst = header === 'BST';
                if (!isStat && !isBst) return;

                var val = parseInt(cells[i].textContent.trim());
                if (isNaN(val)) return;

                var max = isBst ? BST_MAX : STAT_MAX;
                var pct = Math.min(val / max * 100, 100);
                var hue = pct * 1.2; // 0-100 -> 0-120 (red to green)

                cells[i].innerHTML =
                    '<div class="stat-cell">' +
                    '<span class="stat-value">' + val + '</span>' +
                    '<div class="stat-bar-bg">' +
                    '<div class="stat-bar" style="width:' + pct + '%;background:hsl(' + hue + ',65%,42%)"></div>' +
                    '</div>' +
                    '</div>';
            });
        });
    });
});
