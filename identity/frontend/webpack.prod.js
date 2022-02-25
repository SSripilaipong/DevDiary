const { merge } = require('webpack-merge');
const ModuleFederationPlugin = require('webpack/lib/container/ModuleFederationPlugin');
const common = require('./webpack.common.js');

module.exports = merge(common, {
    mode: "production",
    plugins: [
        new ModuleFederationPlugin({
            name: 'identity',
            filename: 'remoteEntry.js',
            exposes: {
                './Register': './src/Register',
            },
        }),
    ],
})
