const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CopyWebpackPlugin = require("copy-webpack-plugin");
const ESLintPlugin = require('eslint-webpack-plugin');
const StylelintPlugin = require("stylelint-webpack-plugin");
const { WebpackManifestPlugin } = require('webpack-manifest-plugin');

const source = path.resolve(path.join("apps", "frontend", "static_src"));
const destination = path.resolve(path.join("apps", "frontend", "static"));

const config = {
  entry: {
    main: [
      path.join(source, "js", "main.js"),
      path.join(source, "scss", "main.scss"),
    ],
  },
  output: {
    path: destination,
    publicPath: "/static/",
    filename: "[name]-[fullhash].js",
    clean: true,
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        loader: "babel-loader",
      },
      {
        test: /\.(scss|css)$/,
        use: [
          MiniCssExtractPlugin.loader,
          {
            loader: "css-loader",
            options: {
              sourceMap: true,
            },
          },
          {
            loader: "postcss-loader",
            options: {
              sourceMap: true,
              postcssOptions: {
                syntax: "postcss-scss",
                plugins: ["postcss-preset-env"],
              },
            },
          },
          "sass-loader",
        ],
      },
    ],
  },
  plugins: [
    new ESLintPlugin({ failOnError: false }),
    new StylelintPlugin({ failOnError: false }),
    new MiniCssExtractPlugin({
      filename: "[name]-[fullhash].css",
    }),
    new CopyWebpackPlugin({
      patterns: [
        {
          from: path.join(source, "images"),
          to: path.join(destination, "images"),
        },
      ],
    }),
    new WebpackManifestPlugin({ publicPath: "" }),
  ],
};

module.exports = (env, argv) => {
  if (argv.mode === "development") {
    config.devtool = "inline-source-map";
  }
  return config;
};
