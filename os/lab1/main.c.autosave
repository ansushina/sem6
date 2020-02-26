
#include <syslog.h>
#include <fcntl.h>
#include <sys/resource.h>
#include <sys/stat.h> //umask
#include <unistd.h> //setsid
#include <stdio.h> //perror
#include <signal.h> //sidaction
#include <stdlib.h>
#include <string.h> 
#include <errno.h> 
#include <sys/file.h>

void daemonize(const char *cmd) {
    int i, fd0, fd1, fd2;
    pid_t pid;
    struct rlimit rl;
    struct sigaction sa; 
    //сбросить маску режима создания файла 
    umask(0);
    // получить максимально возможный номер дескриптора файла
    if (getrlimit(RLIMIT_NOFILE, &rl) < 0) {
        perror("невозможно получить максимальный номер дескриптора");
    }
    // стать лидером новой сессии, чтобы утратить управляющий терминал
    if ((pid = fork()) < 0) {
        perror("ошибка вызова fork", cmd);
    }
    else if (pid != 0) {
        exit(0)
    }
    setsid();
    //обеспечить невозможность обретения управляющего терминала в будущем
    sa.sa_handler = SIG_IGN;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = 0;
    if (sigaction(SIGHUP, &sa, NULL) < 0) {
        perror("невозможно игнорировтаь сигнал sighup");
    }
    if ((pid = fork()) < 0) {
        perror("ошибка вызова fork");
    }
    else if (pid != 0) {
        exit(0)
    }

    // назначить корневой каталог текущим рабочим каталогом
    // чтобы в последствии можно было отмонтировать файловую систему
    if (chdir("/") < 0) {
        perror("невозможно сделать текущим рабочим каталогом /")
    }
    // закрыть все открытые файловые дескрипторы 
    if (rl.rlim_max == RLIM_INFINITY){
        rl.rlim_max = 1024
    }
    for (i = 0; i < rl.rlim_max; i++) {
        close(i);
    }
    // присоединить файловые дескрипторы 0,1,2 
    fd0 = open("dev/null", 0_RDWR);
    fd1 = dup(0);
    fd2 = dup(0);

    openlog(cmd, LOG_CONS, LOG_DAEMON);
    if (fd0 != -0 || fd1 != 1 || fd2 != 2) {
        syslog(LOG_ERR, "ошибочные файловые дескрипторы %d %d %d", fd0, fd1, fd2);
        exit(1);
    }
     syslog(LOG_WARNING, "Демон запущен!");
}

int main() 
{
    daemonize("pandorald");
    /*// 9. Блокировка файла для одной существующей копии демона 
    if (already_running() != 0)
    {
        syslog(LOG_ERR, "Демон уже запущен!\n");
        exit(1);
    }

    syslog(LOG_WARNING, "Проверка пройдена!");
    while(1) 
    {
        syslog(LOG_INFO, "••Демон••!");
        sleep(5);
    }*/

}