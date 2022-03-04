var nodemailer = require("nodemailer");
var log = require('electron-log');
var fs = require('fs');
const homedir = require('os').homedir();
const mainLogPath = homedir + '/AppData/Roaming/collabos/logs/main.log';
const rendererLogPath = homedir + '/AppData/Roaming/collabos/logs/renderer.log'

// async..await is not allowed in global scope, must use a wrapper
export async function sendMail(reciever) {
    log.info("sendMailService.js::sendMail() Log file receiver: " + reciever)
    log.info("sendMailService.js::sendMail() Logfile location: " + homedir + '/AppData/Roaming/collabos/logs/');

    var transporter = nodemailer.createTransport({
        service: "gmail",
        auth: {
            user: "collabosclient@gmail.com",
            pass: "unsecure"
        }
    });
    let files = [];
    if (ifExists(mainLogPath)) {
        files.push({   // file on disk as an attachment
            filename: 'main.log',
            path: mainLogPath // stream this file
        })
    }
    if (ifExists(rendererLogPath)) {
        files.push({   // file on disk as an attachment
            filename: 'renderer.log',
            path: rendererLogPath // stream this file
        })
    }

    log.info("sendMailService.js::sendMail() Logs files to be sent: ", JSON.stringify(files));

    const mailOptions = {
        from: 'collabosclient@gmail.com', // sender address
        to: reciever, // list of receivers
        subject: "CollabOS Phone Client Logs", // Subject line
        text: "This is log files send from CollabOS Phone", // plain text body
        attachments: files
    }

    // send mail with defined transport object
    transporter.sendMail(mailOptions, function (error, info) {
        if (error) {
            log.error('sendMailService.js::sendMail() ', error)
            return false;
        } else {
            log.info('sendMailService.js::sendMail() ', info.response)
            return true;
        }
    });
}

export const clearLogs = () => {
    if (ifExists(mainLogPath)) {
        fs.unlink(mainLogPath, function (err) {
            if (err) {
                log.error('sendMailService.js::clearLogs() ', err); return;
            }
            log.info('sendMailService.js::clearLogs() Main log is deleted successfully');
        });
    }

    if (ifExists(rendererLogPath)) {
        fs.unlink(rendererLogPath, function (err) {
            if (err) {
                log.error('sendMailService.js::clearLogs() ', err); return;
            }
            log.info('sendMailService.js::clearLogs() Renderer log is deleted successfully');
        });
    }
    return true;
}

const ifExists = (filePath) => {
    try {
        if (fs.existsSync(filePath)) {
            return true;
        }
    } catch (err) {
        log.error('sendMailService.js::ifExists() ', err);
        return false;
    }
}