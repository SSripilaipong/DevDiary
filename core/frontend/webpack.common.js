const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const ModuleFederationPlugin = require('webpack/lib/container/ModuleFederationPlugin');
const deps = require('./package.json').dependencies;

const APP_IDENTITY_BUCKET_NAME = process.env.APP_IDENTITY_BUCKET_NAME || 'devdiary.link/_s3/identity';
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
                identity: `identity@https://s3.ap-southeast-1.amazonaws.com/${APP_IDENTITY_BUCKET_NAME}/remoteEntry.js`,
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
