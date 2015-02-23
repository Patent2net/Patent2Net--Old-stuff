function DetectBrowser() {
    if (navigator.userAgent.indexOf("Chrome") != -1) {
        alert('This website is not compliant with your browser, please come back with a nice browser like Firefox. ' +
                'We gonna close this website, thanks you !');
        close();
    }
}