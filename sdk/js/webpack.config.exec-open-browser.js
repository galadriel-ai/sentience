const path = require('path');

module.exports = {
    mode: 'development',
    //DevServer is used for the test that the library is working on the browser
    devServer: {
        open: true,
        openPage: [`examples/example_for_browser.html`],
        contentBase: path.join(__dirname, '/'),
        quiet: true,
        port: 3000,
        host: `localhost`,
        disableHostCheck: true,
    }
};