import ElementPlus from 'element-plus'
import * as ElIcons from '@element-plus/icons-vue'
import 'element-plus/theme-chalk/index.css'
import localeZH from 'element-plus/lib/locale/lang/zh-cn'

export default (app) => {
    for (const name in ElIcons) {
        app.component(name, ElIcons[name])
    }
    app.use(ElementPlus, { locale: localeZH })
}