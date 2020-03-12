#include <linux/module.h> // module_init, ...
#include <linux/kernel.h> // printk
#include <linux/init.h> //__init, __exit
#include <linux/sched.h>

#include <linux/init_task.h>

/* Лицензия, иначе будет kernel panic*/
MODULE_LICENSE("GPL");
MODULE_AUTHOR("Ansushina");
MODULE_DESCRIPTION("lab3");


/* Init-функция, вызываемая при загрузке модуля */
static int __init my_module_init(void) {
	printk(KERN_INFO " Module is loaded.\n");
	struct task_struct *task = &init_task;

	do {
		printk(KERN_INFO "---%s-%d, parent %s-%d", task->comm, task->pid, task->parent->comm, task->parent->pid);
	} while ((task = next_task(task)) != &init_task);

	return 0;
}

/* Cleanup-функция, вызываемая при выгрузке модуля */
static void __exit my_module_exit(void) {
	printk(KERN_INFO " Module is unloaded.\n");
}


/* Ядру сообщаются названия функций, вызываемых при загрузке и выгрузке модуля */
module_init(my_module_init);
module_exit(my_module_exit);
