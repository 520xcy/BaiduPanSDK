import axios from 'axios';
import { ElNotification } from 'element-plus'

const service = axios.create({
    // process.env.NODE_ENV === 'development' 来判断是否开发环境
    // easy-mock服务挂了，暂时不使用了
    // baseURL: 'https://www.easy-mock.com/mock/592501a391470c0ac1fab128',
    timeout: 50000,

});

// 异常拦截处理器
const errorHandler = (error) => {
    let errorsmsg = {
        title: '',
        message: '',
    }
    if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        console.log(error.response.data);
        console.log(error.response.status);
        console.log(error.response.headers);
        errorsmsg.title = '错误'+error.response.status+' '+error.response.data.message;
      
        if (error.request.status == 401) {
            localStorage.removeItem("baidusdk");
            window.location.reload();
        } 
        if(Object.prototype.toString.call(error.response.data.errors) === '[object Object]'){
            for (const key in error.response.data.errors) {
                if (Object.hasOwnProperty.call(error.response.data.errors, key)) {
                    const element = error.response.data.errors[key];
                    errorsmsg.message += element.join(',');
                }
            }
        }else{
            errorsmsg.message = error.response.data.errors;
        }
    } else if (error.request) {
        // The request was made but no response was received
        // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
        // http.ClientRequest in node.js
        console.log(error.request);

    } else {
        // Something happened in setting up the request that triggered an Error
        console.log('Error', error.message);
    }
    ElNotification({
        title: errorsmsg.title,
        type: 'error',
        message: errorsmsg.message
    })
    console.log(error.message)
    return Promise.reject(error)

}

service.interceptors.request.use(
    config => {
        const token = localStorage.getItem("baidusdk")
        if (token) {
            config.headers['Baidusdk'] = token
        }
        return config;
    },
    errorHandler
);

service.interceptors.response.use(
    response => {
        const { data } = response

        if (data.code !== 200) {
            let title = '请求失败'

            ElNotification({
                title,
                message: data.message,
                type: 'error'
            })
            const reg = RegExp(/\"errno\":-6/);
            if (reg.test(data.message)) {
                window.location.href = "/#/login";
            }
            return Promise.reject(new Error(data.message || 'Error'))
        }
        return response
    },
    errorHandler
);

export default service;