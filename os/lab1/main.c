
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
#include <time.h>

#define LOCKFILE "/var/run/daemon.pid"
#define LOCKMODE (S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH) 

int lockfile(int fd)
{
    struct flock fl;
    fl.l_type = F_WRLCK;
    fl.l_start = 0;
    fl.l_whence = SEEK_SET;
    fl.l_len = 0;
    return(fcntl(fd, F_SETLK, &fl));
}

int already_running(void)
{

    syslog(LOG_ERR, "Проверка на многократный запуск!");

    int fd;
    char buf[16];

    fd = open(LOCKFILE, O_RDWR | O_CREAT, LOCKMODE);

    if (fd < 0)
    {
        syslog(LOG_ERR, "невозможно открыть %s: %s!", LOCKFILE, strerror(errno));
        exit(1);
    }

    syslog(LOG_WARNING, "Lock-файл открыт!");

    if (lockfile(fd) < 0)
    {
         if (errno == EACCES || errno == EAGAIN)
         {
             close(fd);
             exit(1);
         }

         syslog(LOG_ERR, "невозможно установить блокировку на %s: %s!\n", LOCKFILE, strerror(errno));
         exit(1);
    }
    /*flock(fd, LOCK_EX | LOCK_UN);
    if (errno == EWOULDBLOCK) {
        syslog(LOG_ERR, "невозможно установить блокировку на %s: %s!", LOCKFILE, strerror(errno));
        close(fd);
        exit(1);
    }*/

    syslog(LOG_WARNING, "Записываем PID!");

    ftruncate(fd, 0);
    sprintf(buf, "%ld", (long)getpid());
    write(fd, buf, strlen(buf) + 1);

    syslog(LOG_WARNING, "Записали PID!");
     
    return 0;
}

void daemonize(const char *cmd) {
    int i, fd0, fd1, fd2;
    pid_t pid;
    struct rlimit rl;
    struct sigaction sa; 
    // 1 сбросить маску режима создания файла 
    umask(0);
    // получить максимально возможный номер дескриптора файла
    if (getrlimit(RLIMIT_NOFILE, &rl) < 0) {
        perror("невозможно получить максимальный номер дескриптора");
    }
    // 2  стать лидером новой сессии, чтобы утратить управляющий терминал
    if ((pid = fork()) < 0) {
        perror("ошибка вызова fork");
    }
    else if (pid != 0) {
        exit(0);
    }
    setsid();
    //3 обеспечить невозможность обретения управляющего терминала в будущем
    sa.sa_handler = SIG_IGN;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = 0;
    if (sigaction(SIGHUP, &sa, NULL) < 0) {
        perror("невозможно игнорировтаь сигнал sighup");
    }

  /*  if ((pid = fork()) < 0) {
        perror("ошибка вызова fork");
    }
    else if (pid != 0) {
        exit(0);

    }*/

    // 4 назначить корневой каталог текущим рабочим каталогом
    // чтобы в последствии можно было отмонтировать файловую систему
    if (chdir("/") < 0) {
        perror("невозможно сделать текущим рабочим каталогом /");
    }
    // 5 закрыть все открытые файловые дескрипторы
    if (rl.rlim_max == RLIM_INFINITY){
        rl.rlim_max = 1024;
    }
    for (i = 0; i < rl.rlim_max; i++) {
        close(i);
    }
    // 6 присоединить файловые дескрипторы 0,1,2 
    fd0 = open("dev/null", O_RDWR);
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
    struct tm *ptr, *start;
    time_t lt;
    lt = time(NULL);
    //printf(asctime(ptr));
    daemonize("my_deamon");
    // 9. Блокировка файла для одной существующей копии демона 
    if (already_running() != 0)
    {
        syslog(LOG_ERR, "Демон уже запущен!\n");
        exit(1);
    }
    start = localtime(&lt);
    char buf1[100];
    snprintf(buf1, 100, "start : %s",asctime(start) );
   // printf("%s", buf);

    syslog(LOG_WARNING, "Проверка пройдена!");
    while(1) 
    {
        time_t lt;
        lt = time(NULL);
        ptr = localtime(&lt);
        char buf[200];
        snprintf(buf, 200, "Deamon %s now : %s",buf1,asctime(ptr) );
        //printf("%s", buf);

        syslog(LOG_INFO, buf);
        sleep(60);
    }

}
