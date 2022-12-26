#include <stdio.h>
#include <iostream>
#include <pthread.h>
#include <SimpleAmqpClient/SimpleAmqpClient.h>

using namespace std;
using namespace AmqpClient;
void *consumer_thread(void *data);

const char * routing_key[] = { "rk_A","rk_A,rk_B", "rk_B"};
const char * queue[] = { "QA","QB", "QC"};

int main(int argc, char * argv[])
{
    //for testing 3 queue (QA, QB, QC), I'll make 3 threads.
    pthread_t p_thread;
	pthread_create(&p_thread, NULL, consumer_thread, (void *)0);
	pthread_detach(p_thread);

	pthread_create(&p_thread, NULL, consumer_thread, (void *)1);
	pthread_detach(p_thread);

	pthread_create(&p_thread, NULL, consumer_thread, (void *)2);
	pthread_detach(p_thread);

    while(1) sleep(1);
}

void *consumer_thread(void *data)
{
    int index = *((int*)(&data));
    printf("index:%d\n", index);
    sleep(1);
    
    Channel::ptr_t connection = Channel::Create("192.168.150.128", 5672);
    connection->BasicConsume(queue[index], queue[index]);
    int timeout = 5000;
    char szmsg[1024];
    while(true){
        try{
            Envelope::ptr_t envelope;
            bool bflag = connection->BasicConsumeMessage(queue[index], envelope, timeout);
            if(bflag == false){  //time out
            cout << "time out => continue" << endl;
                continue;
            }
            cout << "Q[" << queue[index] << "] RCV:" << envelope->Message()->Body() << endl;
        }
        catch(MessageReturnedException &e){
            std::cout << "Message receive error: " << e.what() << std::endl;
        }
    }

}
