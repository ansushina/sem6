#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/interrupt.h>
#include <linux/timex.h>

MODULE_LICENSE("GPL");

static int my_irq = 1, my_dev_id, irq_cnt = 0;

void tasklet_function(unsigned long data);

char my_tasklet_data[] = "my_tasklet_function was called";

DECLARE_TASKLET(my_tasklet, tasklet_function, (unsigned long)&my_tasklet_data);

void tasklet_function(unsigned long data) {
    printk(KERN_INFO "++ tasklet_function was called. state '%ld' count '%i' data '%s'\n", my_tasklet.state, my_tasklet.count, (char*)data);
}

static irqreturn_t my_irq_handler(int irq, void *dev) {
    if (irq == my_irq) {
        printk(KERN_INFO "++ my_irq_handler was called %d time(s)\n", ++irq_cnt);
        tasklet_schedule(&my_tasklet);
        return IRQ_HANDLED;
    }
    return IRQ_NONE;
}

static int __init my_tasklet_init(void) {
    if (request_irq(my_irq, my_irq_handler, IRQF_SHARED, "my_tasklet", &my_dev_id)) {
        printk(KERN_ERR "++ can't get assigned IRQ %i\n", my_irq);
        return 1;
    }
    printk(KERN_INFO "++ Successfully loaded handler for IRQ %d\n", my_irq);
    return 0;
}

static void __exit my_tasklet_exit(void) {
    tasklet_kill(&my_tasklet);
    synchronize_irq(my_irq);
    free_irq(my_irq, &my_dev_id);
    printk(KERN_INFO "++ tasklet unloaded, irq_counter = %d\n", irq_cnt);
    return;
}

module_init(my_tasklet_init);

module_exit(my_tasklet_exit); 