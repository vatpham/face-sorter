window.addEventListener('beforeunload', function (e) {
    e.preventDefault();
    e.returnValue = '';
});

window.addEventListener('popstate', function () {
    const ok = confirm('Leave results and go back?');
    if (!ok) history.forward();
});

