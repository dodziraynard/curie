const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");

module.exports = {
    entry: {
        vendor: "./static/js/vendor.js",
        main: "./static/js/index.js",
    },
    output: {
        filename: "js/[name].[contenthash].bundle.js",
        path: path.resolve(__dirname, "dist"),
    },
    plugins: [
        new HtmlWebpackPlugin({
            template:
                "./dashboard/templates/dashboard/base_template.html",
            filename: "templates/dashboard/base_template.html",
            publicPath: "/static/",
            inject: "body"
        }),
        new HtmlWebpackPlugin({
            template:
                "./accounts/templates/accounts/base_template.html",
            filename: "templates/accounts/base_template.html",
            publicPath: "/static/",
            inject: "body"
        }),
        new HtmlWebpackPlugin({
            template:
                "./website/templates/website/base_template.html",
            filename: "templates/website/base_template.html",
            publicPath: "/static/",
            inject: "body"
        }),
        new CleanWebpackPlugin(),
    ],
}
