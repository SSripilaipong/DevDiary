const { merge } = require('webpack-merge');
const ModuleFederationPlugin = require('webpack/lib/container/ModuleFederationPlugin');
const common = require('./webpack.common.js');

module.exports = merge(common, {
    mode: 'development',
    plugins: [
        new ModuleFederationPlugin({
            name: 'identity',
            filename: 'remoteEntry.js',
            remotes: {
                identity: `identity@https://s3.ap-southeast-1.amazonaws.com/devdiary.link-prod-identity-frontend/remoteEntry.js`,
            },
        }),
    ]
})
