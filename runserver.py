import getopt
import sys

from basic_auth import app


def main(argv):
    user = ''
    password = ''

    try:
        (opts, _) = getopt.getopt(argv, "u:p:d:")
    except getopt.GetoptError:
        printHelp()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-u"):
            user = arg
        elif opt in ("-p"):
            password = arg
        elif opt in ("-d"):
            backup_dir = arg

    if len(user) == 0 or len(password) == 0 or len(backup_dir) == 0:
        printHelp()
        sys.exit(0)

    print('User name is:',  user)
    print('Password is:', password)
    print('Backup directory:', backup_dir)
    app.config['USERNAME'] = user
    app.config['PASSWORD'] = password
    app.config['BACKUP_DIR'] = backup_dir


def printHelp():
    print('Usage: ', __file__,'-u <user name> -p <password> -d <backup_dir>')


if __name__ == '__main__':
    main(sys.argv[1:])
    context = ('ssl.cert', 'ssl.key')
    app.run(host='0.0.0.0', port=80, ssl_context=context)
