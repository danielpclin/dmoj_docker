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
    loader: {
        paths: {
            mathjax: window.location.protocol + '//' + window.location.host + '/static/mathjax'
        }
    }
};
