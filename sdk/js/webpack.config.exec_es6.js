const path = require('path');

module.exports = {
    mode: 'development',
    devServer: {
        open: true,
        openPage: [`examples/example_for_es6.html`],
        contentBase: path.join(__dirname, '/'),
        quiet: true,
        port: 3001,
        host: `localhost`,
        disableHostCheck: true,
    },
    entry: {
        'use-from-es6': [`./examples/example_for_es6.js`],
    },
    output: {
        path: path.join(__dirname, '/'),
        publicPath: '/',
        filename: `[name].js`,
    },

    module: {
        rules: [{
            test: /\.js$/,
            exclude: /(node_modules|bower_components)/,
            use: [
                {
                    loader: 'babel-loader',
                }]
        }]
    },
};