import vue from '@vitejs/plugin-vue'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'

export default {
    base: './',
    plugins: [
        vue(),
        AutoImport({
            resolvers: [ElementPlusResolver()],
        }),
        Components({
            resolvers: [ElementPlusResolver()],
        }),
    ],
    build: {
        sourcemap: false,
        outDir: '../template', //指定输出路径
        assetsDir: 'assets', // 指定生成静态资源的存放路径
        rollupOptions: {
            output: {
                manualChunks(id) {
                    if (id.includes('node_modules')) {
                        const arr = id.toString().split('node_modules/')[1].split('/')
                        switch (arr[0]) {
                            case '@vue':
                            case 'element-plus':
                            case '@element-plus':
                                return '_' + arr[0]
                                break
                            default:
                                return '__vendor'
                                break
                        }
                    }
                }
            }
        }
    },
}