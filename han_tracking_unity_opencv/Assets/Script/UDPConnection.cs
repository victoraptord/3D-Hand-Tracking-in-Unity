using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;

public class UDPConnection : MonoBehaviour
{

    Thread receiveThread;
    UdpClient client;
    public int port = 5052;
    public bool startReceiveing = true;
    public bool printToConsole = false;
    public static string data;

    // Start is called before the first frame update
    void Start()
    {
        receiveThread = new Thread(new ThreadStart(receiveData));
        receiveThread.IsBackground = true;
        receiveThread.Start();
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    private void receiveData()
    {
        client = new UdpClient(port);
        while(startReceiveing)
        {
            try 
            {
                IPEndPoint anyIP = new IPEndPoint(IPAddress.Any, 0);
                byte[] dataByte = client.Receive(ref anyIP);
                data = Encoding.UTF8.GetString(dataByte);

                if(printToConsole)
                {
                    print(data);
                }

            }
            catch (System.Exception e)
            {
                print(e.ToString());
            }
        }
    }
}
