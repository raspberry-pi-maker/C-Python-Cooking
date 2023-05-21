#include <stdio.h>
#include <iostream>
#include <unistd.h>
#include <signal.h>

#include <SimpleAmqpClient/SimpleAmqpClient.h>

using namespace std;
using namespace AmqpClient;

bool g_loop = true;
void sig_handler(int signo)
{
    if (SIGINT == signo) g_loop = false;
}

int main(int argc, char * argv[])
{
    struct sigaction act;
    act.sa_handler = sig_handler;
    sigaction(SIGINT, &act, NULL);
    if(argc < 2){
        cout << "invalid parameter" <<endl;
        return 0;
    }
    int work_time = atoi(argv[1]);

    Channel::ptr_t channel = Channel::Create("192.168.150.128");
    channel->DeclareQueue("task_queue", false, true, false, false);
    //BasicConsume(const std::string &queue, const std::string &consumer_tag = "", bool no_local = true, bool no_ack = true, bool exclusive = true, uint16_t message_prefetch_count = (uint16_t)1U)    
    channel->BasicConsume("task_queue", "task_queue", true, false, false);
    channel->BasicQos("task_queue", 1);
    //channel->BasicConsume("hello","hello");
    cout << " [*] Waiting for messages. To exit press Ctrl + C" <<endl;
    while(g_loop){
        try{
            Envelope::ptr_t envelope;
            bool bflag = channel->BasicConsumeMessage("task_queue", envelope, 1000);
            if(bflag == false){  //time out
                //fprintf(stderr, ".");
                continue;
            }
            
            fprintf(stderr, " [x] Received %s\n",envelope->Message()->Body().c_str() );
            sleep(work_time);
            fprintf(stderr, "sleep %d seconds\n", work_time);
            fprintf(stderr, " [x] Done\n");

            Envelope::DeliveryInfo info;
            info.delivery_tag = envelope->DeliveryTag();
            info.delivery_channel = envelope->DeliveryChannel();
            channel->BasicAck(info);
        }
        catch(MessageReturnedException &e){
            fprintf(stderr, " Message receive error\n" );
        }
    }
    cout << "\n Goob Bye" << endl;    
    return 0;
}