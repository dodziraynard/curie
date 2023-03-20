const common = require("./webpack.common");
const { merge } = require('webpack-merge');

module.exports = merge(common, {
    mode: "development",
    module: {
        rules: [
            {
                test: /\.scss$/,
                use: [
                    "style-loader", // Inject CSS into DOM
                    "css-loader", // CSS into JS
                    "sass-loader", // SCSS into CSS
                ]
            }
        ]
    }
});