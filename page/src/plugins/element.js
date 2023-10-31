import ElementPlus from 'element-plus'
import * as ElIcons from '@element-plus/icons-vue'
import 'element-plus/theme-chalk/index.css'
import zhCn from 'element-plus/dist/locale/zh-cn'

export default (app) => {
    for (const name in ElIcons) {
        app.component(name, ElIcons[name])
    }
    app.use(ElementPlus, { locale: zhCn })
}