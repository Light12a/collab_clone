const CracoLessPlugin = require('craco-less');
const path = require("path");
module.exports = {
    webpack: {
        configure: {
            target: process.env.REACT_APP_PLATFORM === 'app' ? 'electron-renderer' : 'web'
        }
    },
    plugins: [
        {
            plugin: CracoLessPlugin,
            options: {
                lessLoaderOptions: {
                    // appendData: (loaderContext) => {
                    //     loaderContext.addDependency(path.resolve(__dirname, "./src/theme.js"));
                    //     loaderContext.cacheable(true);
                    //     delete require.cache[require.resolve('./src/theme')];
                    //     const { theme } = require("./src/theme");
                    //     return Object.entries(theme).map(([k, v]) => '@' + k + ':' + v + ';').join("\n");
                    // },
                    lessOptions: {
                        modifyVars: {
                             '@primary-color': '#99CC00',
                        //     '@success-color': '#000000'
                        },
                        javascriptEnabled: true,
                    },
                },

            },
        },
    ],
};