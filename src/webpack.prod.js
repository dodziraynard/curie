const common = require("./webpack.common");
const { merge } = require('webpack-merge');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = merge(common, {
    mode: "production",
    plugins: [
        new MiniCssExtractPlugin({ filename: "css/[name].[contenthash].bundle.css" })
    ],
    module: {
        rules: [
            {
                test: /\.scss$/,
                use: [
                    MiniCssExtractPlugin.loader, // Extracts CSS from js
                    "css-loader", // CSS into JS
                    "sass-loader", // SCSS into CSS
                ]
            }
        ]
    }
})
