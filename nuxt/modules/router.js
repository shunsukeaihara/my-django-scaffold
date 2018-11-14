const resolve = require('path').resolve

module.exports = function() {
  this.nuxt.options.build.createRoutes = () => {
    return []
  }
  this.addTemplate({
    fileName: 'router.js',
    src: resolve(this.options.srcDir, 'router/index.js'),
  })
}