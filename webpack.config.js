// webpack v4
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const WebpackMd5Hash = require('webpack-md5-hash');
const MiniCssExtractPlugin = require("mini-css-extract-plugin"); // not needed, only to split them up
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const BundleTracker = require('webpack-bundle-tracker');

const forProduction = process.argv.indexOf('-p') > -1;

const baseName = forProduction ? '[name]-[hash].min.[ext]' : '[name].[ext]';

module.exports = {
  entry: { main: './klimaat_helpdesk/static/index.js' },
  output: {
    path: path.resolve('assets/bundles/'),
    filename: baseName.replace(/\[ext]/i, 'js')
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      },
      {
        test: /\.s[c|a]ss$/,
        use: ['style-loader', MiniCssExtractPlugin.loader, 'css-loader', 'postcss-loader', 'sass-loader']
      },
    ]
  },
  resolve: {
  modules: [
    '../node_modules',
    './klimaat_helpdesk/static/stylesheets',
    './klimaat_helpdesk/static/scripts',
  ],
  extensions: ['.js', '.scss'], // ,
},
  plugins: [
    new CleanWebpackPlugin({ cleanOnceBeforeBuildPatterns: [ 'build' ]}),  // Remove/clean build folders
    new MiniCssExtractPlugin({
      // filename: 'style.[contenthash].css',
      filename: 'style.css',
    }),
    new BundleTracker({
      filename: 'webpack-stats.json',
      path: process.cwd(),
    })
    // new ExtractTextPlugin({filename:'app.bundle.css'}),
    // new HtmlWebpackPlugin({
    //   inject: false,
    //   hash: true,
    //   template: './index.html',
    //   filename: 'index.html'
    // }),
    // new WebpackMd5Hash()
  ]
};
