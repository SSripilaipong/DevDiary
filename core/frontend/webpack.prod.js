const { merge } = require('webpack-merge');
const ModuleFederationPlugin = require('webpack/lib/container/ModuleFederationPlugin');
const common = require('./webpack.common.js');

const APP_IDENTITY_BUCKET_NAME = process.env.APP_IDENTITY_BUCKET_NAME;

module.exports = merge(common, {
    mode: "production",
    plugins: [
        new ModuleFederationPlugin({
            name: 'identity',
            filename: 'remoteEntry.js',
            remotes: {
                identity: `identity@https://s3.ap-southeast-1.amazonaws.com/${APP_IDENTITY_BUCKET_NAME}/remoteEntry.js`,
            },
        }),
    ],
})
