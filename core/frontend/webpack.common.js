const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const ModuleFederationPlugin = require('webpack/lib/container/ModuleFederationPlugin');
const deps = require('./package.json').dependencies;

const APP_IDENTITY_REMOTE_ENTRY = process.env.APP_IDENTITY_REMOTE_ENTRY || 'https://devdiary.link/_s3/identity/remoteEntry.js';
const ASSETS_PUBLIC_PATH = process.env.ASSETS_PUBLIC_PATH || '/';

module.exports = {
    entry: path.join(__dirname, "src", "index.js"),
    output: {
        path: path.resolve(__dirname, "dist"),
        publicPath: ASSETS_PUBLIC_PATH,
    },
    module: {
        rules: [
            {
                test: /\.?js$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader",
                    options: {
                        presets: ['@babel/preset-env', '@babel/preset-react'],
                    },
                },
            },
        ],
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: path.join(__dirname, "src", "index.html"),
        }),
        new ModuleFederationPlugin({
            name: 'core',
            filename: 'remoteEntry.js',
            remotes: {
                identity: `identity@${APP_IDENTITY_REMOTE_ENTRY}`,
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
    ]
}
