#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/interrupt.h>
#include <linux/timex.h>
#include <linux/workqueue.h>

MODULE_LICENSE("GPL");

static int my_irq = 1, my_dev_id, irq_cnt = 0;

struct workqueue_struct *wq;

static void my_wq_function(struct work_struct *work);

DECLARE_WORK(my_work, my_wq_function);

static void my_wq_function(struct work_struct *work) {
    printk(KERN_INFO "[WORKQUEUE] handler called: data '%d'", work->data);
}

static irqreturn_t my_irq_handler(int irq, void *dev_id) {
    irq_cnt++;
    printk(KERN_INFO "[WORKQUEUE]  my_irq_handler was called %d time(s)", irq_cnt);
    queue_work(wq, &my_work);
    return IRQ_NONE;

}

static int __init my_workqueue_init(void) {
    if (request_irq(my_irq, my_irq_handler, IRQF_SHARED, "my_int_workqueue", &my_dev_id)) {
        printk(KERN_ERR "[WORKQUEUE] can't get assigned IRQ %i\n", my_irq);
        return 1;
    }
    printk(KERN_INFO "[WORKQUEUE] assigned IRQ %i\n", my_irq);
    if ((wq = create_workqueue("my_workqueue"))) {
        printk(KERN_INFO "[WORKQUEUE]  workqueue created\n");
    } else {
        free_irq(my_irq, &my_dev_id);
        printk(KERN_INFO "[WORKQUEUE] workqueue allocation failed\n");
        return -ENOMEM;
    }
    printk(KERN_INFO "[WORKQUEUE]  module is now loaded\n");
    return 0;
}

static void __exit my_workqueue_exit(void) {
    flush_workqueue(wq);
    destroy_workqueue(wq);
    printk(KERN_INFO "[WORKQUEUE] workqueue destroyed\n");
    synchronize_irq(my_irq);
    free_irq(my_irq, &my_dev_id);
    printk(KERN_INFO "[WORKQUEUE]  IRQ handler removed\n");
    printk(KERN_INFO "[WORKQUEUE]  module destroyed\n");
}

module_init(my_workqueue_init);

module_exit(my_workqueue_exit);