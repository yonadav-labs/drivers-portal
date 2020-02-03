const TerserPlugin = require('terser-webpack-plugin');
const terserOptions = require('./minify-options');

module.exports = {
  productionSourceMap: false,

  configureWebpack: {
    optimization: {
      splitChunks: false,
    },
    performance: {
      hints: false
    },
    output: {
      filename: 'main.js',
      chunkFilename: 'main.js',
    }
  },

  css: {
    extract: false,
    loaderOptions: {
      sass: {
        data: `@import "@/styles/index.scss";`,
      },
    },
  },

  transpileDependencies: ['vuex-module-decorators'],

  chainWebpack: config => {
    config.optimization.minimizer([
      new TerserPlugin(terserOptions),
    ]);
    config.plugin('html')
      .tap(args => {
        args[0].inject = false;
        return args;
      });
  }
}