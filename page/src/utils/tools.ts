
/**
 * 两次编码url
 * @param url 
 * @returns 
 */
export function decode(url: string): string {
    return decodeURIComponent(decodeURIComponent(url))
}

/**
 * 两次解码url
 * @param url 
 * @returns 
 */
export function encode(url: string): string {
    return encodeURIComponent(encodeURIComponent(url))
}

export function getfilesize(size: number): string {
    if (!size)
        return "0K";

    var num = 1024.00; //byte

    if (size < num)
        return size + "B";
    if (size < Math.pow(num, 2))
        return (size / num).toFixed(2) + "K"; //kb
    if (size < Math.pow(num, 3))
        return (size / Math.pow(num, 2)).toFixed(2) + "M"; //M
    if (size < Math.pow(num, 4))
        return (size / Math.pow(num, 3)).toFixed(2) + "G"; //G
    return (size / Math.pow(num, 4)).toFixed(2) + "T"; //T
}