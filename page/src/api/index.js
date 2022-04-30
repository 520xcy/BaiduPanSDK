export const host = "http://127.0.0.1:8182"
export const apiUrl = {
    getCode: host + '/login',
    getAccessToken: host + '/at',
    getUserinfo: host + '/userinfo',
    getSize: host + '/size',
    getList: host + '/list',
    getFilemeta: host + '/meta',
    getFiles: host + '/download',
    getRun: host + '/run',
    getStop: host + '/stop',
    getStatus: host + '/status',
    delTask: host + '/deltask',
    delFiles: host + '/delfiles'
}