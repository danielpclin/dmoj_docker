window.MathJax = {
    tex: {
        inlineMath: [
            ['~', '~'],
            ['\\(', '\\)']
        ]
    },
    options: {
        enableMenu: false
    },
    paths: {
        mathjax: window.location.protocol + '//' + window.location.host + '/static/mathjax'
    }
};
