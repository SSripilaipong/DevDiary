const { merge } = require('webpack-merge');
const ModuleFederationPlugin = require('webpack/lib/container/ModuleFederationPlugin');
const common = require('./webpack.common.js');

module.exports = merge(common, {
    mode: "production",
    plugins: [
        new ModuleFederationPlugin({
            name: 'core',
            filename: 'remoteEntry.js',
            exposes: {
                './Button': './src/Button',
            },
        }),
    ],
})
