const { merge } = require('webpack-merge');
const common = require('./webpack.common.js');
const ModuleFederationPlugin = require('webpack/lib/container/ModuleFederationPlugin');
const deps = require('./package.json').dependencies;

module.exports = merge(common, {
    mode: "production",
    plugins: [
        new ModuleFederationPlugin({
            name: 'identity',
            filename: 'remoteEntry.js',
            exposes: {
                './Register': './src/Pages/Register',
                './Service': './src/Service/Registration/Dummy',
            },
            shared: {
                ...deps,
                react: {
                    singleton: true,
                    requiredVersion: deps.react,
                },
                'react-dom': {
                    singleton: true,
                    requiredVersion: deps['react-dom'],
                },
            },
        }),
    ],
})
