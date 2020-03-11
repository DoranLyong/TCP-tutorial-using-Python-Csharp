using System;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Text;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace imageStream_client
{ 

public class Client_unity : MonoBehaviour
{
    IPHostEntry ipHostInfo;
    IPAddress ipAddress; // IPv4 
    TcpClient client_sock;
    const int PORT = 8080;

    NetworkStream stream;

    // Start is called before the first frame update
    void Start()
    {
        Debug.Log("*****Unity frame started *****");

        ipHostInfo = Dns.GetHostEntry(Dns.GetHostName());
        ipAddress = ipHostInfo.AddressList[1];
        client_sock = new TcpClient(ipAddress.ToString(), PORT);
        Debug.Log("***** Client Connected to the server *****");

        stream = client_sock.GetStream();        

    }

    // Update is called once per frame
    void Update()
    {
        //Debug.Log("**** Buffer streaming ****");

        // _Client -> Server 
        string message = "1";
        byte[] buff = Encoding.ASCII.GetBytes(message);

        stream.Write(buff, 0, buff.Length); // spend the byte stream into the Stream 


        // _Client <- Server 
        byte[] recvBuf = new byte[client_sock.ReceiveBufferSize]; // total receiveBuffer size 
        int readBytes = stream.Read(recvBuf, 0, recvBuf.Length);

        //Debug.Log($"total receiveBuffer length: {recvBuf.Length}");
        //Debug.Log($"Real-read byte length: {readBytes}");


        // _Set display image 
        byte[] image = new byte[readBytes];
        Buffer.BlockCopy(recvBuf, 0, image, 0, readBytes);

        Viewer.instance.SetImageToDisplay(image);
        



    }
}
}
