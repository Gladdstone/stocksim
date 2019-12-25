const webpack = require('webpack');
const path = require('path');

module.exports = {  
    entry: path.join(__dirname, 'app', 'index.js'),  
    output: {
        path: path.join(__dirname, 'build'),
        publicPath: '/',
        filename: 'bundle.js'
    },
    devServer: {
        contentBase: path.join(__dirname, '/'),
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: ['babel-loader', 'eslint-loader']
            },
            {
                test: /\.less$/,
                use: [
                    {
                        loader: 'style-loader',     // creates style from JS strings
                    },
                    {
                        loader: 'css-loader',       // translates CSS into CommonJS
                    },
                    {
                        loader: 'less-loader',      // compiles less to CSS
                    },
                ],
            },
            {
                test: /\.css$/,
                use: [
                    {
                        loader: 'style-loader',
                    },
                    {
                        loader: 'css-loader',
                    }
                ]
            }
        ]
    },
};
