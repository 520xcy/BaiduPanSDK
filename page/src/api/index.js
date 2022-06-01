export const host = "http://" + document.domain + ":8182"
export const apiUrl = {
    getLogin: host + '/api/login',
    getCode: host + '/api/code',
    getAccessToken: host + '/api/at',
    getUserinfo: host + '/api/userinfo',
    getSize: host + '/api/size',
    getList: host + '/api/list',
    getFilemeta: host + '/api/meta',
    getFiles: host + '/api/download',
    getRun: host + '/api/run',
    getStop: host + '/api/stop',
    getStatus: host + '/api/status',
    delTask: host + '/api/deltask',
    delFiles: host + '/api/delfiles',
    logOut: host + '/api/logout'
}