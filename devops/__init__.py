import sys
import mimetypes

from loguru import logger

config = {
    'handlers': [
        {
            'sink'      : sys.stdout,
            'format'    : '<green>{time:YYYY:MM:DD HH:mm:ss.SSS}</green> [<level>{level}</level>] <level><n>{message}</n></level>',
            'colorize'  : True,
            'level'     : 'INFO'
        }
    ],
}
logger.configure(**config)

mimetypes.types_map.update({
    '.aac'  : 'audio/aac',
    '.abw'  : 'application/x-abiword',
    '.arc'  : 'application/octet-stream',
    '.avi'  : 'video/x-msvideo',
    '.azw'  : 'application/vnd.amazon.ebook',
    '.bin'  : 'application/octet-stream',
    '.bz'   : 'application/x-bzip',
    '.bz2'  : 'application/x-bzip2',
    '.csh'  : 'application/x-csh',
    '.css'  : 'text/css',
    '.csv'  : 'text/csv',
    '.doc'  : 'application/msword',
    '.eot'  : 'application/vnd.ms-fontobject',
    '.epub' : 'application/epub+zip',
    '.gif'  : 'image/gif',
    '.htm'  : 'text/html',
    '.html' : 'text/html',
    '.ico'  : 'image/x-icon',
    '.ics'  : 'text/calendar',
    '.jar'  : 'application/java-archive',
    '.jpeg' : 'image/jpeg',
    '.jpg'  : 'image/jpeg',
    '.js'   : 'application/javascript',
    '.json' : 'application/json',
    '.mid'  : 'audio/midi',
    '.midi' : 'audio/midi',
    '.mpeg' : 'video/mpeg',
    '.mpkg' : 'application/vnd.apple.installer+xml',
    '.odp'  : 'application/vnd.oasis.opendocument.presentation',
    '.ods'  : 'application/vnd.oasis.opendocument.spreadsheet',
    '.odt'  : 'application/vnd.oasis.opendocument.text',
    '.oga'  : 'audio/ogg',
    '.ogv'  : 'video/ogg',
    '.ogx'  : 'application/ogg',
    '.otf'  : 'font/otf',
    '.png'  : 'image/png',
    '.pdf'  : 'application/pdf',
    '.ppt'  : 'application/vnd.ms-powerpoint',
    '.rar'  : 'application/x-rar-compressed',
    '.rtf'  : 'application/rtf',
    '.sh'   : 'application/x-sh',
    '.svg'  : 'image/svg+xml',
    '.swf'  : 'application/x-shockwave-flash',
    '.tar'  : 'application/x-tar',
    '.tif'  : 'image/tiff',
    '.tiff' : 'image/tiff',
    '.ts'   : 'application/typescript',
    '.ttf'  : 'font/ttf',
    '.vsd'  : 'application/vnd.visio',
    '.wav'  : 'audio/x-wav',
    '.weba' : 'audio/webm',
    '.webm' : 'video/webm',
    '.webp' : 'image/webp',
    '.woff' : 'font/woff',
    '.woff2': 'font/woff2',
    '.xhtml': 'application/xhtml+xml',
    '.xls'  : 'application/vnd.ms-excel',
    '.xlsx' : 'application/vnd.ms-excel',
    '.xml'  : 'application/xml',
    '.xul'  : 'application/vnd.mozilla.xul+xml',
    '.zip'  : 'application/zip',
    '.7z'   : 'application/x-7z-compressed'
})