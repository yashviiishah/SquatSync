using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

public class UDPReceiver : MonoBehaviour
{
    private UdpClient udpClient;
    public int port = 5005;

    void Start()
    {
        udpClient = new UdpClient(port);
        Debug.Log("UDP Receiver started, waiting for messages...");

        // Start receiving data asynchronously
        UdpReceive();
    }

    private async void UdpReceive()
    {
        IPEndPoint remoteEndPoint = new IPEndPoint(IPAddress.Any, port);
        try
        {
            while (true)
            {
                // Receive the UDP data asynchronously
                UdpReceiveResult receivedResult = await udpClient.ReceiveAsync();
                string message = Encoding.UTF8.GetString(receivedResult.Buffer);

                // Log the message and check for 'is_squat'
                Debug.Log($"Received: {message} from {receivedResult.RemoteEndPoint}");

                if (message.Contains("is_squat"))
                {
                    Debug.Log("is_squat received from Python!");
                    PlayerMovement.movePlayer = true;
                }
            }
        }
        catch (System.Exception ex)
        {
            Debug.LogError($"Error receiving data: {ex.Message}");
        }
    }

    void OnApplicationQuit()
    {
        udpClient.Close();  // Close the UDP client when the application quits
    }
}
